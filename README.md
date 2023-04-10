# equity
A React-Django Full-stack Equity Research Aid Application

This application uses a Django server and a React front-end to assist users doing equity research easier.
The application allows you to search for a puclicly traded company using its ticker symbol.
The application starts by visualizing various profitability measures and ratios to give you an idea of the company's current financiaql standing.
The application also calculates the stock's beta and expected return using CAPM (Capital Asset Pricing Model).

Next, it scrapes the web for the latest news articles on the searched public company. 
It uses The BERT Hugging Face Financial Summarization Machine Learning model to summarize the articles into one sentence.
The model is also used for sentiment analysis to tell whether the news articles was neutral, negative or positive with a score on how certain the model is of its prediction.
The application also provides the user with a link to the full article so they may the full article themselves.
