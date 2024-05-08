import numpy as np
from scipy.stats import beta

def generate_sample_beta():
    # Set parameters for the beta distribution
    alpha = 2  # shape parameter
    beta_val = 5  # shape parameter

    # Generate random samples from a beta distribution
    data = beta.rvs(alpha, beta_val, size=1000)

    # Pass data to the template
    context = {
        'data': data.tolist(),
    }
    #print("context\n", context)
    return context

generate_sample_beta()

def create_regression_line_chart(scatter_plot_data):

    # Extract x and y values
    x_values = [point["x"] for point in scatter_plot_data]
    y_values = [point["y"] for point in scatter_plot_data]

    # Calculate linear regression
    coefficients = np.polyfit(x_values, y_values, 1)
    slope, intercept = coefficients

    # Create regression line data
    return [{"x": x, "y": slope * x + intercept} for x in x_values]