import pandas as pd

#---
#format dataset
df = pd.read_csv("shiller_data.csv")
df["date"] = df["date"].astype(str)

new_dates = []
for date in list(df["date"]):
	year = date.split(".")[0]
	month = date.split(".")[1]
	if month == "1":
		month = "10"
	new_date = year + "-" + month + "-15"
	new_dates.append(new_date)
df["date"] = new_dates
df["date"] = pd.to_datetime(df["date"], format = "%Y-%m-%d")

df = df[df["date"] <= "2022-01-15"].reset_index(drop = True)
#---

#---
#adjust prices for dividend reinvestment
dividend_prices = []
for i, row in enumerate(df.itertuples()):
	if row.date == df.iloc[0].date:
		price = row.price
		dividend_prices.append(price)
	elif row.date == df.iloc[1].date:
		dividend = row.dividend/12
		current_price = row.price
		dividend_prices.append(current_price+dividend)
		shares = ((dividend_prices[i]/current_price))
	else:
		dividend = row.dividend/12
		previous_price = df.iloc[i-1].price
		current_price = row.price
		dividend_prices.append((shares*dividend)+(shares*(current_price/previous_price)*previous_price))
		shares = ((dividend_prices[i]/current_price))
df["dividend_price"] = dividend_prices
#---

#---
#variables
earnings = 12000
dca_frequency = 12
time_period = 120

start_dates = []
end_dates = []
lump_returns = []
dca_returns = []
#---

#gather historical LS/DCA performance
#---
for row in df.itertuples():

	if (((str((int(str(row.date)[:4])+time_period))) + str(row.date)[4:]))[:10] in list(df["date"].astype(str)):

		date_forward_frequency = ((str((int(str(row.date)[:4])+int(dca_frequency/12)))) + str(row.date)[4:])
		date_forward_time_period = ((str((int(str(row.date)[:4])+time_period))) + str(row.date)[4:])

		filteredDf = df[(df["date"] >= str(row.date)) & ((df["date"] < date_forward_frequency) | (df["date"] == date_forward_time_period))].reset_index(drop = True)

		start_dates.append(str(row.date))
		end_dates.append(date_forward_time_period)

		#---
		#lump sum investing
		inv_return = filteredDf.iloc[len(filteredDf)-1].dividend_price/filteredDf.iloc[0].dividend_price
		lump_returns.append(inv_return)
		#---

		#---
		#dollar cost averaging
		purchase_shares = []
		for i, row in enumerate(filteredDf.itertuples()):
			if i != len(filteredDf)-1:
				shares = earnings/dca_frequency/row.dividend_price
				purchase_shares.append(shares)

		inv_return = (filteredDf.iloc[len(filteredDf)-1].dividend_price * sum(purchase_shares))/earnings
		dca_returns.append(inv_return)
		#---
#---

#---
#synthesize historical results
returnDf = pd.DataFrame()
returnDf["start"] = start_dates
returnDf["start"] = pd.to_datetime(returnDf["start"])
returnDf["end"] = end_dates
returnDf["end"] = pd.to_datetime(returnDf["end"])
returnDf["lump"] = lump_returns
returnDf["dca"] = dca_returns
#---

#---
#percent of times each strategy outperformed the other
percent_times_lump_outperformed = (len(returnDf[returnDf["lump"] > returnDf["dca"]])/len(returnDf)) * 100
percent_times_dca_outperformed = (len(returnDf[returnDf["dca"] > returnDf["lump"]])/len(returnDf)) * 100
#---

#---
#average total returns and compounded annual growth rates
avg_lump_return = float(returnDf["lump"].sum())/len(returnDf)
avg_lump_cagr = avg_lump_return**(1/time_period)
avg_dca_return = float(returnDf["dca"].sum())/len(returnDf)
avg_dca_cagr = avg_dca_return**(1/time_period)
#---
