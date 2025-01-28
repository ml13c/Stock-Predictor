import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from datetime import timedelta


# data for top stocks(placeholders for now)
tickers = ["NVDA", "AAPL", "MSFT", "GOOGL"]
data = {}
for ticker in tickers:
    stock_data = yf.Ticker(ticker).history(period="max")
    stock_data = stock_data.loc["2008-01-01":]
    stock_data["Tomorrow"] = stock_data["Close"].shift(-1)
    stock_data["Target"] = (stock_data["Tomorrow"] > stock_data["Close"]).astype(int)
    stock_data.dropna(inplace=True)
    stock_data["Ticker"] = ticker
    data[ticker] = stock_data

df = pd.concat(data.values())

# definitions for data 
predictors = ["Close", "Volume", "Open", "High", "Low"]
model = RandomForestClassifier(n_estimators=300, min_samples_split=225, random_state=1)

# Splitting data to set where I want to start predicting
split_date = "2022-01-01"
train_data = df[df.index < split_date].copy()  # Use .copy() to avoid SettingWithCopyWarning
future_data = df[(df.index >= split_date) & (df["Ticker"] == "NVDA")].copy()  # Use .copy()

model.fit(train_data[predictors], train_data["Target"])

# Prediction
future_data.loc[:, "Predictions"] = model.predict(future_data[predictors])
future_data.loc[:, "Predicted Price"] = future_data["Close"].shift(1) * (1 + future_data["Predictions"] * 0.01)
last_actual_price = df[(df.index < split_date) & (df["Ticker"] == "NVDA")]["Close"].iloc[-1]
future_data.loc[future_data.index[0], "Predicted Price"] = last_actual_price

# actual NVDA data to today
today = datetime.today().strftime("%Y-%m-%d")
actual_data = yf.Ticker("NVDA").history(period="max").loc["2008-01-01":today]

# start date to evaluate accuracy (1 month after the split date)
evaluation_start_date = (pd.to_datetime(split_date) + timedelta(days=30)).strftime("%Y-%m-%d")

# Filter data
evaluation_data = combined_prices[combined_prices.index >= evaluation_start_date]

# accuracy within ±5 tolerance
tolerance = 5
evaluation_data["Difference"] = abs(evaluation_data["Predicted Price"] - evaluation_data["Actual Price"])
evaluation_data["Is Accurate"] = evaluation_data["Difference"] <= tolerance

# Caccuracy
accuracy = evaluation_data["Is Accurate"].mean() * 100
print(f"Accuracy within ±{tolerance} (starting from {evaluation_start_date}): {accuracy:.2f}%")

# Nan values(before split date) are filled with actual values
combined_prices["Predicted Price"] = combined_prices["Predicted Price"].fillna(combined_prices["Actual Price"])
combined_prices.to_csv("nvda_actual_vs_predicted_prices.csv")
# table
print(combined_prices.tail(20))  # Show the last 20 days

# Output
# Accuracy within ±5 (starting from 2022-01-31): 94.67%
# will show true accuracy (about 52%) in next commit with graphs
# csv table
