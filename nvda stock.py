#import libraries
import requests     #to make http requests to the polygon.io api
import datetime     #for formatting and working with dates
import matplotlib.pyplot as plt

#setup section

API_KEY = "" #replace with own polygon api key
TICKER = "NVDA"  #ticker symbol for the stock you want to look up
START_DATE = "2021-07-01"      #duolingo IPO'd in july 2021 so we start here(starting point)
END_DATE = "2024-07-01"     #End date for the desired product




#function: fetch daily stock prices

def fetch_stock_data(ticker, start_date, end_date):
    #construct the URL for polygons aggregates (bars) endpoint
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    
    #set up parameters for the request
    params = {
        "adjusted": "true",    #use adjusted prices (takes splits/dividends into account)
        "sort": "asc",         #sort oldest to newest
        "limit": 50000,        #fetch up to 50000 records at once (safe for long time spans)
        "apiKey": API_KEY      #your personal api key
    }
    
    #send the HTTP GET request
    response = requests.get(url, params=params)
    
    #parse the response into JSON format
    data = response.json()
    
    #check if the response contains the expected 'results' key
    if "results" not in data :
        print("Error:", data.get("error", "Unknown issue")) #show error message if available
        return[] #return an empty list if soemthign went wrong
    
    return data["results"] #return the list of daily data points


#main code

# call the function to get the data
stock_data = fetch_stock_data(TICKER, START_DATE, END_DATE)

#loop through and display the first few days of results
for day in stock_data[:5]: #onyl prin the first 5 days to keep it short
    #convert the timestamp from milliseconds to a readable data
    date = datetime.datetime.fromtimestamp(day["t"] / 1000).strftime("%Y-%m-%d")
    
    #print out the key stock data for that day
    print(f"{date} | Open: {day['o']} | High: {day['h']} | Low: {day['l']} | Close: {day['c']}")
    
    
    

#if the data is empty, exit early with a message
if not stock_data:
    print(" no data returned. Check the APi key, ticker, or date range.")
else:
    #convert timestamps to datetime objects for plotting
    dates = [datetime.datetime.fromtimestamp(day["t"] / 1000) for day in stock_data]
    
    #extract the closing prices for each day
    close_prices = [day["c"] for day in stock_data]
    
    # plot the data
    plt.figure(figsize=(12, 6)) #set the size of the plot
    plt.plot(dates, close_prices, label=f'{TICKER} Closing price', color = "black") #plot the close prices
    plt.title(f'{TICKER} Stock Price (Since IPO)') #title of the graph
    plt.xlabel("Date")     #label for x axis
    plt.ylabel("price (USD)")  #label for y axis
    plt.grid(True)    #add gridlines for better readability
    plt.legend()      #show the legend with the ticker name
    plt.tight_layout()  #adjust layout to avoid overlap
    plt.show()          #display final graph
