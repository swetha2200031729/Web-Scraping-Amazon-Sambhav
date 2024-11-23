import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline

# Initialize text generation pipeline
generator = pipeline("text-generation", model="gpt2")


def scrape_instagram_images(url):
    try:
        # Initialize Selenium WebDriver
        driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and accessible

        # Navigate to the Instagram post URL
        driver.get(url)
        driver.implicitly_wait(40)  # Adjust based on your internet speed

        # Create a directory to save images
        folder_name = "instagram_images"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Find all image elements on the page
        image_elements = driver.find_elements(By.TAG_NAME, 'img')

        # Extract and download image URLs
        images = []
        for idx, img in enumerate(image_elements):
            image_url = img.get_attribute('src')
            if image_url:
                images.append(image_url)
                try:
                    # Save the image locally
                    img_data = requests.get(image_url).content
                    img_name = os.path.join(folder_name, f"image_{idx+1}.jpg")
                    with open(img_name, 'wb') as file:
                        file.write(img_data)
                    print(f"Downloaded: {img_name}")
                except Exception as e:
                    print(f"Failed to download image {idx+1}: {e}")

        return {"images": images}
    except Exception as e:
        raise ValueError(f"Error scraping Instagram post: {e}")
    finally:
        driver.quit()


@api_view(["POST"])
def scrape_instagram_post(request):
    """
    Endpoint to scrape images from an Instagram post.
    """
    url = request.data.get("url")
    if not url:
        return Response({"error": "URL is required"}, status=400)

    try:
        # Scrape Instagram images
        scraped_data = scrape_instagram_images(url)
        images = scraped_data["images"]

        return Response({"images": images}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def scrape_and_generate(request):
    """
    Endpoint to scrape content and generate text using GPT-2.
    """
    url = request.data.get("url")
    if not url:
        return Response({"error": "URL is required"}, status=400)

    try:
        # Scrape Instagram images
        scraped_data = scrape_instagram_images(url)
        images = scraped_data["images"]

        # Generate placeholder text (or use extracted content for GPT-2 input)
        text_content = "Scraped Instagram post with images."
        generated_text = generator(
            text_content, max_length=150, num_return_sequences=1, truncation=True
        )[0]["generated_text"]

        return Response(
            {"images": images, "generated_text": generated_text}, status=200
        )
    except Exception as e:
        return Response({"error": str(e)}, status=500)
