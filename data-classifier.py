from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file or environment variables.")

# Define sensitive data categories
SENSITIVE_CATEGORIES = [
    "Personally Identifiable Information (PII)",
    "Financial Information",
    "Health Information",
    "Proprietary Business Information",
    "Export-Controlled Information",
    "Non-Sensitive"
]

# Define Pydantic model for structured output
class ClassificationOutput(BaseModel):
    category: str = Field(description="The sensitive data category the input text belongs to")
    confidence: float = Field(description="Confidence score for the classification (0-1)")
    explanation: str = Field(description="Explanation for the classification")

# Initialize the output parser
output_parser = PydanticOutputParser(pydantic_object=ClassificationOutput)
format_instructions = output_parser.get_format_instructions()

# Define the prompt template for sensitive data classification
prompt_template = """
You are a sensitive data classifier. Your task is to analyze the input text and classify it into one of the following categories: {categories}. 
Provide a confidence score (0-1) and a brief explanation for your classification. 
Return the response in the following JSON format:

{format_instructions}

Input text: {input_text}
"""

# Initialize the language model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3, openai_api_key=openai_api_key)

# Create the prompt and chain
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["input_text"],
    partial_variables={"categories": ", ".join(SENSITIVE_CATEGORIES), "format_instructions": format_instructions}
)

# Create a RunnableSequence instead of LLMChain
chain = prompt | llm | output_parser

# Function to classify sensitive data
def classify_sensitive_data(text):
    try:
        result = chain.invoke({"input_text": text})
        return result
    except Exception as e:
        return ClassificationOutput(
            category="Non-Sensitive",
            confidence=0.0,
            explanation=f"Failed to classify due to an error: {str(e)}"
        )

# Example usage
if __name__ == "__main__":
    # Example texts to classify
    test_texts = [
        "Employee SSN: 123-45-6789, Name: John Doe",
        "Company financial report: Q3 revenue $1.2M",
        "Patient diagnosis: Diabetes Type 2",
        "This is a public news article about weather.",
        "Technical specifications for export-restricted software"
    ]

    for text in test_texts:
        print(f"\nInput Text: {text}")
        result = classify_sensitive_data(text)
        print("Classification Result:")
        print(f"Category: {result.category}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Explanation: {result.explanation}")