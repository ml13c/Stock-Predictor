from bs4 import BeautifulSoup
import requests

# Fetch the page content with headers
url = "https://finviz.com/news.ashx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # print each article title by row
    rows = soup.find_all("tr", class_="styled-row is-hoverable is-bordered is-rounded is-border-top is-hover-borders has-color-text news_table-row")
    article_titles = []
    article_tickers =[]
    for row in rows:
        link = row.find("a", class_="nn-tab-link")        
        if link:
            article_titles.append(link.text.strip())

tickerLookup = "NVDA"#desired ticker or stocks
article_tickers =[]

#print out each article title
for title in article_titles:
    print(title)
  #  for tag in ticker_tags:
      #  print(ticker)
    print()


else:
    print(f"he wroih")

