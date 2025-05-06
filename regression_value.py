import numpy as np
from sklearn.linear_model import LinearRegression


def calculate_regression_values(data):
    sample_rate = 1000
    change_threshold = 10

    data = np.array(data)

    # Create time array based on sampling rate
    time_values = np.arange(len(data)) / sample_rate

    # Calculate changes between consecutive readings
    changes = np.diff(data)

    # Identify compression (negative change) and rebound (positive change)
    compression_mask = changes <= -change_threshold
    rebound_mask = changes >= change_threshold

    # Create time points for changes (midpoint between readings)
    change_times = (time_values[:-1] + time_values[1:]) / 2

    # Extract compression and rebound data
    compression_times = change_times[compression_mask]
    compression_values = changes[compression_mask]

    rebound_times = change_times[rebound_mask]
    rebound_values = changes[rebound_mask]

    # Results dictionary
    results = {'compression_slope': None, 'rebound_slope': None}

    # Perform regression analysis for compression
    if len(compression_times) > 1:
        compression_X = compression_times.reshape(-1, 1)
        compression_y = compression_values
        compression_model = LinearRegression()
        compression_model.fit(compression_X, compression_y)
        results['compression_slope'] = float(compression_model.coef_[0])

    # Perform regression analysis for rebound
    if len(rebound_times) > 1:
        rebound_X = rebound_times.reshape(-1, 1)
        rebound_y = rebound_values
        rebound_model = LinearRegression()
        rebound_model.fit(rebound_X, rebound_y)
        results['rebound_slope'] = float(rebound_model.coef_[0])

    return results

def print_regression_results(results, type):
    print(type+ " Regression Results:")

    if results['compression_slope'] is not None:
        print(f"Compression Slope: {results['compression_slope']:.4f}")
    else:
        print("No significant compression movements detected.")

    if results['rebound_slope'] is not None:
        print(f"Rebound Slope: {results['rebound_slope']:.4f}")
    else:
        print("No significant rebound movements detected.")
