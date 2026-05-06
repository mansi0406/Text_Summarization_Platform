# Text Summarizer Project Documentation

## Project Overview

A Streamlit-based text summarization application that supports input from direct text, uploaded files, and web URLs. The app uses Hugging Face transformer models to generate concise summaries and allows users to download the summary as a PDF.

---

## Features

- Summarize plain text input
- Summarize text from uploaded `.txt` or `.md` files
- Fetch and summarize text content from web pages
- Choose from multiple summarization models
- Configure summary token length
- Download generated summary as a PDF
- Basic input cleaning and truncation for long content

---

## System Architecture

| Component        | Description |
|------------------|-------------|
| User Interface   | Built using Streamlit to collect input and display output |
| Input Handler    | Handles text, file, and URL inputs |
| Text Processor   | Cleans and truncates large text |
| AI Model Layer   | Hugging Face transformer models for summarization |
| Output Module    | Displays summary and generates PDF |

---

## Supported Input Types

| Input Type | Description | Example |
|-----------|------------|--------|
| Text      | Direct user input | Paragraph pasted into textbox |
| File      | Upload `.txt` or `.md` | Notes file |
| URL       | Web scraping using BeautifulSoup | News article |

---

## Model Comparison

| Model Name                        | Type        | Speed     | Accuracy  | Notes |
|----------------------------------|-------------|----------|-----------|------|
| sshleifer/distilbart-cnn-12-6    | Lightweight | Fast     | Moderate  | Best for low-resource systems |
| facebook/bart-large-cnn          | Heavy       | Slow     | High      | Produces high-quality summaries |
| t5-small                         | Lightweight | Fast     | Moderate  | Requires "summarize:" prefix |

---

## Requirements

- streamlit==1.57.0
- transformers==4.41.2
- fpdf==1.7.2
- requests==2.33.1
- beautifulsoup4==4.14.3

---

## Installation

1. python -m venv venv
2. Activate:
   - PowerShell: .\venv\Scripts\Activate.ps1
   - CMD: .\venv\Scripts\activate.bat
3. pip install streamlit transformers fpdf requests beautifulsoup4

---

## Running the App

streamlit run app.py

---

## Usage Instructions

1. Select input type
2. Provide input
3. Choose model
4. Click summarize
5. View output

---

## Application Flow

User Input → Processing → Model → Summary → Display

---

## Error Handling

| Scenario | Handling |
|---------|--------|
| Empty input | Warning |
| Invalid URL | Error |
| Large text | Truncated |

---

## Performance Considerations

- Large models need more RAM
- First run downloads model
- Caching improves speed

---

## Sample Input and Output

Input: AI is transforming industries.

Output: AI improves industries.

---

## Limitations

- Input size limits
- Depends on hardware
- Uses pre-trained models

---

## Future Enhancements

- Multi-language
- Chat with document
- Deployment

---

## File Structure

- app.py
- documentation files

---

## License

Educational use only
