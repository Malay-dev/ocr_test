import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Set up your Google API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def extract_details(raw_text):
    """
    Extract details from the raw text using Gemini.
    
    Args:
        raw_text (str): The raw text containing product details.
    Returns:
        dict: A dictionary with extracted details such as product name, type, ingredients, etc.
    """
    try:
        # Set up the model
        model = genai.GenerativeModel('gemini-pro')

        # Prepare the prompt
        prompt = f"""Extract product details from the following text and format the response as a valid JSON object:

{raw_text}

Provide the information in the following format:
{{
  "product_name": "",
  "product_type": "",
  "ingredients": "",
  "manufacturer": "",
  "other_details": {{}}
}}

Ensure that all keys and string values are enclosed in double quotes, and that the entire response is a valid JSON object."""

        # Generate content
        response = model.generate_content(prompt)

        # Get the text content of the response
        response_text = response.text

        # Remove any leading or trailing whitespace and newlines
        response_text = response_text.strip()

        # If the response is not wrapped in curly braces, add them
        if not response_text.startswith('{'):
            response_text = '{' + response_text
        if not response_text.endswith('}'):
            response_text = response_text + '}'

        # Parse the response
        extracted_details = json.loads(response_text)
        
        return extracted_details
    
    except json.JSONDecodeError as json_error:
        print(f"JSON parsing error: {json_error}")
        print(f"Raw response: {response_text}")
        return {}
    except Exception as e:
        print(f"An error occurred while extracting details: {e}")
        return {}

def main():
    # Load the raw text from the file
    input_file_path = 'D:/google_dev_hack/ocr_test/output_detected_text.txt'
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
        
        # Extract details from the raw text
        extracted_details = extract_details(raw_text)
        
        # Print the extracted details in JSON format
        print(json.dumps(extracted_details, indent=4))
    
    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

