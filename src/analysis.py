import pandas as pd
from config import RISKY_BEHAVIORS

def analyze_driver_risk(df):
    """
    Aggregates risk behaviors per driver.
    Returns a DataFrame with total counts and a safety score.
    """
    # Group by Driver
    dataset = df.copy()
    
    # Ensure all behavior columns exist, fill 0 if missing
    for behavior in RISKY_BEHAVIORS.keys():
        if behavior not in dataset.columns:
            dataset[behavior] = 0
            
    # Calculate Total Penalty Points per row
    dataset['Total Penalty'] = 0
    for behavior, details in RISKY_BEHAVIORS.items():
        dataset['Total Penalty'] += dataset[behavior] * details['penalty']
        
    # Check if 'Fuel Type' exists, if not default to 'Diesel' (common for commercial trucks) or make it generic
    if 'Fuel Type' not in dataset.columns:
        dataset['Fuel Type'] = 'Diesel' # Assumption based on context ("혁신..바.." suggests commercial/bus/truck)

    # Since the input seems to be already aggregated per vehicle (summary report),
    # we might not need to groupby if each row is unique vehicle.
    # However, to be safe, we group by ID.
    group_cols = ['Driver ID', 'Driver Name', 'Fuel Type']
    # Filter only cols that exist
    group_cols = [c for c in group_cols if c in dataset.columns]
    
    driver_stats = dataset.groupby(group_cols).agg(
        {b: 'sum' for b in RISKY_BEHAVIORS.keys()}
    )
    
    # Add Total Penalty sum
    driver_stats['Total Penalty Score'] = dataset.groupby(group_cols)['Total Penalty'].sum()
    
    # Calculate Safety Score (Simple formula: 100 - (Total Penalty / Days * factor) or just raw 100 - penalty for now)
    # For this version, let's assume a baseline of 100 and subtract penalty points scaled down, 
    # or just keep it simple: Max 100, Min 0.
    # Let's use: Score = max(0, 100 - (Total Penalty * 0.1)) for demonstration
    driver_stats['Safety Score'] = driver_stats['Total Penalty Score'].apply(lambda x: max(0, 100 - (x * 0.1))) # Simple heuristic
    
    return driver_stats.reset_index()
