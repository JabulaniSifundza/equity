import React, { useState } from 'react';

const Sidebar = () => {
  const [showSidebar, setShowSidebar] = useState(false);

  const toggleSidebar = () => {
    setShowSidebar(!showSidebar);
  };

  return (
    <div className={`sidebar ${showSidebar ? 'show' : ''}`}>
      <button className="hamburger" onClick={toggleSidebar}>
        <span></span>
        <span></span>
        <span></span>
      </button>
      <div className="appDescription">
        <h1>
            Equity Research Application
        </h1>
        <p>
            This application's purpose is to aid users with Equity Research.
            Users can search for a public company's information by entering the desired company's Ticker symbol in the search bar.
            The application searches Yahoo Finance for news articles about the searched company.
            The application uses Hugging Face's Financial Summarization model to summarize news articles.
            The summarized articles are then passed into Hugging Face's Sentiment Analysis Pipeline in order to classify the news as either positive, neutral or negative.
            The application also creates visualizations on key company metrics over a 5 year period.
            The sentiment analysis section is right below the data visualization section. If the sentiment analysis section does not stope loading, please restart your search.
        </p>
      </div>
    </div>
  );
};

export default Sidebar;