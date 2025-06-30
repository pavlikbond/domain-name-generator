# Domain Name Generator

A machine learning system that generates creative and brandable domain name suggestions based on business descriptions. The system is trained on website classification data to learn the relationship between business descriptions and domain names.

## Overview

This project transforms website classification data into training examples for domain name generation. Instead of classifying websites, the model learns to suggest domain names when given a business description.

## Features

- **Data Processing**: Converts website classification data into domain name training examples
- **Synthetic Examples**: Includes hand-crafted examples for better training coverage
- **Interactive Generator**: Command-line interface for generating domain suggestions
- **Training Data Export**: Creates formatted training files for model fine-tuning

## Project Structure

```
domain-name-generator/
├── data.py                 # Core data processing and training example creation
├── main.py                 # Data analysis and training file generation
├── domain_generator.py     # Interactive domain name generator
├── requirements.txt        # Python dependencies
├── website_classification.csv  # Input data (website descriptions and categories)
└── README.md              # This file
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd domain-name-generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Process Training Data

Run the main script to process the website classification data and create training examples:

```bash
python main.py
```

This will:

- Load and process the CSV data
- Add synthetic examples
- Analyze the training data
- Show sample training examples
- Create a training file (`domain_training_data.txt`)

### 2. Generate Domain Suggestions

Use the interactive domain name generator:

```bash
python domain_generator.py
```

Example usage:

```
Business Description: A local coffee shop that serves organic coffee and fresh pastries
Domain Suggestions:
1. brewbean.com - Combines coffee brewing with organic beans
2. freshbrew.org - Emphasizes fresh coffee brewing
3. pastrybrew.net - Combines pastries with coffee brewing
```

### 3. Programmatic Usage

```python
from domain_generator import DomainNameGenerator

# Initialize the generator
generator = DomainNameGenerator()

# Generate domain suggestions
business_desc = "Online platform for freelance graphic designers"
suggestions = generator.generate_domains_simple(business_desc)
print(suggestions)
```

## Data Format

### Input Data (website_classification.csv)

- `website_url`: The original website URL
- `cleaned_website_text`: Business description extracted from the website
- `Category`: Business category/industry

### Training Data Format

The system creates training examples in this format:

```
<|system|>
You are a domain name expert. Generate 3-5 creative, memorable, and brandable domain names for the given business description. Each domain should be:
- Easy to remember and spell
- Relevant to the business
- Available as .com, .org, or .net
- Professional and brandable
<|user|>
Business: [business description]
<|assistant|>
1. [domain].com - [explanation]
2. [domain].org - [explanation]
3. [domain].net - [explanation]
```

## Model Training

To fine-tune a model with the generated training data:

1. Run `python main.py` to create `domain_training_data.txt`
2. Use the training file with your preferred fine-tuning framework (e.g., Hugging Face Transformers, LoRA, QLoRA)
3. The training data is formatted for conversation-style models like Llama

## Configuration

### Model Settings

- **Base Model**: `meta-llama/Meta-Llama-3.1-8B` (configurable in `data.py`)
- **Token Limits**: 150-200 tokens for business descriptions
- **Temperature**: 0.7 for generation (configurable in `domain_generator.py`)

### Data Processing

- **Minimum Characters**: 300 characters for business descriptions
- **Text Cleaning**: Removes special characters, excessive whitespace, and long words with numbers
- **Synthetic Examples**: 5 hand-crafted examples for better training coverage

## Example Output

### Training Example

```
Business Description: official site good hotel accommodation big saving hotel destination worldwide browse hotel review find guarantee good price hotel budget lodging accommodation hotel hotels special offer package special weekend break city break deal budget cheap discount saving select language find deal hotel home try search connect traveller india travel talk community recommend destination flamborough boreland colvend catfield harberton warleggan inspiration trip spot winter wildlife beautiful snowy island bye bye work want spontechnaity tech drive travel vital value maximise travel homes guest love browse property type hotels apartments resorts villa cabins cottage glamping serviced apartment holiday home guest house hostels motels ryokans riads holiday park homestays campsites country house farm stay boats luxury tent self catering accommodation tiny house chapel saint leonards wuqing wuchang saint eval great rowsley instow verified review real guest work start booking follow trip finally review skip main content inr choose currency current currency indian rupee choose language current language english uk english uk english deutsch nederlands français español español ar español mx catal italiano português pt português br norsk suomi svenska dansk ÄeÅ¡tina magyar românÄƒ æ—¥æœ¬èªž ç®€ä½"ä¸­æ–‡ ç¹é«"ä¸­æ–‡ polski ÎµÎ»Î»Î·Î½Î¹ÎºÎ¬ Ñ€ÑƒÑÑÐºÐ¸Ð¹ türkÃ§e Ð±ÑŠÐ»Ð³Ð°Ñ€ÑÐºÐ¸ Ø§Ù„Ø¹Ø±Ø¨ÙŠØ© í•œêµ­ì–´ ×¢×'×¨×™×ª latviski ÑƒÐºÑ€Ð°Ñ—Ð½ÑŒÐºÐ° bahasa indonesia bahasa malaysia à¸ à¸²à¸©à¸²à¹„à¸—à¸¢ eesti hrvatski lietuviÅ³ slovenÄina srpski slovenÅ¡Äina tiáº¿ng viá»‡t filipino Ã­slenska help reservation list property register sign coronavirus support check travel restriction travel permit certain purpose particular touristic travel allow read find deal hotel home cosy country home funky city flat type destination error enter destination start search flamborough boreland colvend catfield check check room occupancy adult child room adults adults children child rooms room search want entire home apartment travel work result show map travel offer enjoy stay january deal early deal save booking good start find deal travel community traveller general discussion traveller view traveller explore india popular destination lot offer goa property lonavala property north goa property mahabaleshwar property mumbai property new delhi property south goa property jaipur property alibaug property bangalore property find apartment villa aparthotels holiday homes cottage home apartment trip discover home flamborough property boreland colvend property catfield property harberton property warleggan property animal hibernate winter destination embrace cold magical frost tip vista blissful quiet snowy island promise pure escapism remote work long term reality soon set office traveller technology regain confidence help travel safely traveller prioritise value money book transparency flexibility sign member deal reveal secret deal sign hotels hotel apartment apartment resort resort villas villas cabin cabin cottage cottage glampe glamping site service apartment serviced apartment holiday home holiday home guest house guest house hostels hostel motel motel ryokan ryokan riad riad holiday park holiday park homestays homestay campsite campsite country house country house farm stay farm stay boats boat luxury tent luxury tent self catering accommodation self catering property tiny house tiny house united kingdom holiday rental holiday home villa apartment glamping site china china united kingdom holiday rental villa holiday home united kingdom villa holiday home holiday rental united kingdom holiday rental holiday home villa destination list property mobile version account change book online contact customer service affiliate business countries regions cities districts airports hotels places interest home apartments resorts villas hostels guest house unique place stay destination reviews travel communities seasonal holiday deal travel agents coronavirus faq contact customer service partner help careers sustainability press centre safety resource centre investor relation terms conditions partner dispute privacy cookie statement corporate contact seek get perfect place listing include listing home apartment unique place stay locate destination country territory base amsterdam netherlands support internationally office country extranet login copyright right reserve booking holdings world leader online travel related service start dialog content million property review real verify guest start booking way leave review booking know review come real guest stay property follow trip guest stay property check quiet room friendly staff finally review trip guest tell stay check naughty word verify authenticity guest review add site book want leave review sign sign leave review end dialog content check date check date mo tu th fr sa su close calendar sign continue sign account use option account create account gogless
Category: Travel
Domain: booking.com
```

### Generated Suggestions

```
Business: A local coffee shop that serves organic coffee and fresh pastries
Domain Suggestions:
1. brewbean.com - Combines coffee brewing with organic beans
2. freshbrew.org - Emphasizes fresh coffee brewing
3. pastrybrew.net - Combines pastries with coffee brewing
4. organicbrew.com - Highlights organic coffee focus
5. brewcafe.org - Simple, memorable coffee shop name
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Acknowledgments

- Uses the Meta Llama 3.1 8B model as the base
- Training data derived from website classification datasets
- Built with Hugging Face Transformers library
