# Stock-Predictor
Trained AI model and used webscraping to help predict stock price
breakdown plan of stock project
    -sentimental analysis for real world news/speculation on a certain stock
        -classify as stock type and see world news that could impact stock type in real time
        -use google to look up stock news over any big things in the past 3-5 years and other potential things within recent year
            -any possible reveals or announcements
            -twitter pages for speculation and reputation (wont be as heavy in deciding price prediction unless credible source)

NOT YET COMBINED/FINISHED

                ##
                GENERAL-look up stock-->send to gpt classifier-->classify as a stock type-->look up in google stock type related news-->send data to gpt to summarize-->parse and prepare data
                    -->(or just) send to gpt to analyze data-->set articles into table that gives a score--> determine table value based off of overall pos and neg scores
                SPECIFIC-look up stock news-->send to gpt-->send to gpt to summarize-->parse data/gpt analzye-->set data into table for score-->determine table value-->
                --(at same time)look at stock history-->compare to overall S&P 500 stock trends and history-->
                
                ##
    -past historical data using big stock like S&P 500 for market trends to base off of
    -past historical data of stock
    -real time indicators for price trends
    
    -graph it out in color of real data and predicted data and look at training growth from there




    use biztoc
    extract text from this and send to analyze
    maybe use twitter too
    use scores to help determine market for certain stock in future and present
    use past data to help determine trends
    need data for other competing/affecting tickers as that influences things a lot
    read every news article and given article name give score of relevancy to stock and if it wil affect it or not
