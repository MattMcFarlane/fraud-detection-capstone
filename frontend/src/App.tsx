import { useState } from 'react'
import './App.css'

function App() {
  //set up transaction data form values
  const [transactionData, setTransactionData] = useState({
    distance_from_home: 0,
    distance_from_last_transaction: 0,
    ratio_to_median_purchase_price: 0,
    repeat_retailer: false,
    used_chip: false,
    used_pin_number: false,
    online_order: false
  })

  //define the fraud result type to use for holding api valu
  type fraudResult = {
    fraud_probability: number,
    flagged_as_fraud: boolean
  }
  //set the fraud result state initially to null, allowing fraudResult or null types
  const [fraudResult, setFraudResult] = useState<fraudResult | null>(null)

  //handle form submit and api call
  const submitTransaction = async(event : React.FormEvent) => {
    //block browser from auto refreshing
    event.preventDefault()

    //call api
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(transactionData)
    })

    //wait for response
    const result = await response.json()

    //log result
    console.log(result)

    //set result
    setFraudResult(result)

  }

  return (
    <>
      <section id="top">
        <div>
          <h1>Card Master's Fraud Detection Tool</h1>
          <form onSubmit={submitTransaction}>
            <div className="form-grid">
              {/*Home distance*/}
              <label>Distance From Home:</label>
              <input className="slider" type="range" min="0" max="500"
                value={transactionData.distance_from_home}
                onChange={(event) => setTransactionData({
                  ...transactionData,
                  distance_from_home: Number(event.target.value)
                })}/>
              <div className="slider-value">{transactionData.distance_from_home}</div>

              {/*Last Transaction*/}
              <label>Distance From Last Transaction:</label>
              <input className="slider " type="range" min="0" max="200"
                value={transactionData.distance_from_last_transaction}
                onChange={(event) => setTransactionData({
                  ...transactionData,
                  distance_from_last_transaction: Number(event.target.value)
                })}/>
              <div className="slider-value">{transactionData.distance_from_last_transaction}</div>

              {/*Median Purchase Price*/}
              <label>Ratio To Median Purchase Price:</label>
              <input className="slider" type="range" min="0" max="10" step="0.1"
                value={transactionData.ratio_to_median_purchase_price}
                onChange={(event) => setTransactionData({
                  ...transactionData,
                  ratio_to_median_purchase_price: Number(event.target.value)
                })}/>
              <div className="slider-value">{transactionData.ratio_to_median_purchase_price} </div>

              {/*Repeat Retail*/}
              <label>Repeat Retailer: </label>
              <input type="checkbox" checked={transactionData.repeat_retailer}
              onChange={(event) => setTransactionData({
                ...transactionData,
                repeat_retailer: event.target.checked
              })}/>
              <span></span>

              {/*chip*/}
              <label>Used Chip:</label>
              <input type="checkbox" checked={transactionData.used_chip}
              onChange={(event) => setTransactionData({
                ...transactionData,
                used_chip: event.target.checked
              })}/>
              <span></span>

              {/*pin*/}
              <label>Used Pin Number:</label>
              <input type="checkbox" checked={transactionData.used_pin_number}
              onChange={(event) => setTransactionData({
                ...transactionData,
                used_pin_number: event.target.checked
              })}/>
              <span></span>

              {/*online*/}
              <label>Online Order:</label>
              <input type="checkbox" checked={transactionData.online_order}
              onChange={(event) => setTransactionData({
                ...transactionData,
                online_order: event.target.checked
              })}/>
              <span></span>

              {/*Submit button*/}
              <button type="submit">Check Transaction</button>
            </div>
          </form>
        </div>

        {fraudResult != null && (
            <div className="fraud-results">
              <h2>Results</h2>
              <p>Prediction: {fraudResult.flagged_as_fraud ? "Fraud" : "Not Fraud"}</p>
              <p>Fraud Probability: {(fraudResult.fraud_probability * 100).toFixed(3)}%</p>
            </div>
        )}
      </section>

      <section id="ds-analysis">
        <h2>Dataset Analysis</h2>
        <div>
          <img src="/charts/fraud_by_home_distance.png" alt="Fraud Rate by Distance From Home"/>
        </div>
        <div>
          <img src="/charts/fraud_by_last_transaction.png" alt="Fraud Rate by Distance From Last Transaction" />
        </div>
        <div>
              <img src="/charts/fraud_by_purchase_ratio.png" alt="Fraud Rate by Ratio to Median Purchase Price"/>
        </div>

      </section>
    </>
  )
}

export default App
