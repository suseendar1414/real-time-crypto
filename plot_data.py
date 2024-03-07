import matplotlib.pyplot as plt
from backend import fetch_and_process_ohlc_data

def plot_realtime_ohlc_data():
    plt.ion()  # Turn on interactive mode for continuous plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title('Real-Time OHLC Data')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')

    while True:
        timestamps, open_prices, high_prices, low_prices, close_prices = fetch_and_process_ohlc_data()

        # Clear previous plot
        ax.clear()

        # Plot new data
        ax.plot(timestamps, open_prices, label='Open', color='blue')
        ax.plot(timestamps, high_prices, label='High', color='green')
        ax.plot(timestamps, low_prices, label='Low', color='red')
        ax.plot(timestamps, close_prices, label='Close', color='orange')

        # Customize plot
        ax.legend()
        ax.grid(True)

        # Update plot
        plt.pause(1)  # Adjust this delay as needed for real-time updating

# Call the function to plot real-time OHLC data
plot_realtime_ohlc_data()
