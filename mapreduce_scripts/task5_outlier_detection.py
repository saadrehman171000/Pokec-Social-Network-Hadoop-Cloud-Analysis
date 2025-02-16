#!/usr/bin/env python3
import sys
from collections import defaultdict

class OutlierMapper:
    def __init__(self):
        # Define indices for relevant columns
        self.completion_idx = 2
        self.age_idx = 7
        self.height_idx = 8  # Assuming height is part of this field
        
    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.completion_idx, self.age_idx, self.height_idx):
                    continue
                    
                completion = fields[self.completion_idx]
                age = fields[self.age_idx]
                height_str = fields[self.height_idx]
                
                # Extract height if present (assuming format like "height:180")
                height = None
                if "height:" in height_str:
                    try:
                        height = int(height_str.split("height:")[1].split()[0])
                    except:
                        height = None
                
                # Emit values for each feature
                if completion and completion.isdigit():
                    print(f"completion\t{completion}")
                if age and age.isdigit():
                    print(f"age\t{age}")
                if height is not None:
                    print(f"height\t{height}")
                    
            except Exception as e:
                continue

class OutlierReducer:
    def reduce(self):
        current_feature = None
        values = []
        
        print("Feature\tQ1\tQ3\tIQR\tLower_Bound\tUpper_Bound\tOutliers_Count\tTotal_Count\tOutlier_Percentage")
        
        for line in sys.stdin:
            try:
                feature, value = line.strip().split('\t')
                value = float(value)
                
                if current_feature != feature:
                    if current_feature and values:
                        self.calculate_outliers(current_feature, values)
                    current_feature = feature
                    values = [value]
                else:
                    values.append(value)
                    
            except Exception as e:
                continue
                
        if current_feature and values:
            self.calculate_outliers(current_feature, values)
    
    def calculate_outliers(self, feature, values):
        values.sort()
        n = len(values)
        
        # Calculate quartiles
        q1_idx = n // 4
        q3_idx = (3 * n) // 4
        
        q1 = values[q1_idx]
        q3 = values[q3_idx]
        iqr = q3 - q1
        
        # Define bounds for outliers (using 1.5 * IQR rule)
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Count outliers
        outliers = [x for x in values if x < lower_bound or x > upper_bound]
        outlier_count = len(outliers)
        outlier_percentage = (outlier_count / n) * 100
        
        print(f"{feature}\t{q1:.1f}\t{q3:.1f}\t{iqr:.1f}\t{lower_bound:.1f}\t{upper_bound:.1f}\t{outlier_count}\t{n}\t{outlier_percentage:.2f}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = OutlierMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = OutlierReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 