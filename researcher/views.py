from django.shortcuts import render
import requests
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from bs4 import BeautifulSoup
from django.http import JsonResponse
import json
import numpy as np
from yahooquery import Ticker
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
from secret import API_TOKEN
# Create your views here. 

def index(request):
    return render(request, 'index.html')

API_TOKEN = API_TOKEN
API_URL = "https://api-inference.huggingface.co/models/human-centered-summarization/financial-summarization-pegasus"
SENTI_MODEL_URL = "https://api-inference.huggingface.co/models/ahmedrachid/FinancialBERT-Sentiment-Analysis"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis",num_labels=3)
tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
sentiment = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

unwanted_string_list = ['maps', 'policies', 'preferences', 'accounts', 'support']

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()   

def sent_query(payload):
    response = requests.post(SENTI_MODEL_URL, headers=headers, json=payload)
    return response.json()


research_tickers = []

def get_news(ticker):
    news_source = f"https://www.google.com/search?q=yahoo+finance+{ticker}&tbm=nws"
    r = requests.get(news_source)
    soup = BeautifulSoup(r.text, 'html.parser')
    linktags = soup.find_all('a')
    return [link['href'] for link in linktags]

article_links = {ticker:get_news(ticker) for ticker in research_tickers}

def remove_unwanted_strings(urls, unwanted_string):
	# sourcery skip: invert-any-all
    new_urls = []
    for url in urls:
        if 'https://' in url and not any(exclude_word in url for exclude_word in unwanted_string):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            new_urls.append(res)
    return list(set(new_urls))
cleaned_urls = {ticker:remove_unwanted_strings(article_links[ticker], unwanted_string_list) for ticker in research_tickers}

def scrape_and_read_articles(URLs):
    NEWS_ARTICLES = []
    for url in URLs:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        paragraph_text = [paragraph.text for paragraph in paragraphs]
        words = ' '.join(paragraph_text).split(' ')[:350]
        full_article = ' '.join(words)
        NEWS_ARTICLES.append(full_article)
    return NEWS_ARTICLES
# articles = {ticker:scrape_and_read_articles(cleaned_urls[ticker]) for ticker in research_tickers}

def summarize(articles):
    summaries = []
    for article in articles:
        summary = query({"inputs": article})
        summaries.append(summary)
    return summaries
# ticker_summary = {ticker:summarize(articles[ticker]) for ticker in research_tickers}

def get_sentiment(summaries):
    sentiments = []
    for summary in summaries:
        # score = sentiment(summary[0]['summary_text'])
        score = sent_query(summary[0]['summary_text'])
        sentiments.append(score[0][0])
        # sentiments.append(score[0])
    return sentiments


# ticker_score = {ticker:get_sentiment(ticker_summary[ticker]) for ticker in research_tickers}
def create_output_list(ticker_summary, scores, article_urls):
    output = []
    for ticker in research_tickers:
        for counter in range(len(ticker_summary[ticker])):
            desired_output = [
                ticker,
                ticker_summary[ticker][counter][0]['summary_text'],
                scores[ticker][counter][0]['label'],
                scores[ticker][counter][0]['score'],
                article_urls[ticker][counter]
            ]
            output.append(desired_output)
    return output


# full_summary = create_output_list(ticker_summary, ticker_score, cleaned_urls)
# full_summary.insert(0, ['Ticker Symbol', 'Article Summary', 'Sentiment/Label', 'Confidence', 'Full article URL'])

company_ticker = Ticker('AAPL')
market_ticker = Ticker('^GSPC')
stock_priceDF = company_ticker.history(period='1d', start='2018-01-31', end='2023-02-01')
market_DF = market_ticker.history(period='1d', start='2018-01-31', end='2023-02-01')
stock_priceDF['log_returns'] = np.log(stock_priceDF['adjclose']/stock_priceDF['adjclose'].shift(1))
market_DF['log_returns'] = np.log(market_DF['adjclose']/market_DF['adjclose'].shift(1))
stock_priceDF = stock_priceDF.dropna()
market_DF = market_DF.dropna()

covariance = (np.cov(stock_priceDF['log_returns'], market_DF['log_returns'])) * 250
covariance_with_market = covariance[0, 1]

market_variance = market_DF['log_returns'].var() * 250

beta_final = covariance_with_market / market_variance
company_capm = 0.025 + beta_final * 0.05

income_state = company_ticker.income_statement()
balance_sheet = company_ticker.balance_sheet()
cash_flow_statement = company_ticker.cash_flow(trailing=False)

def get_costs_(cost_array):
	return [float(cost) for cost in cost_array]

def get_year(income_state_years):
    years = []
    for year in income_state_years:
        str_time = year.strftime('%Y-%m-%d')
        years.append(str_time)
    return years

def get_net(ebit_array):
	return [float(earning) for earning in ebit_array]

def get_ebit(earnings_arr):
	return [float(earned) for earned in earnings_arr]

def get_revenue(revenue_arr):
	return [float(rev) for rev in revenue_arr]

# sourcery skip: identity-comprehension
years = get_year(income_state['asOfDate'])
total_expense = get_costs_(income_state['TotalExpenses'])
net = get_net(income_state['NetIncome'])
ebit = get_ebit(income_state['EBIT'])
total_revenues = get_revenue(income_state['TotalRevenue'])

total_expense_dict = {year: cost for (year, cost) in zip(years, total_expense)}
net_income_dict = {year: income for (year, income) in zip(years, net)}

def get_total_liabilities(liabilities):
	return [float(liability) for liability in liabilities]

def get_total_assets(assets):
	return [float(asset) for asset in assets]

def get_total_cash(cash):
	return [float(liquidity) for liquidity in cash]

def get_current_assets(current_assets):
	return [float(current_asset) for current_asset in current_assets]

def get_current_liabilities(current_liabilities):
	return [float(current_liability) for current_liability in current_liabilities]

def ending_cash_balance(ending_cash):
	return [float(ending_cash) for ending_cash in ending_cash]

def get_operating_cash_flow(cash_flow_arr):
	return [float(cash_flow) for cash_flow in cash_flow_arr]

val_ending_cash_balance = ending_cash_balance(cash_flow_statement['EndCashPosition'])
total_liabilities = get_total_liabilities(balance_sheet['TotalLiabilitiesNetMinorityInterest'])
total_assets = get_total_assets(balance_sheet['TotalAssets'])
total_cash_equivalents = get_total_cash(balance_sheet['CashAndCashEquivalents'])
total_current_assets = get_current_assets(balance_sheet['CurrentAssets'])
total_get_current_liabilities = get_current_liabilities(balance_sheet['CurrentLiabilities'])
operating_cash_flows = get_operating_cash_flow(cash_flow_statement['OperatingCashFlow'])

# Calculating Ratios
# Current ratio - company's ability to pay off its current liabilities 
current_ratios = {year: current_asset/current_liability for(year, current_asset, current_liability) in zip(years, total_current_assets, total_get_current_liabilities)}
# ROCE - Return on Capital Employed
roce = {year: year_ebit/(assets - curr_liabilities) for(year, year_ebit, assets, curr_liabilities) in zip(years, ebit, total_assets, total_get_current_liabilities)}
# Net Profit Margin
net_profit_margin = {year: (net_income/revenue) for(year, net_income, revenue) in zip(years, net, total_revenues)}
# Operating Cash Flow ratio
operating_cash_flow_ratio = {year: operating_cash/current_liability for(year, operating_cash, current_liability) in zip(years, operating_cash_flows, total_get_current_liabilities)}

def get_news_clean_summarize(request, research_ticker):
    # blank_call = summarize(articles[research_ticker])
    # summarize(articles[research_ticker])
    research_tick_as_list = [research_ticker]
    get_news(research_ticker)
    article_links = {ticker:get_news(ticker) for ticker in research_tick_as_list}
    cleaned_urls = {ticker:remove_unwanted_strings(article_links[ticker], unwanted_string_list) for ticker in research_tick_as_list}
    articles = {ticker:scrape_and_read_articles(cleaned_urls[ticker]) for ticker in research_tick_as_list}
    ticker_summary = {ticker:summarize(articles[ticker]) for ticker in research_tick_as_list}
    ticker_score = {ticker:get_sentiment(ticker_summary[ticker]) for ticker in research_tick_as_list}
    full_summary = create_output_list(ticker_summary, ticker_score, cleaned_urls)
    full_summary.insert(0, ['Ticker Symbol', 'Article Summary', 'Sentiment/Label', 'Confidence', 'Full article URL'])
    return JsonResponse({'FullSummary': full_summary, 'ticker_score': ticker_score, 'ticker_summary': ticker_summary, 'cleaned_urls': cleaned_urls})

def get_ticker_value_amounts(request, research_ticker):
	# sourcery skip: identity-comprehension
    company_ticker = Ticker(research_ticker)
    market_ticker = Ticker('^GSPC')
    income_state = company_ticker.income_statement()
    balance_sheet = company_ticker.balance_sheet()
    cash_flow_statement = company_ticker.cash_flow(trailing=False)
    stock_priceDF = company_ticker.history(period='1d', start='2018-01-31', end='2023-02-01')
    market_DF = market_ticker.history(period='1d', start='2018-01-31', end='2023-02-01')
    stock_priceDF['log_returns'] = np.log(stock_priceDF['adjclose']/stock_priceDF['adjclose'].shift(1))
    market_DF['log_returns'] = np.log(market_DF['adjclose']/market_DF['adjclose'].shift(1))
    stock_priceDF = stock_priceDF.dropna()
    market_DF = market_DF.dropna()
    covariance = (np.cov(stock_priceDF['log_returns'], market_DF['log_returns'])) * 250
    covariance_with_market = covariance[0, 1]

    market_variance = market_DF['log_returns'].var() * 250

    beta_final = covariance_with_market / market_variance
    company_capm = 0.025 + beta_final * 0.05
    
    
    years = get_year(income_state['asOfDate'])
    net = get_net(income_state['NetIncome'])
    ebit = get_ebit(income_state['EBIT'])
    total_revenues = get_revenue(income_state['TotalRevenue'])
    total_expense = get_costs_(income_state['TotalExpenses'])
    val_ending_cash_balance = ending_cash_balance(cash_flow_statement['EndCashPosition'])
    total_liabilities = get_total_liabilities(balance_sheet['TotalLiabilitiesNetMinorityInterest'])
    total_assets = get_total_assets(balance_sheet['TotalAssets'])
    total_cash_equivalents = get_total_cash(balance_sheet['CashAndCashEquivalents'])
    total_current_assets = get_current_assets(balance_sheet['CurrentAssets'])
    total_get_current_liabilities = get_current_liabilities(balance_sheet['CurrentLiabilities'])
    operating_cash_flows = get_operating_cash_flow(cash_flow_statement['OperatingCashFlow'])
    # Current ratio - company's ability to pay off its current liabilities 
    current_ratios = {year: current_asset/current_liability for(year, current_asset, current_liability) in zip(years, total_current_assets, total_get_current_liabilities)}
    # ROCE - Return on Capital Employed
    roce = {year: year_ebit/(assets - curr_liabilities) for(year, year_ebit, assets, curr_liabilities) in zip(years, ebit, total_assets, total_get_current_liabilities)}
    # Net Profit Margin
    net_profit_margin = {year: (net_income/revenue) for(year, net_income, revenue) in zip(years, net, total_revenues)}
    # Operating Cash Flow ratio
    operating_cash_flow_ratio = {year: operating_cash/current_liability for(year, operating_cash, current_liability) in zip(years, operating_cash_flows, total_get_current_liabilities)}
        
    total_expense_dict = {year: cost for (year, cost) in zip(years, total_expense)}
    net_income_dict = {year: income for (year, income) in zip(years, net)}
    ending_cash_values = {year: ending_cash for (year, ending_cash) in zip(years, val_ending_cash_balance)}
    return JsonResponse({'TotalExpense': total_expense_dict, 'NetIncome': net_income_dict, 'ExpectedReturn': company_capm, 'CompanyBeta': beta_final, 'CurrentRatios':current_ratios, 'ReturnOnCapitalEmployed':roce, 'NetProfitMargin': net_profit_margin, 'OperatingCashFlowRatio': operating_cash_flow_ratio, 'EndingCash': ending_cash_values})



