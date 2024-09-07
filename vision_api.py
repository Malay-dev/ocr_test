import os
import io
import json

from google.cloud import vision
from google.cloud.vision_v1 import ImageAnnotatorClient

from gemini_api import extract_details 

def set_google_credentials(credentials_path):
    """
    Set the environment variable for Google Cloud credentials.
    """
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    print("Google Cloud credentials set successfully")

def create_vision_client():
    """
    Create and return a Google Cloud Vision client.
    """
    try:
        client = ImageAnnotatorClient()
        print("Vision client created successfully")
        return client
    except Exception as e:
        raise RuntimeError(f"Error creating Vision client: {e}")

def load_image(image_path):
    """
    Load and return the content of an image file.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    print("Image loaded successfully")
    return vision.Image(content=content)

def detect_text_in_image(client, image):
    """
    Perform text detection on the provided image and return the detected text.
    """
    try:
        response = client.text_detection(image=image)
        print("Response received")

        if response.error.message:
            raise RuntimeError(f"{response.error.message}\nFor more info on error messages, check: "
                               "https://cloud.google.com/apis/design/errors")

        if response.text_annotations:
            return response.text_annotations[0].description
        else:
            return "No text detected in the image"
    except Exception as e:
        raise RuntimeError(f"An error occurred during text detection: {e}")

def write_text_to_file(text, output_file_path):
    """
    Write the detected text to a file.
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Detected text written to {output_file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while writing to file: {e}")

def main():
    credentials_path = 'D:/google_dev_hack/ocr_test/service_account_key.json'
    image_folder_path = 'D:/google_dev_hack/ocr_test/images'
    file_name = '2.jpg'
    output_file_path = 'D:/google_dev_hack/ocr_test/output_detected_text.txt'
    
    try:
        # Set Google Cloud credentials
        set_google_credentials(credentials_path)
        
        # Create the Vision client
        client = create_vision_client()
        
        # Load the image
        image_path = os.path.join(image_folder_path, file_name)
        image = load_image(image_path)
        
        # Detect text in the image
        detected_text = detect_text_in_image(client, image)
        print("Detected Text:", detected_text)
        
        # Write the detected text to a file
        write_text_to_file(detected_text, output_file_path)

        # Extract details from the raw text
        extracted_details = extract_details(detected_text)
        
        # Print the extracted details in JSON format
        print(json.dumps(extracted_details, indent=4))
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
