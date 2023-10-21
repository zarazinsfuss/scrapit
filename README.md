# scrapit - Simple web scraper script

scrapit is a simple Python script designed to scrape content from a provided URL and save it in an output/ directory. After scraping, it commits and pushes the content to a Git repository.

## Installation

Clone this repository:

```
git clone https://github.com/your_username/scrapit.git
```

Navigate to the cloned directory:

```
cd scrapit
```

Install the required Python packages:

```
pip install -r requirements.txt
```

## Usage

To scrape a webpage:

```
python scrapit.py <URL>
```

Replace <URL> with the target webpage you want to scrape.

## Forking and Renaming

If you wish to use this script for your own purposes and perhaps target a specific webpage regularly:

1. Fork this repository.
2. Rename the forked repository to match the name of your target webpage or any other name you prefer.
3. Clone your forked and renamed repository to your local machine.
4. Follow the installation steps above.
5. Don't forget to take out the `output/` from the `.gitignore` so that your scrapped web page is being commited.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
