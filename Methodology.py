import numpy as np
import matplotlib.pyplot as plt

def stock_price(s_0=100, dt=0.004, r=0.05, q=0.02, vol=0.4, period=250):
    # Make a history of stock prices over 250 trading days
    prices = np.zeros(period)
    ## initialize an empty array to store prices that
    # move based on Brownian motion
    epsilon = np.random.randn(period)
    ## an array of standard normal errors
    price_new = s_0

    for a in range(period):
        price_new = price_new * np.exp((r - q - 0.5 * vol**2) * dt + vol * np.sqrt(dt) *
                     epsilon[a])
        ## updated price of the stock
        prices[a] = price_new

    return prices  ## vector of history of prices

def simulation(iterations=10000, period=250):
    # Simulate some number of histories of stock prices
    simulations = np.zeros((iterations, period))
    for i in range(iterations):
        simulations[i] = stock_price()
    return simulations

def option_price(option_payoff, rate=0.05, T=0.75):
    # Calculate the price of the option
    return int(np.sum(option_payoff) / 10000 *
               np.exp(-T * rate) * 10000) / 10000

def plotting(payoffs, name):
    avg = np.mean(payoffs)
    plt.figure(figsize=(8, 6))
    plt.hist(payoffs, bins=30, color = "orange", edgecolor = "black")
    plt.axvline(x=avg, color='red', linestyle='--', linewidth=2, label=f'Average Payoff = {avg:.2f}')
    plt.xlabel('Payoff', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title("Payoff Histogram of " + name, fontsize=14)
    plt.grid(alpha=0.3)
    plt.legend(fontsize=12)
    ## Note average payoff at maturity
    plt.show()

def lookBackCallPrice(sim=simulation()):
    # Simulation and price of Lookback Call Option
    payoffs = np.zeros(len(sim))  ## initialize empty array for payoffs
    i = 0
    for vector in sim:
        K = np.min(vector)  ## "strike" of this option is the minimum
        S_T = vector[-1]  ## price at maturity
        payoffs[i] = (S_T - K)  ## append the payoffs of each simulation
        i += 1
    plotting(payoffs, "Lookback Call Option")
    print("Price of Lookback Call Option: $" + str(
        option_price(payoffs)))
    ## calculate the price from the payoffs of all sims

def lookBackPutPrice(sim=simulation()):
    # Simulation and price of Lookback Put Option
    payoffs = np.zeros(len(sim))  # initialize empty array for payoffs
    i = 0
    for vector in sim:
        K = np.max(vector)  # "strike" of this option is the maximum
        S_T = vector[-1]  # price at maturity
        payoffs[i] = (K - S_T)  # append the payoffs of each simulation
        i += 1
    plotting(payoffs, "Lookback Put Option")
    print("Price of Lookback Put Option: $" + str(
        option_price(payoffs)))
    # calculate the price from the payoffs of all sims

def europeanCallPrice(sim=simulation()):
    # Simulation and price of European Call Option
    strike_price = 110  # Strike price for the call option
    payoffs = np.zeros(len(sim))  # initialize empty array for payoffs
    i = 0
    for vector in sim:
        S_T = vector[-1]  # price at maturity
        payoffs[i] = max(S_T - strike_price, 0)  # European call payoff
        i += 1
    plotting(payoffs, "European Call Option")
    print("Price of European Call Option: $" + str(
        option_price(payoffs)))


def europeanPutPrice(sim=simulation()):
    # Simulation and price of European Put Option
    strike_price = 90  # Strike price for the put option
    payoffs = np.zeros(len(sim))  # initialize empty array for payoffs
    i = 0
    for vector in sim:
        S_T = vector[-1]  # price at maturity
        payoffs[i] = max(strike_price - S_T, 0)  # European put payoff
        i += 1
    plotting(payoffs, "European Put Option")
    print("Price of European Put Option: $" + str(
        option_price(payoffs)))

