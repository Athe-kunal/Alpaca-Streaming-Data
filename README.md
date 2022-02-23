# FinRL-project

## Project Proposal: 

It has the entire pipeline of model serving, backend, and frontend to create a demo for users of the FinRL to test out the live performance of the RL trading agents. Here is the workflow that I have thought of:

1. It starts with training and tuning a minute level model for multiple stocks and cryptocurrency
2. Serving the model using FastAPI
3. For live minute-level data using we will be using WebSockets from Alpaca and Binance and stream data to our model to get the actions i.e how many stocks to transact
4. Based on this information, we will be using Streamlit to showcase visualizations like CandleSticks and performance indicators on the web

Follow the instructions to run the repository

```pip install -r requirements.txt```

To start streaming data, run

`python final_stream.py`

To start the streamlit application, run

`streamlit run final_plot.py`
