import React from 'react';
import { useContext } from 'react';
import { CompanyContext } from '../context/CompanyContext';
import { Line } from "react-chartjs-2";

const Ratios = () => {
    const {financials} = useContext(CompanyContext);
    let ratios = financials.map((incomeData)=>{
        return incomeData.financialRatios
    })

    let beta = financials.map((securityData)=>{
        return securityData.beta
    })

    let expectedReturn = financials.map((securityData)=>{
        return securityData.capm
    })
  return (
    <div>Ratios</div>
  )
}

export default Ratios