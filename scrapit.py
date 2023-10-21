import os
import sys
import requests
from bs4 import BeautifulSoup
from git import Repo

def download_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Save the main HTML
    html_path = os.path.join(output_dir, "page.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    # Download images
    img_folder = os.path.join(output_dir, "images")
    os.makedirs(img_folder, exist_ok=True)
    for img_tag in soup.find_all("img"):
        img_url = img_tag["src"]
        img_name = os.path.basename(img_url)
        img_path = os.path.join(img_folder, img_name)
        with open(img_path, "wb") as img_file:
            img_file.write(requests.get(img_url).content)

def upload_to_git():
    REPO_DIR = os.getcwd()  # Assuming the script is run from the repo directory
    repo = Repo.init(REPO_DIR)

    # Add all files in the output directory to the repo
    repo.git.add("output/*")

    # Commit the changes
    repo.git.commit("-m", "Add scraped content")

    # Push to remote (assuming you've set up a remote named 'origin')
    repo.git.push("origin", "master")

def print_help():
    help_message = """
Usage: python script_name.py <URL>

Arguments:
    URL: The target URL to scrape.

Description:
    This script scrapes the content of the provided URL and saves it in the 'output/' directory.
    It then commits and pushes the changes to a Git repository.
    """
    print(help_message)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ["--help", "-h"]:
        print_help()
        sys.exit(1)

    target_url = sys.argv[1]
    download_content(target_url)
    upload_to_git()

