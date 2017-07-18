# Stock Analysis Tools
A collection of tools for analyzing stock data. Includes: Line charts, candlestick charts, correlation matrices, and an experimental machine learning stock screener.

This python program provides a multitude of ways for professional and retail traders to analyze and visualize large quantities of market data.
While there are certainly many premium softwares that provide such features, we instead aim to supply the user with the same tools at no additional cost.

## The Correlation Matrix
Let's go right into it!

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
**This feature is made to be purely experimental. DO NOT USE this feature as sound financial advice!!!** 

Based on the supplied market index data, the "Do Machine Learning" feature will try to predict the future percent change of a particular ticker. Like the Correlation Matrix, this feature will begin by asking the user to download all of the stock data for an index. However, this time it will also ask the user to specify a particular ticker.

![ScreenShot](https://user-images.githubusercontent.com/29148427/28332221-dd59699e-6ba8-11e7-89c3-e87ef8a79514.jpg)

After downloading all of the relevant market index data, the program will create a folder and save the each company's data as individual csv files. The adjusted closing prices of these csv files will be compiled into one joined csv files. A bunch of formatting will then be done in the background so that the data would be ready for us to use in our machine learning algorithm. The data will be separated into [features and labels](https://stackoverflow.com/questions/40898019/what-is-the-difference-between-feature-and-label).

For now we will make the following definitions for our labels:

|Action taken| Change in price|
|------------|----------------|
|Buy         |2% increase     |
|Sell        |2% decrease     |
|Hold        |-2%< x <2% change|

In reality, these particular definitions need to be tuned for each individual machine learning algorithm and each individual stock, but we will use 2% for now. In addition, your trading strategy may also influence these limits.

It follows, then, that our feature set will be the actual daily percentage change of the company's stock prices. For example, a percentage increase of <2% during a seven day interval (the input/feature) would map to the action taken of "buy" (the output/label). 

We will now select the appropriate model for our machine learning algorithm.

### To shuffle or not to shuffle?

During the creation of this algorithm the biggest dilemma for me was whether or not to use a [train_test_split](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) model or a [TimeSeriesSplit](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html). A TTS would shuffle up the train and testing data sets, while the TSS would keep the train and testing data sets in chronological order. For example, TSS would train on k and then test on k+1. 

At first this may seem like a silly question. *Why would anyone what to shuffle up the chronological order?* Indeed, it may seem absurd to potentially use the data from 2017 to predict the prices of 2016. That just makes no sense.

At the same time, though, it may not be the best decision to use the data from 2014 to predict the prices of 2017. Certainly, global events, investor confidence, market conditions, and relationships between different companies are changing constantly. So there is no guaruntee that the patterns of the past will still apply in the future. It turns out that for longer, *more general* models, shuffling the data may actually yield more accurate predictions! However, for shorter intervals with more frequent data (i.e. minute prices), a TSS is more appropriate.

(In this github version we have included only the TimeSeriesSplit)

### The Voting Classifier

For this program we have chosen to use a [VotingClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html) to do our predictions. The VotingClassifier contains three classifiers inside it, being [LinearSVC](http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html), [KNeighborsClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html), and [RandomForestClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html). These three classifiers will do a majority vote, and the result of the vote is used as our prediction.

### The Results are in!!!

As an example, I will do machine learning on AAPL against the S&P 500 index. Just for the fun of it, let's use 17 years' worth of daily stock prices (because we can). Here are the results using TTS:

![ScreenShot](https://user-images.githubusercontent.com/29148427/28335613-db5e1c06-6bb3-11e7-9a6b-b314d6a11542.jpg)

On the bottom left corner is the data spread. This is what the data actually looks like before we split it into testing and training sets. On the bottom right corner is the number of times the machine predicted buy, sell, and hold respectively. It made the right prediction 47% of the time, which is certainly better than randomly guessing. 



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

