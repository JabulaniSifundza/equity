import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Sidebar from './components/Sidebar';
import Navigation from './components/Navigation';
import Summary from './components/Summary';
import Metrics from './components/Metrics';


function App() {
  return (
    
   <div>
    <Navigation />
    <Sidebar />
   </div>
  
  )
}

export default App
