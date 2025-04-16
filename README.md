# Support Hero Scraper

A Python web scraper that extracts knowledge base articles from support website and converts them to Markdown files for offline reference and documentation.

## Overview

This tool automates the process of collecting support documentation from help center. It navigates through section pages, extracts article links, and then converts each article from HTML to clean Markdown format for easy reading and reference.

## Features

- Scrapes article links from main sections of the support website
- Extracts article content and converts HTML to Markdown format
- Saves articles as individual Markdown files with URL-based naming
- Headless browser operation for efficient scraping
- Built-in error handling and timeouts for reliable scraping

## Requirements

The scraper requires Python 3.6+ and the following dependencies:
- beautifulsoup4
- html2text
- selenium
- requests

All dependencies are listed in the `requirements.txt` file.

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install a compatible ChromeDriver for Selenium

## Usage

1. Edit the `main_sections` list in `scraper.py` to include the URLs of the main support sections you want to scrape
2. Run the script:
   ```bash
   python scraper.py
   ```
3. The script will save all articles in the `articles` directory

## Article Structure

Each article is saved as a separate Markdown file. The filename is derived from the last part of the article's URL path. For example, an article at `https://support.example.com/articles/100188-auth-guide` would be saved as `100188-auth-guide.md`.

## Customization

You can customize the scraper behavior by modifying:
- The `main_sections` list to target different areas of the website
- The HTML selector patterns in the script if the website structure changes
- The HTML to Markdown conversion options through the `html2text` configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.