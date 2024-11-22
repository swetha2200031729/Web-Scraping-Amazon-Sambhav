from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests


def scrape_static_content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text and image URLs
        texts = " ".join([p.get_text() for p in soup.find_all("p")])
        images = [img["src"] for img in soup.find_all("img", src=True)]

        return {"texts": texts, "images": images}
    except Exception as e:
        raise ValueError(f"Error scraping URL: {e}")


@api_view(["POST"])
def scrape_and_generate(request):
    url = request.data.get("url")
    if not url:
        return Response({"error": "URL is required"}, status=400)

    try:
        # Scrape content
        scraped_data = scrape_static_content(url)
        texts = scraped_data["texts"]
        images = scraped_data["images"]

        # Generate a placeholder response since text generation is disabled
        generated_text = (
            "Text generation is disabled. This is a placeholder output."
        )

        return Response(
            {"texts": texts, "images": images, "generated_text": generated_text}
        )
    except Exception as e:
        return Response({"error": str(e)}, status=500)
