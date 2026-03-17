import base64
import os

import requests
from PIL import Image


def validate_image(image_path: str) -> bool:
    """
    Validate if an image file can be opened and is not corrupted.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        True if the image is valid and can be opened, False otherwise
    """
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify that it's a valid image
        # Re-open to check if it can be fully loaded (verify() may not catch all issues)
        with Image.open(image_path) as img:
            img.load()  # Force load the image data
        return True
    except Exception as e:
        print(f"Warning: Image '{image_path}' is invalid or corrupted: {e}")
        return False


def generate_image(
    prompt_file: str,
    reference_images: list[str],
    output_file: str,
    aspect_ratio: str = "16:9",
) -> str:
    with open(prompt_file, "r") as f:
        prompt = f.read()
    parts = []
    i = 0
    
    # Filter out invalid reference images
    valid_reference_images = []
    for ref_img in reference_images:
        if validate_image(ref_img):
            valid_reference_images.append(ref_img)
        else:
            print(f"Skipping invalid reference image: {ref_img}")
    
    if len(valid_reference_images) < len(reference_images):
        print(f"Note: {len(reference_images) - len(valid_reference_images)} reference image(s) were skipped due to validation failure.")
    
    for reference_image in valid_reference_images:
        i += 1
        with open(reference_image, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        parts.append(
            {
                "inlineData": {
                    "mimeType": "image/jpeg",
                    "data": image_b64,
                }
            }
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY is not set"
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent",
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "generationConfig": {"imageConfig": {"aspectRatio": aspect_ratio}},
            "contents": [{"parts": [*parts, {"text": prompt}]}],
        },
    )
    response.raise_for_status()
    json = response.json()
    parts: list[dict] = json["candidates"][0]["content"]["parts"]
    image_parts = [part for part in parts if part.get("inlineData", False)]
    if len(image_parts) == 1:
        base64_image = image_parts[0]["inlineData"]["data"]
        # Save the image to a file
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(base64_image))
        return f"Successfully generated image to {output_file}"
    else:
        raise Exception("Failed to generate image")

def generate_image_vertex(
    prompt_file: str,
    reference_images: list[str],
    output_file: str,
    aspect_ratio: str = "16:9",
) -> str:
    # 1. 환경 변수 확인 (Vertex AI용 API Key도 동일하게 사용 가능하지만,
    # 내부적으로는 PROJECT_ID와 LOCATION이 필수입니다)
    project = os.getenv("VERTEX_API_PROJECT_ID")
    location = os.getenv("VERTEX_API_LOCATION")

    # Validate required environment variables
    if not project or not location:
        raise Exception(
            "Missing required environment variables: VERTEX_API_PROJECT_ID and/or VERTEX_API_LOCATION. "
            "Please ensure these are set in your .env file."
        )

    with open(prompt_file, "r") as f:
        prompt = f.read()

    # 2. Get API key for authentication
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise Exception("GEMINI_API_KEY environment variable is not set")

    # Warning for reference images
    if reference_images and len(reference_images) > 0:
        print(f"Warning: {len(reference_images)} reference image(s) provided but will be ignored.")
        print("Vertex AI Imagen 3 does not support reference images via this interface.")

    # 3. Call Vertex AI Imagen API via REST
    # Endpoint format: https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google/models/imagen-3.0-generate-001:predict
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google/models/imagen-3.0-generate-001:predict"

    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "instances": [
            {
                "prompt": prompt
            }
        ],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": aspect_ratio
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    # 4. Extract and save generated image
    try:
        result = response.json()

        # Vertex AI Imagen returns predictions with bytesBase64Encoded
        if "predictions" in result and len(result["predictions"]) > 0:
            prediction = result["predictions"][0]

            # Try different possible keys for the image data
            img_base64 = None
            if "bytesBase64Encoded" in prediction:
                img_base64 = prediction["bytesBase64Encoded"]
            elif "image" in prediction and "bytesBase64Encoded" in prediction["image"]:
                img_base64 = prediction["image"]["bytesBase64Encoded"]
            else:
                raise Exception(f"Unexpected response format. Keys in prediction: {prediction.keys()}")

            # Decode and save
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(img_base64))
            return f"Successfully generated image to {output_file} (Vertex AI)"
        else:
            raise Exception(f"No predictions in response. Response keys: {result.keys()}")

    except (KeyError, IndexError) as e:
        raise Exception(f"Failed to extract image from response: {e}. Response: {result}")
    except Exception as e:
        raise Exception(f"Failed to generate/save image: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate images using Gemini API")
    parser.add_argument(
        "--prompt-file",
        required=True,
        help="Absolute path to JSON prompt file",
    )
    parser.add_argument(
        "--reference-images",
        nargs="*",
        default=[],
        help="Absolute paths to reference images (space-separated)",
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="Output path for generated image",
    )
    parser.add_argument(
        "--aspect-ratio",
        required=False,
        default="16:9",
        help="Aspect ratio of the generated image",
    )

    args = parser.parse_args()

    try:
        langchain_google_mode = os.getenv("LANGCHAIN_GOOGLE_MODE", "genai")
        if langchain_google_mode.lower() == "vertexai":
            print(f"Using Vertex AI mode (LANGCHAIN_GOOGLE_MODE={langchain_google_mode})")
            result = generate_image_vertex(
                args.prompt_file,
                args.reference_images,
                args.output_file,
                args.aspect_ratio,
            )
        else:
            print(f"Using Google AI Studio mode (LANGCHAIN_GOOGLE_MODE={langchain_google_mode})")
            result = generate_image(
                args.prompt_file,
                args.reference_images,
                args.output_file,
                args.aspect_ratio,
            )
        print(result)
    except Exception as e:
        print(f"Error while generating image: {e}")
