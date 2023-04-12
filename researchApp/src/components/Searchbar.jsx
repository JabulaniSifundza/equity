import React, {useState} from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';
import { motion } from 'framer-motion';
import loaderImage from '../assets/logo.PNG';

const Loader = ({isLoading, children})=>{
  return (
    <div className="loaderCont">
      {isLoading ? (
        <motion.img
          src={loaderImage}
          alt="Loading..."
          exit={{ opacity: 0 }}
          animate={{
            scale: [0.25, 0.5, 0.75, 1, 1.25, 1, 0.75, 0.5, 0.25],
            opacity: 1
          }}
          transition={{ duration: 2, repeatType: "mirror", repeat: Infinity }}
        />
      ):(
        children
      )}
    </div>
  )
}

const SummaryLoader = ({summaryIsLoading, children})=>{
  return (
    <div className="loaderContSummary">
      {summaryIsLoading ? (
        <motion.img 
          src={loaderImage}
          alt="Loading..."
          exit={{ opacity: 0 }}
          animate={{
            scale: [0.25, 0.5, 0.75, 1, 1.25, 1, 0.75, 0.5, 0.25],
            opacity: 1
          }}
          transition={{ duration: 2, repeatType: "mirror", repeat: Infinity }}
        />):(
          children
        )}
    </div>
  )
}

const Searchbar = () => {
  const [inputValue, setInputValue] = useState('');

  const [isLoading, setIsLoading] = useState(true);
  const [summaryIsLoading, setsummaryIsLoading] = useState(true);

  const [articleURLS, setArticleURLS] = useState([])
  const [ticker_scores, setTicker_scores] = useState([])
  const [ticker_summary, setTicker_summary] = useState([])

  const [sentimentError, setSentimentError] = useState(0)
  //Expenses
  const [expenses, setExpenses] = useState({})
  // Net Income
  const [netIcome, setNetIncome] = useState({})
  // Profit Margin
  const [margin, setMargin] = useState({})
  //Current Ratios
  const [currentRatio, setCurrentRatio] = useState({})
  //Ending cash balance
  const [endingCash, setEndingCash] = useState({})
  //Operating Cash Flow Ratio
  const [operatingCashRatio, setoperatingCashRatio] = useState({})
  // ROCE
  const [roce, setRoce] = useState({})
  // CAPM
  const [capm, setCapm] = useState(0.00)
  // Beta
  const [beta, setBeta] = useState(0.00)

  const newFetch = async(name)=>{
    const res = await axios.get(`http://127.0.0.1:8000/get_ticker_value_amounts/${name}/`)

    setExpenses(res.data.TotalExpense)
    setNetIncome(res.data.NetIncome)
    setEndingCash(res.data.EndingCash)

    setMargin(res.data.NetProfitMargin)
    setCurrentRatio(res.data.CurrentRatios)
    setoperatingCashRatio(res.data.OperatingCashFlowRatio)
    setRoce(res.data.ReturnOnCapitalEmployed)
  
    setCapm(res.data.ExpectedReturn)
    setBeta(res.data.CompanyBeta)

    const sentRes = await axios.get((`http://127.0.0.1:8000/get_news_clean_summarize/${name}/`)).catch((error)=>{
      console.log(error.message);
      console.log(error.response.status);
      setSentimentError(error.response.status)
    })
    setArticleURLS(Object.values(sentRes.data.cleaned_urls)[0])
    setsummaryIsLoading(false)
    //console.log(Object.values(sentRes.data.cleaned_urls)[0])
    setTicker_scores(Object.values(sentRes.data.ticker_score)[0])
    //console.log(Object.values(sentRes.data.ticker_score)[0])
    setTicker_summary(Object.values(sentRes.data.ticker_summary)[0])
    console.log(Object.values(sentRes.data.ticker_summary)[0])
  }

  const handFetch = (stock)=>{
    newFetch(stock);
    console.log(margin)
    console.log(Object.keys(netIcome));
    setIsLoading(false);
  }

  const netSeries = [{
    name: "Net Income",
    data: Object.values(netIcome)
  },
  {
    name: "Expenses",
    data: Object.values(expenses),
  },
   {
    name: "Ending Cash Balance",
    data: Object.values(endingCash),
  },
]
  const netOptions = {
    chart: {
      height: '100%',
      type: 'line',
      stacked: false
    },
    title: {
      text:`${inputValue} Net profit, Expenses and Ending Cash Balance`,
      margin: 30,
      style: {
      fontSize: '24px',
      fontWeight: 'bold',
      color:  '#000000'
    },
    },
    dataLabels:{
      enabled: false
    },
    colors: ["#008BFF", "#FF0032", "#348C31"],
    stroke: {
    width: [4, 4, 4]
  },
    series:[
      {
        name: "Net Income",
        type: "line",
        data: Object.values(netIcome)
      },
      { 
        name: "Expenses",
        type: "line",
        data: Object.values(expenses)},
      {
        name: "Ending Cash Balance",
        type: "column",
        data: Object.values(endingCash)
      }
    ],
      xaxis: {
      categories: Object.keys(netIcome)
    },
    yaxis:{
       labels: {
        formatter: function (value) {
           if (value >= 1000000000) {
              return (value / 1000000000).toLocaleString('en-US', { style: 'currency', currency: 'USD' }) + ' Billion';
            } else {
              return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
            }
        }
      },
      title: {
        text: "Amount"
      },
    },
    tooltip:{
      x: {
        format: 'YYYY',
        colors: "#000000"
      },
      style: {
        fontSize: '12px',
        color: "#000000"
      },
    }
  }

  const ratioSeries =[
    {
      name: "Net Profit Margin",
      data: Object.values(margin),
    },
    {
      name: "Current Ratio",
      data: Object.values(currentRatio),
    },
    {
      name: "Operating Cash Ratio",
      data: Object.values(operatingCashRatio),
    },
    {
      name: "Return on Capital Employed",
      data: Object.values(roce),
    }
  ]

  const ratioOptions ={
    chart: {
      height: '100%',
      type: 'line',
      stacked: false
    },
    title: {
      text:`${inputValue} Net profit margin, Current ratio and ROCE`,
      margin: 30,
      style: {
      fontSize: '24px',
      fontWeight: 'bold',
      color:  '#000000',
      
    },
    },
    dataLabels:{
      enabled: false
    },
    colors: ["#008BFF", "#FF0032", "#348C31", "#000000"],
    stroke: {
      width: [4, 4, 4, 4]
    },
    xaxis: {
      categories: Object.keys(netIcome)
    },
    yaxis:{
      labels: {
        formatter: function (value) {
           return `${(value * 100).toFixed(2)}%`
        }
      },
      title: {
        text: "Ratios"
      },
    },
    tooltip:{
      x: {
        format: 'YYYY',
        colors: "#000000"
      },
      style: {
        fontSize: '12px',
        color: "#000000"
      },
    }
  }

  return (
    <div className="appContainer">
      <div className="searchContainer">
          <input type="text" className="searchTicker" placeholder="Company Ticker" value={inputValue} onChange={event => setInputValue(event.target.value)}/>
          <button className="searchBtn" onClick={() => handFetch(inputValue)}>Search</button>
      </div>

      <Loader isLoading={isLoading}>
        {expenses ? (
           <div className="graphsAndMetrics">
            <Chart options={netOptions} series={netSeries} width="680px" height="600px"/>
            <Chart options={ratioOptions} series={ratioSeries} width="680px" height="600px"/>
            <div className="metrics">
              <h5>CAPM/Expected Return: <span className="spacer">{`${(capm * 100).toFixed(2)}%`}</span></h5>
            </div>
            <div className="metrics">
              <h5>{`${inputValue} Beta`}: <span className="spacer">{`${(beta.toFixed(2))}`}</span></h5>
            </div>
          </div>
          ):(
          <div className="graphsAndMetrics">
            <h4>We are sorry but an unknown error has occurred. Please try your search again</h4>    
          </div>
          )}
      </Loader>

      <SummaryLoader summaryIsLoading={summaryIsLoading}>
        <div className="summaryContainer">
        <h2>
          {`${inputValue} News and Sentiment analysis`}
        </h2>
        {
          articleURLS ? articleURLS.map((url, index)=>{
            return (
            <div className="summary" key={index}>
              <p className="summaryArticle">{ticker_summary[index][0].summary_text}</p>
              <a href={url} className="summaryLink">Read</a>
              <div className="summaryClass">
                <p className="summaryLabel">Sentiment:</p>
                <p className="summaryLabel">{ticker_scores[index].label}</p>
                <p className="summaryLabel">Score:</p>
                <p className="summaryScore">{`${(ticker_scores[index].score * 100).toFixed(2)}%`}</p>
              </div>
            </div>
            )
           }):(
            <div className="summary">
            <h4>
              {`We are sorry but internal server has occurred while creating your summary. Please click the search button once more. Error code ${sentimentError}`}
            </h4>

            </div>
           )}
        </div>
      </SummaryLoader>
      
    </div>
  )
}
export default Searchbar
