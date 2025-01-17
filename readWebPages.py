from bs4 import BeautifulSoup  # parses html and extracts data
import requests  
import re #as long as name remains consistent it can find it alone without 
        # having to implement a checkpoint for class html

# Set the URL for the "Stocks News" tab on Finviz
url = "https://finviz.com/news.ashx?v=3"

# headers so it doesnt get blocked when running
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # url I provided sends it straight to stock news so it just looks for news container class
    #this shouldnt change in the html but keep in mind it can change if any errors
    rows = soup.find_all("div", class_="news-badges-container")

    article_titles = []
    article_tickers = []
    article_links = []

    # go through each news article in the container
        #TODO
            #   This should probably be set to occur as often as possible if trading real time ?
            #   maybe too many requests and might get blocked though
            #   Check every 1-3 hours for the previous request top article and if it has moved down in the new 
            #   request title array a significant amount then get the links and tickers to process
            #   article sentiment to help evaluate stock performance
    for row in rows:        
        link_tag = row.find("a", class_=re.compile("nn-tab-link"))
        # ticker (<a> tag) that identifies the stock symbol
        ticker_tag = row.find("a", class_=re.compile("fv-label stock-news-label"))

        # only process the row if both a title link and ticker are found
        if link_tag and ticker_tag:
            title = link_tag.text.strip()
            ticker = ticker_tag.text.strip()
            link = link_tag["href"]

            article_titles.append(title)
            article_tickers.append(ticker)
            article_links.append(link)

    for title, ticker, link in zip(article_titles, article_tickers, article_links):
        print(f"Title: {title}")  # Print the article title
        print(f"Ticker: {ticker}")  # Print the stock ticker
        print(f"Link: {link}\n")  # Print the full link to the article

else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
