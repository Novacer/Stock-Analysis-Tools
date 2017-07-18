# Stock Analysis Tools
A collection of tools for analyzing stock data. Includes: Line charts, candlestick charts, correlation matrices, and an experimental machine learning stock screener.

This python program provides a multitude of ways for professional and retail traders to analyze and visualize large quantities of market data.
While there are certainly many premium softwares that provide such features, we instead aim to supply the user with the same tools at no additional cost.

## The Line Chart
The "Get Line Chart" feature first prompts the user for a stock ticker/symbol, and the interval of data that they want to graph.

![ScreenShot](https://user-images.githubusercontent.com/29148427/28299145-482aaf8a-6b2c-11e7-8ec5-b791925b07b2.jpg)

After pressing "start", the program will store the two dates as a string before converting them into [datetime](https://docs.python.org/3/library/datetime.html) objects.
Using the two dates and the stock symbol, all of the relevant data (open/high/low/close/volume) will be downloaded from the Yahoo! Finance API and saved temporarily as a [DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).
The daily adjusted closing prices, 100 day moving average, and volume will be graphed on an interactive chart. (See below)

![ScreenShot](https://user-images.githubusercontent.com/29148427/28299473-52c39b1c-6b2e-11e7-9a8f-f35b29d18860.jpg)

## The Bar Chart
Similar to the Line Chart, the "Get Bar Chart" feature will also prompt the user for a stock ticker/symbol, and the interval of time that they want to graph.
It will also download the relevant stock data from the Yahoo! Finance API. However, unlike the Line Chart, the Bar Chart will manipulate the DataFrame
and compile the data in ten day intervals. The result produces the very familiar candlestick chart, like so:

![ScreenShot](https://user-images.githubusercontent.com/29148427/28299721-bd44534a-6b2f-11e7-983c-82338a470c76.jpg)

## The Correlation Matrix
Now we get to the fun part.

* See [here](http://www.investopedia.com/terms/c/correlation.asp) if you want an explanation on what correlation is used for in finance.

The "Make Correlation Matrix" feature will begin by prompting the user for an index to analyze, as well as the time interval to analyze.
Currently, we support the [S&P 500](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) index and the [NASDAQ 100](http://www.cnbc.com/nasdaq-100/) index.

![ScreenShot](https://user-images.githubusercontent.com/29148427/28300189-aacce1ca-6b32-11e7-9341-7fe8c030811d.jpg)

The program will create a folder named sp500_stock_dfs (or nasdaq100_stock_dfs) in the directory of the program. Then it will download all of the stock
data from the specified index during the time interval from Yahoo! Finance API as .csv files. This can take quite a while for the first time! After the first time, however, the user
will be able to reuse the same data, or re-download it if they want to update the data. 

The program will then compile all of the adjusted closing prices into a single csv file. Afterwards, it will extrapolate the % return from the daily prices.
* See [here](http://www.investopedia.com/terms/r/return.asp) if you want to learn more about how returns are used in finance.

Finally, it will perform a bunch of fancy math to calculate the [Pearson product-moment correlation](http://www.investopedia.com/terms/c/correlationcoefficient.asp?lgl=rira-baseline-vertical)
for each 2 pairs of stocks within the index. All of this data is taken to be visualized as a "heatmap".

![ScreenShot](https://user-images.githubusercontent.com/29148427/28300588-5dfc2c2c-6b35-11e7-8c10-2ba6bb2dc375.jpg)

I know, the outside borders look REALLY ugly, but that's because there's 500 labels crammed in there... It'll get better when we zoom in anyways.

Looking at it like this we don't really see what's going on, but once we zoom in the significance suddenly becomes clear.

![ScreenShot](https://user-images.githubusercontent.com/29148427/28300721-416de900-6b36-11e7-8b8e-b190acc7dafe.jpg)

We see here a collection of pixels ranging from lightish yellow to dark green. As explained by the legend on the right side, dark green represents
a correlation of 1.00, yellow represents a correlation of 0, and dark red represents a correlation of -1.00.

In layman's terms, the greener the pixel, the stronger the positive relationship is between the two companies (If A's price goes up, B's price goes up as well). 
Yellow pixels represent companies whose prices don't seem to have a relationship.
Red pixels represent companies that have an inverse relationship (If A's price goes up, B's price goes down).

From our example here we see that EQR and MAA have a very strong positive correlation. A quick comparision between the charts of these two companies
and you will see that their prices indeed rise and fall in unison.

## Machine Learning
To be continued....



