import requests
import datetime
import time

try:
    # Define the interval (1 minute)
    interval = 60

    # Define the number of intervals to fetch (e.g., for the last 6 hours)
    num_intervals = 6 * 60 // interval

    # Print the header line
    print("Timestamp (Unix time)\tDatetime\tOpen\tHigh\tLow\tClose\tCurrent Price")

    while True:
        # Initialize an empty list to store OHLC data
        ohlc_data = []

        # Make requests for each interval and aggregate the data
        for i in range(num_intervals):
            # Calculate the start and end timestamps for the current interval
            end_timestamp = datetime.datetime.now().timestamp() - i * interval
            start_timestamp = end_timestamp - interval
            
            # Make the request for the current interval to retrieve OHLC data
            resp = requests.get(f'https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval={interval}&since={int(start_timestamp)}')
            
            # Check if the request was successful
            if resp.status_code == 200:
                data = resp.json()
                
                # Check if the response contains OHLC data
                if 'result' in data:
                    # Check if OHLC data is available for the current interval
                    if data['result'] and isinstance(data['result']['XXBTZUSD'], list):
                        # Extract OHLC data and append to the list
                        ohlc_data.extend(data['result']['XXBTZUSD'])
                    else:
                        print(f"No OHLC data found for interval {i}.")
                else:
                    print(f"No OHLC data found for interval {i}.")
            else:
                print(f"Failed to retrieve OHLC data for interval {i}.")

            # Introduce a delay between requests to avoid rate limiting
            time.sleep(1)

        # Sort the aggregated data by timestamp
        ohlc_data.sort(key=lambda x: x[0])

        # Get the current price
        current_price_resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
        if current_price_resp.status_code == 200:
            current_price_data = current_price_resp.json()
            if 'result' in current_price_data:
                current_price = current_price_data['result']['XXBTZUSD']['c'][0]
            else:
                current_price = 'N/A'
        else:
            current_price = 'N/A'

        # Print the formatted data without the header
        for entry in ohlc_data[:10]:
            timestamp = entry[0]
            datetime_str = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            open_price = entry[1]
            high_price = entry[2]
            low_price = entry[3]
            close_price = entry[4]
            print(f"{timestamp}\t{datetime_str}\t{open_price}\t{high_price}\t{low_price}\t{close_price}\t{current_price}")

except KeyboardInterrupt:
    print("Data retrieval interrupted. Exiting...")


