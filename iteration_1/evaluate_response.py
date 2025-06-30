import os
import openai
import json
import re
from google.colab import userdata
import torch

class DomainResponseEvaluator:
    """Simple class for evaluating domain name suggestions using GPT-4 as judge"""
    
    def __init__(self):
        api_key = userdata.get('OPENAI_API_KEY')
        print(api_key)
        os.environ['OPENAI_API_KEY'] = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def calculate_average_score(self, scores):
        """Calculate average score from individual criteria scores"""
        criteria_scores = [
            scores.get('relevance', 0),
            scores.get('creativity', 0),
            scores.get('memorability', 0),
            scores.get('conciseness', 0),
            scores.get('safety', 0)
        ]
        return round((sum(criteria_scores) / len(criteria_scores) / 10), 2)
    
    def evaluate_domains(self, business_description, domains):
        """
        Evaluate a list of domain names against a business description
        
        Args:
            business_description (str): Description of the business
            domains (list): List of domain names to evaluate
            
        Returns:
            list: List of dictionaries with domain info and scores
        """
        
        evaluation_prompt = f"""You are an expert evaluator of domain name suggestions. Please evaluate the following domain names for the given business description.

        Business Description: {business_description}

        Domain Names to Evaluate:
        {chr(10).join([f"{i+1}. {domain}" for i, domain in enumerate(domains)])}

        For each domain, evaluate on these criteria using a 0-10 scale (use whole numbers only):
        1. Relevance (how well the name relates to the business)
        2. Creativity (how unique and innovative the name is)
        3. Memorability (how easy the name is to remember)
        4. Conciseness (how short and clear the name is)
        6. Safety (whether name is appropriate and non-harmful)

        Scoring Guide:
        - 0-2: Poor
        - 3-4: Below Average
        - 5-6: Average
        - 7-8: Good
        - 9-10: Excellent

        Respond in this exact JSON format:
        [
            {{
                "domain": "domain1.com",
                "relevance": <score>,
                "creativity": <score>,
                "memorability": <score>,
                "conciseness": <score>,
                "safety": <score>
            }},
            {{
                "domain": "domain2.com",
                "relevance": <score>,
                "creativity": <score>,
                "memorability": <score>,
                "conciseness": <score>,
                "safety": <score>
            }}
        ]

        Only respond with the JSON array, no other text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert evaluator. Respond only with valid JSON array."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            if content is None:
                print("Received empty response from LLM")
                return []
                
            content = content.strip()
            
            # Try to parse JSON, handle potential formatting issues
            try:
                results = json.loads(content)
                # Calculate average score for each result
                for result in results:
                    result['confidence'] = self.calculate_average_score(result)
                return results
            except json.JSONDecodeError:
                # Try to extract JSON if there's extra text
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    results = json.loads(json_match.group())
                    # Calculate average score for each result
                    for result in results:
                        result['confidence'] = self.calculate_average_score(result)
                    return results
                else:
                    print(f"Could not parse JSON from response: {content}")
                    return []
                    
        except Exception as e:
            print(f"Error evaluating domains: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Test the evaluator with good domains
    evaluator = DomainResponseEvaluator()
    
    test_business = "An online store selling artisanal handmade leather goods."
    test_domains = ["leathercraft.com", "artisanleather.com", "handmadegoods.com", "craftyleather.com"]
    
    print("Evaluating domains...")
    results = evaluator.evaluate_domains(test_business, test_domains)
    
    print(f"\nEvaluation Results:")
    for result in results:
        print(json.dumps(result, indent=2))
        print() 

    # Test the evaluator with bad domains
    test_business = "An online store selling artisanal handmade leather goods."
    test_domains = ["junglegym.com", "cargurus.com", "thebestleathershopthatyoucanbuyfrom.com", "leatherleatherleather.net"]
    
    print("Evaluating domains...")
    results = evaluator.evaluate_domains(test_business, test_domains)
    
    print(f"\nEvaluation Results:")
    for result in results:
        print(json.dumps(result, indent=2))
        print() 