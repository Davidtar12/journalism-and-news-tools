import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_first_image_from_webpage(url, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        image_divs = soup.find_all('div', class_=["col-lg-12", "row article-cover-image no-gutters"])

        for div in image_divs:
            if div.get('data-image-src'):
                img_url = div['data-image-src']
                break
            elif 'background' in div.get('style', ''):
                style = div['style']
                img_url = style.split("url('")[1].split("')")[0]
                break
        else:
            print(f"No suitable image found in {url}")
            return

        img_url = urljoin(url, img_url)
        try:
            img_data = requests.get(img_url, headers=headers).content
            img_name = os.path.basename(img_url.split("?")[0])
            save_path = os.path.join(save_dir, img_name)

            with open(save_path, 'wb') as file:
                file.write(img_data)
            print(f"Image downloaded: {save_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {img_url}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to load webpage {url}: {e}")

# Example usage
webpage_urls = [
    "https://news.mongabay.com/2024/05/ecuadors-los-lobos-narcotrafficking-gang-muscles-in-on-illegal-gold-mining/"
    
    
    
    
    # Add more URLs as needed
]
save_dir = r"C:\Users\david\Downloads"

for url in webpage_urls:
    download_first_image_from_webpage(url, save_dir),
    