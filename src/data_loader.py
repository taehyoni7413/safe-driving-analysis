import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import RISKY_BEHAVIORS

def generate_dummy_data(filepath="data/raw/sample_driving_data.xlsx", num_records=20):
    """
    Generate dummy data with the user-provided schema.
    Columns: 인덱스,차량번호,총운행거리(km),합계,과속,장기과속,급가속,급출발,급감속,급정지,급좌회전,급우회전,급유턴,급앞지르기,급진로변경
    """
    np.random.seed(42)
    
    data = []
    for i in range(1, num_records + 1):
        # Generate random values similar to the user's screenshot
        km = np.random.randint(1000, 150000)
        
        # Behaviors (using Korean keys initially to match Excel export format)
        row = {
            "인덱스": i,
            "차량번호": f"혁신{np.random.randint(10,99)}바{np.random.randint(1000,9999)}",
            "총운행거리(km)": km,
        }
        
        total_events = 0
        for b_key, b_val in RISKY_BEHAVIORS.items():
            # Random float/int values mostly small, some 0
            val = round(max(0, np.random.normal(1, 2)), 2) if np.random.random() > 0.3 else 0
            row[b_val['label_ko']] = val
            total_events += val
            
        row["합계"] = round(total_events, 2)
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_excel(filepath, index=False)
    return filepath

def load_data(filepath):
    """
    Load Excel data.
    Expected columns: 차량번호, and the 11 behavior columns.
    Maps Korean columns to internal English keys.
    """
    try:
        df = pd.read_excel(filepath)
        
        # Normalize column names (strip whitespace)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Column Mapping
        column_map = {v['label_ko']: k for k, v in RISKY_BEHAVIORS.items()}
        df = df.rename(columns=column_map)
        
        # Essential columns
        # Check for various forms of "Vehicle Number" if standard one missing
        if '차량번호' not in df.columns:
            # Try to find a column that contains "차량" and "번호"
            candidates = [c for c in df.columns if "차량" in str(c) and "번호" in str(c)]
            if candidates:
                df.rename(columns={candidates[0]: '차량번호'}, inplace=True)

        if '차량번호' in df.columns:
            # User request: Replace '00' with Index to make unique IDs
            # form: 혁신00바0000 -> 혁신{Index}바0000
            if '인덱스' in df.columns:
                def make_unique_id(row):
                    v_num = str(row['차량번호'])
                    idx = row['인덱스']
                    # Try to replace 00 with padded index
                    if '00' in v_num:
                        # Replace only the first occurrence or specific pattern?
                        # User said "00" (likely the middle part). 
                        # simpler approach: replace '00' with f"{idx:02d}"
                        return v_num.replace('00', f"{int(idx):02d}", 1)
                    else:
                        # Fallback: append index
                        return f"{v_num}_{int(idx)}"
                
                df['차량번호_Unique'] = df.apply(make_unique_id, axis=1)
                df['Driver ID'] = df['차량번호_Unique']
                df['Driver Name'] = df['차량번호_Unique']
            else:
                # If no index, just use vehicle number (might be duplicates)
                if 'Driver Name' not in df.columns:
                    df['Driver Name'] = df['차량번호']
                if 'Driver ID' not in df.columns:
                    df['Driver ID'] = df['차량번호']
        else:
            # Fallback if no identifier found
            df['Driver ID'] = 'Unknown'
            df['Driver Name'] = 'Unknown'

        # Ensure all expected columns exist (fill 0 if missing)
        for k in RISKY_BEHAVIORS.keys():
            if k not in df.columns:
                df[k] = 0
                
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
