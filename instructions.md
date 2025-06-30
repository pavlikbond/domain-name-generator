# AI Engineer Homework

## Instructions

- Provide reproducible code with detailed setup instructions
- Programming language: **Python**
- Focus on **model evaluation**, **edge case discovery**, and **iterative improvement**
- API deployment is optional (**bonus points**)

---

## Expected Deliverables

1. Git repo with **Jupyter Notebook** containing all experiments and evaluations
2. Experiments should be **reproducible** with clear **model version tracking**
3. **Runnable evaluation framework** that works across all model iterations
4. **Technical report** with findings and improvement analysis (brief write-up is enough). Be ready to discuss in more depth during the interview
5. You can submit **partial tasks** with an explanation of any incomplete parts

---

## Task Overview

Build and iteratively improve a **fine-tuned LLM** for **domain name suggestions**, with emphasis on:

- Systematic evaluation
- Edge case discovery
- Model improvement cycles
- Ensuring model refuses to generate inappropriate or harmful domain names
- (Optional) Deploy selected model as an API endpoint

**Tip:** If time is limited, focus on **model evaluation and improvement framework** rather than full fine-tuning/deployment

---

## Required Components

### 1. Synthetic Dataset Creation

- Create an initial synthetic dataset
- Include **diverse business types** and **complexity levels**
- **Document** dataset creation methodology

---

### 2. Model Development & Iteration

- **Baseline Model**: Fine-tune an initial open-source LLM (use common recipes)
- **Improved Model(s)**: Address issues via:
  - Dataset augmentation
  - Different fine-tuning approaches (LoRA, full fine-tuning, etc.)
  - Hyperparameter optimization
- **Save and version all model checkpoints**

---

### 3. LLM-as-a-Judge Evaluation Framework

**Implementation Requirements:**

- Design and implement **automated evaluation** using LLM-as-a-judge
- You may use third-party API models (GPT-4, Claude, etc.) or fine-tune your own evaluation model
- Create a **systematic scoring methodology** for domain name quality

---

### 4. Edge Case Discovery & Analysis

- Systematically discover **model failure modes** and edge cases
- **Categorize and analyze** failure types
- Show **measurable improvements** in handling edge cases
- Document **root causes** and **improvement strategies**

---

### 5. Safety Guardrails

- Implement **content filtering** for inappropriate requests
- Document your **approach and testing** with examples

---

## Model Requirements

- **Domain Name Generator**: Must use open-source LLM (e.g., LLaMA, Mistral, etc.)
- **LLM-as-a-Judge**: May use API-based models or fine-tuned open-source models
- All code must be **reproducible** with **clear setup instructions**

---

## Technical Report Guidelines

### 1. Methodology & Initial Results

- Dataset creation approach and baseline model selection
- Initial model performance and evaluation metrics

### 2. Edge Case Analysis

- Discovery process: How edge cases were identified
- Failure taxonomy: Categories with examples
- Frequency analysis: How common each failure type is

### 3. Iterative Improvement

- Improvement strategies: What was tried and why
- Quantified results: Before/after metrics
- LLM judge validation: Ensuring evaluation quality

### 4. Model Comparison & Recommendations

- Performance comparison: Statistical significance of improvements
- Production readiness: Which version you'd deploy and why
- Future improvements: Next steps

---

## API Development (Optional)

Create a simple API endpoint:

### API Specifications

- **Input**: JSON with a `business_description` field
- **Output**: JSON with list of domain suggestions, confidence scores, and status

#### Example Request:

```json
{
  "business_description": "organic coffee shop in downtown area"
}
{
  "suggestions": [
    {"domain": "organicbeanscafe.com", "confidence": 0.92},
    {"domain": "downtowncoffee.org", "confidence": 0.87},
    {"domain": "freshbreworganic.net", "confidence": 0.83}
  ],
  "status": "success"
}

```

#### Safety Example

```json
{
  "business_description": "adult content website with explicit nude content"
}
{
  "suggestions": [],
  "status": "blocked",
  "message": "Request contains inappropriate content"
}
```
