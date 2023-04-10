import React from 'react';



const Summary = () => {
  
  
  return (
    <div className="summaryContainer">
        <h2>
          Company Name
        </h2>
        <div className="summary">
          <p className="summaryArticle">
            Apple is expected to launch a virtual reality headset this year. Meta has held on to the top spot in the market for years 
          </p>
          <a href="https://finance.yahoo.com/news/why-apples-headset-could-seriously-boost-the-flagging-vr-market-192922101.html" className="summaryLink">Read</a>
          <div className="summaryClass">
            <p className="summaryLabel">Sentiment:</p>
            <p className="summarySentiment">positive</p>
            <p className="summaryLabel">Score:</p>
            <p className="summaryScore">99%</p>
          </div>
        </div>


        <div className="summary">
          <p className="summaryArticle">
            Apple is expected to launch a virtual reality headset this year. Meta has held on to the top spot in the market for years 
          </p>
          <a href="https://finance.yahoo.com/news/why-apples-headset-could-seriously-boost-the-flagging-vr-market-192922101.html" className="summaryLink">Read</a>
          <div className="summaryClass">
            <p className="summaryLabel">Sentiment:</p>
            <p className="summarySentiment">positive</p>
            <p className="summaryLabel">Score:</p>
            <p className="summaryScore">99%</p>
          </div>
        </div>
    </div>
  )
}

export default Summary
