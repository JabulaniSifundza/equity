import React from 'react';
import { useContext } from 'react';
import { CompanyContext } from '../context/CompanyContext';
import { Line } from "react-chartjs-2";

const Cashflow = () => {
    const {financials} = useContext(CompanyContext);
    let flows = financials.map((incomeData)=>{
        return incomeData.cashflow
    })
  return (
    <div>Cashflow</div>
  )
}

export default Cashflow