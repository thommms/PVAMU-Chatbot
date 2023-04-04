import requests
from bs4 import BeautifulSoup

# Define the URL of the website to scrape and the keyword to search for
url = "https://example.com/search"
keyword = "example keyword"

# Send a GET request to the search URL with the keyword as a query parameter
response = requests.get(url, params={"q": keyword})

# Parse the HTML content of the search results page using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the search result items on the page and print their titles and URLs
search_results = soup.find_all("div", {"class": "search-result"})
for result in search_results:
    title = result.find("h3").text
    url = result.find("a")["href"]
    print(f"Title: {title}\nURL: {url}\n")
