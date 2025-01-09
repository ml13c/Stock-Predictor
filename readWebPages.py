from bs4 import BeautifulSoup
import requests

url = "https://finviz.com/news.ashx?v=3"

# Define headers to make the request look like it’s coming from a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}


response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # parse html
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all containers that hold news badges/locate individual articles
    rows = soup.find_all("div", class_="news-badges-container")

    article_titles = []
    article_tickers = []
    article_links = []

    # Loop through each container/article
    for row in rows:
        # <a> tag holds the article title
        link_tag = row.find("a", class_="nn-tab-link")
        # <a> tag identifies the stock symbol
        ticker_tag = row.find("a", class_="fv-label stock-news-label is-opaque is-neutral")

        # only process if both a title link and ticker are found
        if link_tag and ticker_tag:
            # article title from the link tag
            title = link_tag.text.strip()
            # stock ticker text
            ticker = ticker_tag.text.strip()
            # Build full URL for the article
            link = "https://finviz.com" + link_tag["href"]

            article_titles.append(title)
            article_tickers.append(ticker)
            article_links.append(link)

    for title, ticker, link in zip(article_titles, article_tickers, article_links):
        print(f"Title: {title}")  # Print the article title
        print(f"Ticker: {ticker}")  # Print the stock ticker
        print(f"Link: {link}\n")  # Print the full link to the article

else:
    # If the request fails, print the HTTP status code for debugging
    print(f"Failed to fetch the page. Status code: {response.status_code}")
