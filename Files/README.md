# About the Data

The data-set used for this dashboard is publicly available [here](https://data.world/datafiniti/consumer-reviews-of-amazon-products). It consists of a set of reviews for several Amazon products that were scraped from _amazon.com_ to be used for analysis.

# Analysis Techniques

The dashboard was created using [Dash](https://plotly.com/dash/) and Python. One specific product out of the lot in the dataset was selected with a balance in mind:

- reducing the sample size in order to make model training less time consuming and computationally expensive (since this is a small display dashboard)
- having enough data to make the techniques used viable

To generate the dashboard content [topic modeling](https://en.wikipedia.org/wiki/Topic_model) (using [_None- Negative Matrix Factorization (NMF)_](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) ) and [sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) (using the [_Natural Language Toolkit (NLTK) Vader Sentiment Analyzer_](https://en.wikipedia.org/wiki/Natural_Language_Toolkit) ) were performed on every review for that product, that way the product's strengths and weaknesses can be automatically and directly obtained from customer feedback.

The goal of the dashboard is not to perform an exhaustive analysis on the product, but to display some tools that I can bring to the table that, I believe, can enrich the way data is processed, mined, and digested to generate useful information.
