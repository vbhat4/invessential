import pandas as pd
import datetime
import radar
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np

#variables
earnings = 100
number_of_simulations = 10000
simulation_period = 20

#format dataset
df = pd.read_csv("1789_SP500.csv")
df.columns = ["date", "open", "high", "low", "close", "volume"]
df = df.sort_values(by = ["date"]).reset_index(drop = True)
df["date"] = pd.to_datetime(df["date"])

#---
#other
pd.options.mode.chained_assignment = None
plt.rcParams["font.family"] = "Avenir"

price_today = df.iloc[len(df) - 1]["close"]
date_list = list(df["date"])

start_dates = []
end_dates = []
open_gains = []
close_gains = []
changes_in_price = []
#---

#---
#run simulations
for i in range(number_of_simulations):

	#---
	#filter to a random time period of specified duration
	start_date = pd.to_datetime(radar.random_datetime(start = datetime.datetime(year = 1928, month = 10, day = 1), stop = datetime.datetime(year = 2002, month = 9, day = 16)).date())
	while start_date not in date_list:
		start_date = pd.to_datetime(radar.random_datetime(start = datetime.datetime(year = 1928, month = 10, day = 1), stop = datetime.datetime(year = 2002, month = 9, day = 16)).date())
	start_dates.append(start_date)

	try:
		end_date = start_date.replace(year = start_date.year + simulation_period)
	except ValueError:
		end_date = start_date + (date(start_date.year + simulation_period, 1, 1) - date(start_date.year, 1, 1))
	for i in range(10):
		if end_date in date_list:
			break
		else:
			end_date = end_date + datetime.timedelta(days = 1)
	end_date = pd.to_datetime(end_date)
	end_dates.append(end_date)

	filteredDf = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
	#---

	#---
	#buying at open
	total_earned = 0
	purchase_shares = []
	for row in filteredDf.itertuples():
		shares = earnings/row.open
		total_earned += earnings
		purchase_shares.append(shares)

	total_now = 0
	for shares in purchase_shares:
		amount_now = price_today * shares
		total_now += amount_now

	gain = ((total_now/total_earned) - 1) * 100
	open_gains.append(gain)
	#---

	#---
	#buying at close
	total_earned = 0
	purchase_shares = []
	for row in filteredDf.itertuples():
		shares = earnings/row.close
		total_earned += earnings
		purchase_shares.append(shares)

	total_now = 0
	for shares in purchase_shares:
		amount_now = price_today * shares
		total_now += amount_now

	gain = ((total_now/total_earned) - 1) * 100
	close_gains.append(gain)
	#---

	#---
	#change in price
	start_price = list(df[df["date"] == start_date]["close"])[0]
	end_price = list(df[df["date"] == end_date]["close"])[0]
	change_in_price = ((end_price / start_price) - 1) * 100
	changes_in_price.append(change_in_price)
	#---
#---

#synthesize simulation results
gainDf = pd.DataFrame()
gainDf["start"] = start_dates
gainDf["end"] = end_dates
gainDf["open"] = open_gains
gainDf["close"] = close_gains
gainDf["change"] = changes_in_price

#percent of times each strategy outperformed the other
percent_times_open_outperformed = len(gainDf[gainDf["open"] > gainDf["close"]]) * 100
percent_times_close_outperformed = len(gainDf[gainDf["close"] > gainDf["open"]]) * 100

#create stats on relative performance of buying at open
openDf = gainDf[gainDf["open"] > gainDf["close"]].reset_index(drop = True)
openDf["difference"] = openDf["open"] - openDf["close"]
avg_percent_difference = openDf["difference"].sum()/len(openDf)
avg_cagr_difference = ((avg_percent_difference / 100) + 1) ** (1 / simulation_period)

#create stats on relative performance of buying at close
closeDf = gainDf[gainDf["close"] > gainDf["open"]].reset_index(drop = True)
closeDf["difference"] = closeDf["close"] - closeDf["open"]
avg_percent_difference = closeDf["difference"].sum()/len(closeDf)
avg_cagr_difference = ((avg_percent_difference / 100) + 1) ** (1 / simulation_period)

#---
#plot start years of buying at open simulations
start_years = []
for start_date in list(openDf["start"]):
	start_years.append(str(start_date)[:4])
openDf["start_year"] = start_years
openDf["count"] = 1

for year in range(1928, 2003):
	if str(year) not in list(openDf["start_year"]):
		openDf.loc[len(openDf)] = [pd.to_datetime(f"{year}-01-01"), pd.to_datetime(f"{year}-01-01"), 0.00, 0.00, 0.00, 0.00, str(year), 0]

openDf = openDf.sort_values(by = ["start"]).reset_index(drop = True)

plt.figure(figsize=(12,4))
plt.subplots_adjust(bottom = 0.2)
plt.title("Starting Years of 20 Year Simulations When Buying at Open Outperforms", fontsize = 13, pad = 15, loc = "left")
ax = sns.barplot(x = "start_year", y = "count", data = openDf, estimator = sum, ci = None, color = "salmon")
plt.xlabel("Start Year", fontsize = 11)
plt.ylabel("Number of Simulations", fontsize = 11)
ax.xaxis.labelpad = 15
ax.yaxis.labelpad = 15
ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
plt.tight_layout()
plt.savefig("start_years_open_simul.jpg", dpi = 330)
#---

#---
#plot average outperformance of buying at open simulations
start_years = []
for start_date in list(openDf["start"]):
	start_years.append(str(start_date)[:4])
openDf["start_year"] = start_years
openDf["difference"] = openDf["difference"] / 100

for year in range(1928, 2003):
	if str(year) not in list(openDf["start_year"]):
		openDf.loc[len(openDf)] = [pd.to_datetime(f"{year}-01-01"), pd.to_datetime(f"{year}-01-01"), 0.00, 0.00, 0.00, 0.00, str(year)]

openDf = openDf.sort_values(by = ["start"]).reset_index(drop = True)

plt.figure(figsize=(12,4))
plt.subplots_adjust(bottom = 0.2)
plt.title("Average Outperformance of 20 Year Simulations When Buying at Open Outperforms", fontsize = 13, pad = 15, loc = "left")
ax = sns.barplot(x = "start_year", y = "difference", data = openDf, estimator = np.mean, ci = None, color = "yellowgreen")
plt.xlabel("Start Year", fontsize = 11)
plt.ylabel("Average Outperformance", fontsize = 11)
ax.xaxis.labelpad = 15
ax.yaxis.labelpad = 15
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1, decimals = 1, symbol = "%", is_latex = False))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
plt.tight_layout()
plt.savefig("avg_outperf_open_simul.jpg", dpi = 330)
#---

#---
#plot start years of buying at close simulations
start_years = []
for start_date in list(closeDf["start"]):
	start_years.append(str(start_date)[:4])
closeDf["start_year"] = start_years
closeDf["count"] = 1

for year in range(1928, 2003):
	if str(year) not in list(closeDf["start_year"]):
		closeDf.loc[len(closeDf)] = [pd.to_datetime(f"{year}-01-01"), pd.to_datetime(f"{year}-01-01"), 0.00, 0.00, 0.00, 0.00, str(year), 0]

closeDf = closeDf.sort_values(by = ["start"]).reset_index(drop = True)

plt.figure(figsize=(12,4))
plt.subplots_adjust(bottom = 0.2)
plt.title("Starting Years of 20 Year Simulations When Buying at Close Outperforms", fontsize = 13, pad = 15, loc = "left")
ax = sns.barplot(x = "start_year", y = "count", data = closeDf, estimator = sum, ci = None, color = "salmon")
plt.xlabel("Start Year", fontsize = 11)
plt.ylabel("Number of Simulations", fontsize = 11)
ax.xaxis.labelpad = 15
ax.yaxis.labelpad = 15
ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
plt.tight_layout()
plt.savefig("start_years_close_simul.jpg", dpi = 330)
#---

#---
#plot average outperformance of buying at close simulations
start_years = []
for start_date in list(closeDf["start"]):
	start_years.append(str(start_date)[:4])
closeDf["start_year"] = start_years
closeDf["difference"] = closeDf["difference"] / 100

for year in range(1928, 2003):
	if str(year) not in list(closeDf["start_year"]):
		closeDf.loc[len(closeDf)] = [pd.to_datetime(f"{year}-01-01"), pd.to_datetime(f"{year}-01-01"), 0.00, 0.00, 0.00, 0.00, str(year)]

closeDf = closeDf.sort_values(by = ["start"]).reset_index(drop = True)

plt.figure(figsize=(12,4))
plt.subplots_adjust(bottom = 0.2)
plt.title("Average Outperformance of 20 Year Simulations When Buying at Close Outperforms", fontsize = 13, pad = 15, loc = "left")
ax = sns.barplot(x = "start_year", y = "difference", data = closeDf, estimator = np.mean, ci = None, color = "yellowgreen")
plt.xlabel("Start Year", fontsize = 11)
plt.ylabel("Average Outperformance", fontsize = 11)
ax.xaxis.labelpad = 15
ax.yaxis.labelpad = 15
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1, decimals = 1, symbol = "%", is_latex = False))
ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
plt.tight_layout()
plt.savefig("avg_outperf_close_simul.jpg", dpi = 330)
#---
