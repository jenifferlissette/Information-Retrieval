import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
import multiprocessing as mp

def fetch_html_content(url, headers, timeout=10):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        return BeautifulSoup(response.text, "html.parser")
    except requests.Timeout:
        print(f"Timeout occurred for URL: {url}")
    except requests.RequestException as e:
        print(f"Request failed for URL: {url} with exception: {e}")
    return None

def extract_links(url_elements):
    all_links = []
    for link_item in url_elements.find_all("li", class_="comp mntl-link-list__item"):
        anchor_tag = link_item.find("a", href=True)
        if anchor_tag:
            all_links.append(anchor_tag['href'])
    return all_links

def get_links_from_page(page_elements):
    all_links = []
    for link_item in page_elements.find_all("a", class_="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image"):
        if link_item.has_attr('href'):
            all_links.append(link_item['href'])
    return all_links

def get_title(soup):
    return soup.find("title").text if soup else np.nan

def get_recipe_description(soup):
    description = soup.find("p", class_="article-subheading type--dog")
    return description.text if description else np.nan

def get_recipe_ingredients(soup):
    if not soup:
        return np.nan
    ingredient_text = ''
    for item in soup.find_all("li", class_="mm-recipes-structured-ingredients__list-item"):
        ingredient_text += item.text.strip() + '\n'
    return ingredient_text

def get_recipe_steps(soup):
    if not soup:
        return np.nan
    step_text = ''
    for step_item in soup.find_all("li", class_="comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--LI"):
        for tag in step_item.find_all(["figure", "div"]):
            tag.decompose()
        step_text += step_item.text.strip() + '\n'
    return step_text

def process_recipe(args):
    url, headers = args
    soup = fetch_html_content(url, headers)
    return {
        'Title': get_title(soup),
        'Description': get_recipe_description(soup),
        'Ingredients': get_recipe_ingredients(soup),
        'Steps': get_recipe_steps(soup)
    }

if __name__ == "__main__":
    headers = {
        "User-Agent": "My App"
    }

    # Read the initial HTML file
    with open(r"C:\Users\VELA\Desktop\Recuperacion\Information-Retrieval\webScraping\data\Allrecipes_RecipesA-Z.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Extract initial links
    links_html = extract_links(soup)

    # Fetch HTML content for initial links
    with mp.Pool(processes=mp.cpu_count()) as pool:
        recipe_links = list(tqdm(pool.starmap(fetch_html_content, [(url, headers) for url in links_html]), total=len(links_html), desc="Fetching initial links"))

    # Get links from each recipe page
    links_per_recipe_page = [get_links_from_page(link) for link in recipe_links if link]

    # Combine all links
    all_links = [link for links_in_page in links_per_recipe_page for link in links_in_page]

    print(f"Total recipes to process: {len(all_links)}")

    # Process all recipes in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_recipe, [(url, headers) for url in all_links]), total=len(all_links), desc="Processing recipes"))

    # Create DataFrame
    recipe_df = pd.DataFrame(results)

    # Save to CSV
    recipe_df.to_csv('AllRecipes.csv', index=True)
    print("Data saved to AllRecipes.csv")