from typing import Dict, List, Any
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

class EndpointHandler():
    def __init__(self, path=""):
        """
        Initialize the handler with the base model + LoRA adapters
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load base model first
        base_model_name = "unsloth/llama-3.2-3b-unsloth-bnb-4bit"
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            load_in_4bit=True  # Use 4-bit to save memory
        )
        
        # Load LoRA adapters from the path (your model repo)
        self.model = PeftModel.from_pretrained(base_model, path)
        
        # Constants from your training code
        self.INAPPROPRIATE_CONTENT_TEXT = "Request contains inappropriate content"
        
        # Set up chat template (this is crucial!)
        self.tokenizer.chat_template = """{% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = bos_token + content %}{% endif %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}{% endif %}"""
        
        # Ensure pad token is set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def extract_domains(self, text_output):
        """
        Extract domains from the model's text output
        """
        # Find the assistant's response after the header
        assistant_match = re.search(r'<\|start_header_id\|>assistant<\|end_header_id\|>', text_output, re.IGNORECASE)

        if assistant_match:
            text_to_process = text_output[assistant_match.end():]
        else:
            text_to_process = text_output

        if self.INAPPROPRIATE_CONTENT_TEXT in text_to_process:
            return [self.INAPPROPRIATE_CONTENT_TEXT]

        # Clean up the text - remove special tokens with spaces to avoid concatenation
        text_to_process = re.sub(r'<\|[^|]*\|>', ' ', text_to_process)  # Replace special tokens with space
        text_to_process = re.sub(r'\s+', ' ', text_to_process).strip()  # Normalize whitespace

        # Multiple domain patterns to catch different formats
        patterns = [
            r'\b([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]\.[a-zA-Z]{2,})\b',  # Basic domain pattern
            r'\d+\.\s*([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]\.[a-zA-Z]{2,})',  # Numbered list pattern
            r'\b([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]\.(com|net|org|io|dev|games|tech|online))\b'  # Specific TLDs
        ]

        domains = []
        for pattern in patterns:
            matches = re.findall(pattern, text_to_process, re.IGNORECASE)
            for match in matches:
                # Handle tuple results from patterns with groups
                domain = match[0] if isinstance(match, tuple) else match
                # Additional validation: ensure domain doesn't contain weird characters
                if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$', domain) and domain not in domains:
                    domains.append(domain)

        # Return the domains found, or a message if none
        return domains[:5] if domains else ['No domains were found']

    def create_conversation(self, business_description: str):
        """
        Create the conversation format for the model (exactly as in training)
        """
        return [
            {
                "role": "system",
                "content": "You are a creative assistant that suggests catchy domain names for businesses."
            },
            {
                "role": "user",
                "content": f"Generate 3 to 5 creative and memorable domain names for the following business description. Avoid hyphens or numbers. Prioritize .com domains unless a better option fits. Keep names short, brandable, and easy to spell.\n\nBusiness Description: {business_description}"
            }
        ]

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the inference request
        """
        try:
            # Extract business description (support both formats)
            business_description = data.get("business_description") or data.get("inputs", "")
            if not business_description:
                return {
                    "suggestions": [],
                    "status": "error",
                    "message": "No business description provided"
                }
            
            # Extract parameters
            parameters = data.get("parameters", {})
            temperature = parameters.get("temperature", 1.2)
            max_new_tokens = parameters.get("max_new_tokens", 64)
            min_p = parameters.get("min_p", 0.1)
            
            # Create conversation
            messages = self.create_conversation(business_description)
            
            # Apply chat template (same as your working code)
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate (same parameters as your working code)
            with torch.no_grad():
                output_ids = self.model.generate(
                    input_ids=input_ids,
                    max_new_tokens=max_new_tokens,
                    use_cache=True,
                    eos_token_id=self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
                    temperature=temperature,
                    min_p=min_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            # Decode response (same as your working code)
            generated_tokens = output_ids[0][input_ids.shape[-1]:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=False)
            
            # Clean up response (same as your working code)
            response = response.split("<|reserved_special_token_")[0].strip()
            
            # Extract domains
            domains = self.extract_domains(response)
            
            # Check for inappropriate content
            if domains == [self.INAPPROPRIATE_CONTENT_TEXT]:
                return {
                    "suggestions": [],
                    "status": "blocked",
                    "message": "Request contains inappropriate content"
                }
            
            # Convert domains to suggestions
            suggestions = []
            for domain in domains:
                if domain != 'No domains were found':
                    suggestions.append({"domain": domain})
            
            return {
                "suggestions": suggestions,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "suggestions": [],
                "status": "error",
                "message": f"An error occurred during inference: {str(e)}"
            }