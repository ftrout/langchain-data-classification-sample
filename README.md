# Sensitive Data Classifier

This Python script uses [LangChain](https://www.langchain.com/) to classify sensitive data in text inputs. It leverages OpenAI's GPT-4o model (by default) to categorize text into predefined sensitive data categories, such as Personally Identifiable Information (PII), Financial Information, Health Information, Proprietary Business Information, Export-Controlled Information, or Non-Sensitive data. The script returns a structured JSON output with the category, confidence score, and explanation for each classification, using Pydantic for output parsing.

## Features
- Classifies text into sensitive data categories using a language model.
- Provides structured output with category, confidence score (0-1), and explanation.
- Supports customizable sensitive data categories.
- Built with LangChain for easy integration with various LLMs.
- Uses `python-dotenv` to securely manage API keys.
- Includes error handling for robust operation.

## Prerequisites
- **Python**: Version 3.7 or higher.
- **Dependencies**: Specified in `requirements.txt`:
  - `langchain`
  - `langchain-core`
  - `langchain-openai`
  - `openai`
  - `python-dotenv`
  - `pydantic`
- **OpenAI API Key**: Required to use the OpenAI language model (e.g., GPT-4o).

## Sample Output
```
Input Text: Employee SSN: 123-45-6789, Name: John Doe
Classification Result:
Category: Personally Identifiable Information (PII)
Confidence: 0.95
Explanation: The input text contains an SSN and a name, both of which are considered PII as they can be used to uniquely identify an individual.

Input Text: Company financial report: Q3 revenue $1.2M
Classification Result:
Category: Financial Information
Confidence: 0.90
Explanation: The text contains information about a company's financial performance, specifically mentioning the Q3 revenue, which is classified as financial information.

Input Text: Patient diagnosis: Diabetes Type 2
Classification Result:
Category: Health Information
Confidence: 0.95
Explanation: The input text contains information about a patient's medical condition, which is classified as health information.

Input Text: This is a public news article about weather.
Classification Result:
Category: Non-Sensitive
Confidence: 0.95
Explanation: The input text is a public news article about weather, which does not contain any sensitive information such as PII, financial, health, proprietary business, or export-controlled information.

Input Text: Technical specifications for export-restricted software
Classification Result:
Category: Export-Controlled Information
Confidence: 0.95
Explanation: The input text refers to technical specifications for export-restricted software, which typically falls under export-controlled information due to regulations on the dissemination of such sensitive technology and data.
```