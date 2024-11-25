import numpy as np
import matplotlib.pyplot as plt

# Parameters
S0 = 100  # Initial stock price
r = 0.05  # Risk-free rate
q = 0.02  # Dividend yield
sigma = 0.4  # Volatility
T = 0.75  # Time to maturity (years)
N = 250  # Number of time steps
dt = T / N  # Time step size
M = 10000  # Number of simulations

# Precompute constants
mu = r - q  # Drift term
discount_factor = np.exp(-r * T)

# Simulate stock price paths
np.random.seed(42)  # For reproducibility
z = np.random.normal(0, 1, (M, N))  # Random draws
S = np.zeros((M, N + 1))  # Stock price matrix
S[:, 0] = S0  # Initial stock price

# Generate stock prices
for t in range(1, N + 1):
    S[:, t] = S[:, t - 1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z[:, t - 1])

# Compute average stock prices for each path
S_avg = np.mean(S[:, :-1], axis=1)  # Exclude the last time step

# Compute payoffs for Asian options
# 1. Average Strike Call Option
payoff_call = np.maximum(S[:, -1] - S_avg, 0)

# 2. Average Strike Put Option
payoff_put = np.maximum(S_avg - S[:, -1], 0)

# Discount the expected payoffs to get option prices
price_call = discount_factor * np.mean(payoff_call)
price_put = discount_factor * np.mean(payoff_put)

# Generate histograms for payoffs
def plot_histogram(payoffs, title, color, average_payoff):
    plt.figure(figsize=(8, 6))
    plt.hist(payoffs, bins=50, color=color, alpha=0.7, edgecolor='black')
    plt.axvline(x=average_payoff, color='red', linestyle='--', linewidth=2, label=f'Average Payoff = {average_payoff:.2f}')
    plt.title(title, fontsize=14)
    plt.xlabel('Payoff', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)
    plt.show()

# Plot histogram for Average Strike Call Option
average_call_payoff = np.mean(payoff_call)
plot_histogram(payoff_call, 'Payoff Histogram: Average Strike Call Option', 'orange', average_call_payoff)

# Plot histogram for Average Strike Put Option
average_put_payoff = np.mean(payoff_put)
plot_histogram(payoff_put, 'Payoff Histogram: Average Strike Put Option', 'orange', average_put_payoff)

# Print option prices
print(f"Price of Average Strike Call Option: ${price_call:.2f}")
print(f"Price of Average Strike Put Option: ${price_put:.2f}")


