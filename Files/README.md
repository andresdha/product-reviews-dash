# About the Data

The data-set used for this dashboard is publicly available [here](https://data.world/datafiniti/consumer-reviews-of-amazon-products). It consists of a set of reviews for several Amazon products that were scraped from _amazon.com_ to be used for analysis.

# Analysis Techniques

The dashboard was created using [Dash](https://plotly.com/dash/) and Python. One specific product out of the lot in the data-set was selected to reduce the sample size and make model training less time-expensive.

To generate the dashboard content [topic modeling](https://en.wikipedia.org/wiki/Topic_model) and [sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) were performed on every review for that product, that wat the product's strengths and weaknesses can be automatically and directly obtained from customer feedback.
