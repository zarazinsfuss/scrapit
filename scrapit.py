import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_asset(base_url, asset_url, output_folder):
    """Download an asset and return its local path."""
    asset_response = requests.get(urljoin(base_url, asset_url))
    asset_name = os.path.basename(asset_url)
    asset_path = os.path.join(output_folder, asset_name)
    with open(asset_path, 'wb') as asset_file:
        asset_file.write(asset_response.content)
    return asset_name

def download_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Download and adjust CSS links
    for link_tag in soup.find_all("link", rel="stylesheet"):
        css_url = link_tag["href"]
        if css_url.startswith(("http:", "https:", "//")):  # Avoid base64 or data URLs
            local_css_name = download_asset(url, css_url, output_dir)
            link_tag["href"] = local_css_name

    # Download and adjust JS links
    for script_tag in soup.find_all("script"):
        js_url = script_tag.get("src")
        if js_url and js_url.startswith(("http:", "https:", "//")):  # Avoid inline JS
            local_js_name = download_asset(url, js_url, output_dir)
            script_tag["src"] = local_js_name

    # Download images and adjust their sources
    for img_tag in soup.find_all("img"):
        img_url = img_tag["src"]
        if img_url.startswith(("http:", "https:", "//")):  # Avoid base64 or data URLs
            local_img_name = download_asset(url, img_url, os.path.join(output_dir, "images"))
            img_tag["src"] = os.path.join("images", local_img_name)

    # Save the adjusted HTML
    html_path = os.path.join(output_dir, "page.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

def print_help():
    help_message = """
Usage: python script_name.py <URL>

Arguments:
    URL: The target URL to scrape.

Description:
    This script scrapes the content of the provided URL and saves it in the 'output/' directory.
    """
    print(help_message)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ["--help", "-h"]:
        print_help()
        sys.exit(1)

    target_url = sys.argv[1]
    download_content(target_url)

