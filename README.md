# Identifying Risk Sources with Principal Component Analysis
The aim of this project is to look into how Principal Component Analysis can be employed to identify uncorrelated risk sources for leveraging in stock markets.
The project tries to answer following questions:
* What is difference between using correlation and covariance matrix as an underlying foundation of PCA?
* What can be the possible interpretation of first N principal components? How are they different?

## Methodology:
There exist numerous books and articles describing application of PCA on time series data, as well as research papers discussing possible implications of the applied method. 
The data was taken from German equity market, in particular companies listed in the DAX, MDAX and SDAX indices,
which contain combination of large and medium-sized enterprises with no industry restrictions.
The timeframe spans more than 12 years, since the beginning of 2010. 
Python programming language and its various libraries was used to assist during the implementation process.
The data itself was taken through Yahoo! Finance API.
The German market was chosen to be conducted the research on considering following reasons:
* It is a representative of a highly developed European country with diversified economy, which is reflected in the equity market itself.
* The said market is not a usual example in the textbooks and is rarely being talked about in the non-specific research papers discussing risk factors and equity markets.

## Implementation: 
This application was created using Python's Dash implementation. Different modules were interconnected
with the help of Flask engine. The data about indexes constituents were gathered from an open source and
the price data was acquired using Yahoo! Finance's API. The data was then stored in SQLite database. The ETL process was handled using Python.
Plotly provides the graphs for the frontend, as well as the overall HTML structure that accompanies it.
At this point the backend can handle following actions:
* Set up an SQLite database with a given schema, that allows the accommodation of daily stocks data
* Conduct an ETL process: from fetching the data from API to storing it in the Database following normalisation conventions
* Preprocess the given data for feeding the frontend data-dependent elements
* Define the Principal Component Analysis from scratch, thus modelling the data and providing insights into the underlying statistical structure
