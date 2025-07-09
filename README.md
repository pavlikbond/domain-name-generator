# Domain Name Generator

A machine learning system that generates creative and brandable domain name suggestions based on business descriptions.

## Quick Start

This project contains multiple iterations of model training and evaluation. All iterations are designed to run in **Google Colab**.

### Iterations

- **Iteration 1** (`iteration_1/`): Initial training data preparation and model fine-tuning
- **Iteration 2** (`iteration_2/`): Improved training with better data processing
- **Iteration 3** (`iteration_3/`): Final iteration with comprehensive testing
- **Testing** (`testing/`): Model comparison and evaluation scripts

### How to Run

1. Open any of the `.ipynb` files in Google Colab
2. Upload the corresponding data files to your Colab session
3. Run the cells sequentially

### Deployment

The trained model is deployed as a Hugging Face endpoint. See `deployment/` folder for the handler code.

## Project Structure

```
├── iteration_1/          # First training iteration
├── iteration_2/          # Second training iteration
├── iteration_3/          # Third training iteration
├── testing/              # Model evaluation and comparison
├── deployment/           # Hugging Face endpoint handler
└── README.md
```

## Requirements

- Google Colab (for running iterations)
- Hugging Face account (for model deployment)
- Python 3.8+
