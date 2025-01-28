import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

# placeholder stocks
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

# predictors
predictors = ["Close", "Volume", "Open", "High", "Low"]
model = RandomForestClassifier(n_estimators=300, min_samples_split=225, random_state=1)

# splitting data
split_date = "2022-01-01"
train_data = df[df.index < split_date].copy()  # Use .copy() to avoid SettingWithCopyWarning
future_data = df[(df.index >= split_date) & (df["Ticker"] == "NVDA")].copy()  # Use .copy()


model.fit(train_data[predictors], train_data["Target"])

# predicting
future_data.loc[:, "Predictions"] = model.predict(future_data[predictors])
future_data.loc[:, "Predicted Price"] = future_data["Close"].shift(1) * (1 + future_data["Predictions"] * 0.01)
last_actual_price = df[(df.index < split_date) & (df["Ticker"] == "NVDA")]["Close"].iloc[-1]
future_data.loc[future_data.index[0], "Predicted Price"] = last_actual_price

today = datetime.today().strftime("%Y-%m-%d")
actual_data = yf.Ticker("NVDA").history(period="max").loc["2008-01-01":today]

combined_prices = pd.concat([
    actual_data[["Close"]].rename(columns={"Close": "Actual Price"}),
    future_data[["Predicted Price"]]
], axis=1)

# all values that arent predicted(before split) are set to actual price
combined_prices["Predicted Price"] = combined_prices["Predicted Price"].fillna(combined_prices["Actual Price"])

# start evaluating 1 month after model starts predicting
evaluation_start_date = (pd.to_datetime(split_date) + timedelta(days=30)).strftime("%Y-%m-%d")

# only include dates after the evaluation start date for accuracy score
evaluation_data = combined_prices[combined_prices.index >= evaluation_start_date].copy()  # Use .copy()

# Calculate accuracy within ±5 tolerance
tolerance = 5
evaluation_data.loc[:, "Difference"] = abs(evaluation_data["Predicted Price"] - evaluation_data["Actual Price"])
evaluation_data.loc[:, "Is Accurate"] = evaluation_data["Difference"] <= tolerance
accuracy = evaluation_data["Is Accurate"].mean() * 100
print(f"Accuracy within ±{tolerance} (starting from {evaluation_start_date}): {accuracy:.2f}%")

# Save the table to a CSV file
evaluation_data.to_csv("nvda_actual_vs_predicted_prices_evaluation.csv")

print(evaluation_data.tail(20))  # last 20 rows to see if worked
