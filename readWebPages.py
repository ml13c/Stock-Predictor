from bs4 import BeautifulSoup  # Import the library to parse HTML and extract data
import requests  # Import the library to make HTTP requests

# Set the URL for the "Stocks News" tab on Finviz
url = "https://finviz.com/news.ashx?v=3"

# Define headers to make the request look like it’s coming from a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

# Send a GET request to fetch the page's HTML content
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML response with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all containers that hold news badges; this helps locate individual articles
    rows = soup.find_all("div", class_="news-badges-container")

    # Initialize lists to store the titles, tickers, and links we extract
    article_titles = []
    article_tickers = []
    article_links = []

    # Loop through each container (representing one article)
    for row in rows:
        # Extract the link (<a> tag) that holds the article title
        
        # <td class="news_link-cell">
        #                 <div class="news-badges-container">
        #                     <a href="https://www.prnewswire.com/news-releases/mark-arnold-appointed-as-next-president-of-rasmussen-university-302353770.html" onclick="trackAndOpenNews(event, 'PR Newswire', 'https://www.prnewswire.com/news-releases/mark-arnold-appointed-as-next-president-of-rasmussen-university-302353770.html')" target="_blank" class="nn-tab-link" rel="nofollow">Mark Arnold Appointed as Next President of Rasmussen University</a>
        #                      <a href="quote.ashx?t=APEI" data-boxover="cssbody=[hoverchart] cssheader=[tabchrthdr] body=[<img src='https://charts2-node.finviz.com/chart.ashx?cs=m&amp;t=APEI&amp;tf=d&amp;s=linear&amp;ct=candle_stick&amp;tm=d' srcset='https://charts2-node.finviz.com/chart.ashx?cs=m&amp;t=APEI&amp;tf=d&amp;s=linear&amp;ct=candle_stick&amp;tm=d 1x, https://charts2-node.finviz.com/chart.ashx?cs=m&amp;t=APEI&amp;tf=d&amp;s=linear&amp;ct=candle_stick&amp;tm=d&amp;sf=2 2x' width='324' height='180' alt='' referrerPolicy='no-referrer-when-downgrade' loading='lazy'><div><b>American Public Education Inc</b>Education &amp; Training Services <span>•</span> USA <span>•</span> 379.93M </div>] offsetx=[80] offsety=[30] delay=[250]" class="fv-label stock-news-label is-opaque is-positive-50"><span class="select-none font-semibold">APEI</span></a>
        #                     <span class="news_date-cell color-text is-muted text-right">PR Newswire</span>
        #                 </div>
        #             </td>
        
        link_tag = row.find("a", class_="nn-tab-link")
        # Extract the ticker (<a> tag) that identifies the stock symbol
        ticker_tag = row.find("a", class_="fv-label stock-news-label is-opaque is-positive-50")

        # Only process the row if both a title link and ticker are found
        if link_tag and ticker_tag:
            # Extract and clean the article title from the link tag
            title = link_tag.text.strip()
            # Extract and clean the stock ticker text
            ticker = ticker_tag.text.strip()
            # Build the full URL for the article by appending the relative link to the base URL
            link = "https://finviz.com" + link_tag["href"]

            # Add the extracted data to their respective lists
            article_titles.append(title)
            article_tickers.append(ticker)
            article_links.append(link)

    # Combine the extracted data and print them neatly
    for title, ticker, link in zip(article_titles, article_tickers, article_links):
        print(f"Title: {title}")  # Print the article title
        print(f"Ticker: {ticker}")  # Print the stock ticker
        print(f"Link: {link}\n")  # Print the full link to the article

else:
    # If the request fails, print the HTTP status code for debugging
    print(f"Failed to fetch the page. Status code: {response.status_code}")
