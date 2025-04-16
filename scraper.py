import os
import re
import html2text
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def scrape_and_save_articles(urls, folder='articles'):
    # Setup headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # HTML to Markdown converter
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.body_width = 0

    for url in urls:
        print(f"Scraping content from {url}")
        driver.get(url)

        try:
            # Wait until the article title has text (max 60 seconds)
            WebDriverWait(driver, 60).until(
                lambda d: d.find_element(By.CSS_SELECTOR, '.article-title').text.strip()
            )
        except:
            print(f"Timeout waiting for article title on {url}")
            continue

        try:
            # Now grab the main article content
            article_div = driver.find_element(By.CSS_SELECTOR, 'div.article.row.container.container-padding')
            html_content = article_div.get_attribute('innerHTML')

            # Convert HTML to Markdown
            markdown_content = converter.handle(html_content)

            # Create filename from last part of URL
            path = urlparse(url).path
            slug = path.rstrip('/').split('/')[-1] or 'index'
            slug = re.sub(r'[^\w\-]', '_', slug)  # sanitize
            file_path = os.path.join(folder, f"{slug}.md")

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            print(f"Saved article to {file_path}")

        except Exception as e:
            print(f"Error scraping content from {url}: {e}")

    driver.quit()

def scrape_article_links(urls):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    all_links = []
    
    for url in urls:
        print(f"Scraping {url}...")
        driver.get(url)

        try:
            # Wait up to 60 seconds for at least one <a> inside <ul.article-list>
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.article-list a'))
            )
        except:
            print(f"Timeout: No <a> inside .article-list found on {url}")
            continue

        # Now collect all <a> elements inside the ul.article-list
        article_list = driver.find_element(By.CSS_SELECTOR, 'ul.article-list')
        a_tags = article_list.find_elements(By.TAG_NAME, 'a')
        page_links = [a.get_attribute('href') for a in a_tags if a.get_attribute('href')]

        print(f"Found {len(page_links)} links")
        all_links.extend(page_links)

    driver.quit()
    
    return all_links


# Main sections to scrape
main_sections = []

scrape_and_save_articles(scrape_article_links(scrape_article_links(main_sections)))
