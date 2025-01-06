# SaRGeN (Suspicious Activity Report Generator)

## Overview
SaRGeN is a comprehensive Bank Secrecy Act (BSA) / Anti-Money Laundering (AML) Detection System that helps financial institutions analyze transactions, detect suspicious patterns, and generate Suspicious Activity Reports (SARs). The system uses advanced analytics and machine learning to identify potential money laundering activities and streamline the SAR reporting process.

## Features

### 1. Transaction Analysis Dashboard
- **Real-time Data Preview**
  - Transaction volume trends
  - Amount distribution analysis
  - Top customer activity visualization
  - Statistical summaries and metrics
  - Interactive data filtering and exploration

### 2. Red Flag Detection System
- **Automated Rule Detection**
  - High-value cash deposits
  - Structured transactions
  - High-risk country transactions
  - High-velocity cash activity
  - Keyword-based detection
  - Unusual transaction patterns
  - Large incoming wire monitoring

- **Customizable Analysis**
  - Filter by customer
  - Multiple rule selection
  - Visual pattern analysis
  - Transaction flagging and tracking

### 3. SAR Generation System
- **Intelligent Narrative Generation**
  - AI-powered report writing
  - Structured format following regulatory guidelines
  - Transaction evidence integration
  - Professional formatting
  - Customizable templates

### 4. Customer Violation Analysis
- **Advanced Monitoring**
  - Multiple violation detection
  - Customer risk profiling
  - Transaction pattern visualization
  - Historical activity analysis
  - Rule violation summaries

## Technical Architecture

### Core Components
1. **Data Processing Module**
   - Transaction data validation
   - Date/time normalization
   - Customer data aggregation
   - Statistical analysis

2. **Visualization System**
   - Interactive charts and graphs
   - Consistent theming
   - Responsive design
   - Custom styling system

3. **Rule Engine**
   - Configurable detection rules
   - Real-time processing
   - Multi-factor analysis
   - Pattern recognition

4. **AI Integration**
   - GPT-powered narrative generation
   - Natural language processing
   - Context-aware reporting
   - Professional output formatting

## Installation

```bash
# Clone the repository
git clone https://github.com/Kaleemullahqasim/SaRGeN

# Navigate to project directory
cd SaRGeN

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Start the application
streamlit run app.py
```

## Required Data Format
The system expects CSV files with the following columns:
- `transaction_id`: Unique identifier for each transaction
- `customer_id`: Customer identifier
- `date`: Transaction date
- `amount`: Transaction amount
- `type`: Transaction type
- Additional fields as needed for specific rule detection

## Configuration
Key configurations can be modified in the following files:
- `red_flag_rules.py`: Detection rule parameters
- `modules/visualization.py`: Visual theming and styling
- `sar_groq.py`: AI narrative generation settings

## Dependencies
- streamlit
- pandas
- numpy
- plotly
- groq
- watchdog

## Development

### Project Structure
```
SaRGeN/
├── app.py                 # Main application
├── requirements.txt      # Project dependencies
├── red_flag_rules.py    # Detection rules
├── sar_groq.py          # SAR generation
└── modules/
    ├── visualization.py  # Visualization components
    └── data_processing.py # Data processing utilities
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[MIT License](LICENSE)

## Acknowledgments
- Built with Streamlit
- Powered by Groq AI
- Visualization by Plotly

## Support
For support, please open an issue in the GitHub repository or contact the maintainers.