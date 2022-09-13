import pandas as pd
import plotly.express as px

#symbols to plot
tickers = ["NUSI", "NDX", "QYLD", "QRMI", "QCLR", "JEPI", "FTHI", "PBP"]

#initialize dataframes
janjul = pd.DataFrame()
julaug = pd.DataFrame()

#---
#for the january to july period
for ticker in tickers:

	#import year to date OHLC for each symbol
	df = pd.read_csv(f"{ticker}_YTD.csv")
	df = df.sort_values(by = ["Date"]).reset_index(drop = True)
	df["Date"] = pd.to_datetime(df["Date"])

	df = df[(df["Date"] >= "2022-01-03") & (df["Date"] <= "2022-07-01")]

	#add a date column
	if tickers.index(ticker) == 0:
		janjul["date"] = df["Date"]

	#compute year to date drawdowns
	starting_price = list(df["Close/Last"])[0]
	percent_changes = []
	for price in list(df["Close/Last"]):
		percent_change = ((1 - (price / starting_price)) * -1)
		percent_changes.append(percent_change)
	janjul[f"{ticker}"] = percent_changes
#---

#---
#for the july to august period
for ticker in tickers:

	#import year to date OHLC for each symbol
	df = pd.read_csv(f"{ticker}_YTD.csv")
	df = df.sort_values(by = ["Date"]).reset_index(drop = True)
	df["Date"] = pd.to_datetime(df["Date"])

	df = df[(df["Date"] >= "2022-07-01") & (df["Date"] <= "2022-08-19")]

	#add a date column
	if tickers.index(ticker) == 0:
		julaug["date"] = df["Date"]

	#compute year to date drawdowns
	starting_price = list(df["Close/Last"])[0]
	percent_changes = []
	for price in list(df["Close/Last"]):
		percent_change = ((1 - (price / starting_price)) * -1)
		percent_changes.append(percent_change)
	julaug[f"{ticker}"] = percent_changes
#---

#---
#for the january to july period
#plot data and set colors
fig = px.line(janjul, x = "date", y = list(janjul.columns)[1:], template = "simple_white", render_mode = "svg", title = "Performance of NUSI Versus Peers in the First Half of 2022 and July-August", color_discrete_map = {"NUSI" : "rgba(38, 70, 83, 0.5)", "NDX" : "rgba(42, 157, 143, 0.5)", "QYLD" : "rgba(233, 196, 106, 0.5)", "QRMI" : "rgba(244, 162, 97, 0.5)", "QCLR" : "rgba(231, 111, 81, 0.5)", "JEPI" : "rgba(58, 134, 255, 0.5)", "FTHI" : "rgba(187, 77, 0, 0.5)", "PBP" : "rgba(72, 86, 150, 0.5)"}, width = 754, height = 393)
#remove weekends and trading holiday gaps
fig.update_xaxes(rangebreaks = [dict(bounds = ["sat", "mon"]), dict(values = ["2022-01-17", "2022-02-21", "2022-04-15", "2022-05-30", "2022-06-20", "2022-07-04"])])
#format title
fig.update_layout(title = dict(font = dict(family = "Avenir", color = "#404040")))
fig.update_layout(font_family = "Avenir", font_color = "#404040", title_font_family = "Avenir", title_font_color = "#404040", legend_title_font_color = "#404040")
fig.update_layout(title = {"x" : 0.197})
#format legend
fig.update_layout(legend = dict(xanchor = "left", x = -0.322))
fig.update_layout(legend = dict(bgcolor = "#F8F9FA", bordercolor = "#404040", borderwidth = 1))
fig.update_layout(legend = dict(font = dict(family = "Avenir", size = 17, color = "#404040")), legend_title = dict(font = dict(family = "Avenir", size = 17, color = "#404040")))
fig.update_layout(legend_title_text = "")
#format axis and tick labels
fig.update_xaxes(title_text = "")
fig.update_yaxes(title_text= "")
fig.layout.yaxis.tickformat = ",.0%"
#save image
fig.write_image("NUSI_comp_1.jpg", scale = 3)
#---

#---
#for the july to august period
#plot data and set colors
fig = px.line(julaug, x = "date", y = list(julaug.columns)[1:], template = "simple_white", render_mode = "svg", title = " ", color_discrete_map = {"NUSI" : "rgba(38, 70, 83, 0.5)", "NDX" : "rgba(42, 157, 143, 0.5)", "QYLD" : "rgba(233, 196, 106, 0.5)", "QRMI" : "rgba(244, 162, 97, 0.5)", "QCLR" : "rgba(231, 111, 81, 0.5)", "JEPI" : "rgba(58, 134, 255, 0.5)", "FTHI" : "rgba(187, 77, 0, 0.5)", "PBP" : "rgba(72, 86, 150, 0.5)"}, width = 393, height = 393)
#remove weekends and trading holiday gaps
fig.update_xaxes(rangebreaks = [dict(bounds = ["sat", "mon"]), dict(values = ["2022-01-17", "2022-02-21", "2022-04-15", "2022-05-30", "2022-06-20", "2022-07-04"])])
#format title
fig.update_layout(title = dict(font = dict(family = "Avenir", color = "#404040")))
fig.update_layout(font_family = "Avenir", font_color = "#404040", title_font_family = "Avenir", title_font_color = "#404040", legend_title_font_color = "#404040")
fig.update_layout(title = {"x" : 0.197})
#format legend
fig.update_layout(showlegend = False)
#format axis and tick labels
fig.update_xaxes(title_text = "")
fig.update_yaxes(title_text= "")
fig.layout.yaxis.tickformat = ",.0%"
#save image
fig.write_image("NUSI_comp_2.jpg", scale = 3)
#---
