import base64
import requests
def get_image(image_url: str):
    try:
        # Download the image file
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = response.content

        # Encode the image data to base64
        encoded_image = base64.b64encode(image_data).decode("utf-8")

        return {"image_data": encoded_image}
    except Exception as e:
        return {"error": str(e)}
    
image_url = "https://drive.google.com/uc?id=18VsFQTO7mUqQGHOoMhRxqOk1NNP7BIH8"

if __name__ == "__main__":
    print(get_image(image_url))

    