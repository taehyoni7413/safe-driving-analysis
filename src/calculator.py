import pandas as pd
from config import RISKY_BEHAVIORS, CO2_EMISSION, FUEL_PRICE

def calculate_impact(driver_stats_df):
    """
    Calculates fuel wasted and CO2 emissions based on behavior counts.
    """
    df = driver_stats_df.copy()
    
    # Initialize columns
    df['Estimated Fuel Wasted (L)'] = 0.0
    
    # Calculate Fuel Loss
    for behavior, details in RISKY_BEHAVIORS.items():
        loss_per_event_l = details['fuel_loss_ml'] / 1000.0
        if behavior in df.columns:
            df['Estimated Fuel Wasted (L)'] += df[behavior] * loss_per_event_l
            
    # Calculate CO2 Emission (kg)
    # We need to compute this per row based on 'Fuel Type'
    def get_co2_factor(fuel_type):
        return CO2_EMISSION.get(fuel_type, 2.3) # Default to Gasoline if unknown
        
    df['CO2 Emission (kg)'] = df.apply(
        lambda row: row['Estimated Fuel Wasted (L)'] * get_co2_factor(row['Fuel Type']), axis=1
    )
    
    # Calculate Financial Loss
    def get_fuel_price(fuel_type):
        return FUEL_PRICE.get(fuel_type, 1600)
        
    df['Financial Loss (KRW)'] = df.apply(
        lambda row: row['Estimated Fuel Wasted (L)'] * get_fuel_price(row['Fuel Type']), axis=1
    )
    
    return df
