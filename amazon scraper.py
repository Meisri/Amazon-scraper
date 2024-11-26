import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get product title
def get_title(soup):
    try:
        title = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
        return title
    except AttributeError:
        return "Title not available"

# Function to get product price
def get_price(soup):
    try:
        price = soup.find("span", {"class": "a-price-whole"}).get_text(strip=True)
        return price
    except AttributeError:
        return "Price not available"

# Function to get product rating
def get_rating(soup):
    try:
        rating = soup.find("span", {"class": "a-icon-alt"}).get_text(strip=True)
        return rating
    except AttributeError:
        return "Rating not available"

# Function to get product review count
def get_review_count(soup):
    try:
        review_count = soup.find("span", {"id": "acrCustomerReviewText"}).get_text(strip=True)
        return review_count
    except AttributeError:
        return "Review count not available"

# Function to get product availability
def get_availability(soup):
    try:
        availability = soup.find("div", {"id": "availability"}).find("span").get_text(strip=True)
        return availability
    except AttributeError:
        return "Availability not available"

# Function to scrape a product page
def scrape_product(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    # Send HTTP request
    webpage = requests.get(URL, headers=headers)
    
    # Check if the request was successful
    if webpage.status_code != 200:
        return ["Failed to retrieve page", "N/A", "N/A", "N/A", "N/A"]

    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(webpage.content, "lxml")
    
    # Extract product information
    product_title = get_title(soup)
    product_price = get_price(soup)
    product_rating = get_rating(soup)
    product_review_count = get_review_count(soup)
    product_availability = get_availability(soup)

    # Return the product details
    return [product_title, product_price, product_rating, product_review_count, product_availability]

# Main script
if __name__ == "__main__":

    # List of URLs to scrape
    urls = [
        "https://www.amazon.in/Taraash-Sterling-Silver-Initial-Pendant/dp/B085D8MH9L/",
        "https://www.amazon.in/Taraash-Sterling-Silver-Initial-Pendant/dp/B01NBZBVRW/",
        "https://www.amazon.in/Taraash-Sterling-Silver-Initial-Pendant/dp/B01N38MYDS/",
        "https://www.amazon.in/Taraash-Sterling-Silver-Initial-Pendant/dp/B01NBZHI2O/"
    ]

    # Create an empty list to store product data
data = []

    # Loop over each URL and scrape product details
for url in urls:
        product_data = scrape_product(url)
        data.append(product_data)  # Append each product's data to the list

    # Create a DataFrame using the collected data
df = pd.DataFrame(data, columns=["Title", "Price", "Rating", "Review Count", "Availability"])

    # Save the data to a CSV file
df.to_csv("amazon_products.csv", index=False)
print("Data saved to amazon_products.csv")