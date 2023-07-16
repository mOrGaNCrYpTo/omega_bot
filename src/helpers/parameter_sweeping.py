from sklearn.model_selection import ParameterGrid

# Define the parameter grid
param_grid = {
    'smaPeriod': range(10, 100, 10),
    'trailingStopPct': [0.01, 0.02, 0.03, 0.04, 0.05]
}

# Create a grid of parameters to search over
grid = ParameterGrid(param_grid)

best_score = float('-inf')
best_params = None

# For each combination of parameters...
for params in grid:
    # Create and run the strategy
    strategy = SMACrossover(feed, "AAPL", params['smaPeriod'], params['trailingStopPct'])
    strategy.run()
    
    # Calculate some performance metric
    score = calculate_performance(strategy)
    
    # If this score is better than the best seen so far, remember it
    if score > best_score:
        best_score = score
        best_params = params

print(f'Best parameters: {best_params}')
