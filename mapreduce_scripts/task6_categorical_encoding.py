#!/usr/bin/env python3
import sys
from collections import defaultdict

class EncodingMapper:
    def __init__(self):
        # Define indices for categorical columns
        self.gender_idx = 3
        self.region_idx = 4
        self.eye_color_idx = 9
        
        # Define valid categories for each feature
        self.valid_genders = {'0', '1'}  # 0: male, 1: female
        self.valid_eye_colors = {'0', '1', '2', '3'}  # Different eye colors
        
    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.gender_idx, self.region_idx, self.eye_color_idx):
                    continue
                
                # Extract categorical values
                gender = fields[self.gender_idx]
                region = fields[self.region_idx]
                eye_color = fields[self.eye_color_idx]
                
                # Emit for gender encoding
                if gender in self.valid_genders:
                    print(f"gender\t{gender}")
                
                # Emit for region encoding
                if region:
                    print(f"region\t{region}")
                
                # Emit for eye color encoding
                if eye_color in self.valid_eye_colors:
                    print(f"eye_color\t{eye_color}")
                    
            except Exception as e:
                continue

class EncodingReducer:
    def reduce(self):
        current_feature = None
        value_counts = defaultdict(int)
        total_count = 0
        
        # Header for the encoding summary
        print("Feature\tCategory\tCount\tPercentage\tEncoding")
        
        for line in sys.stdin:
            try:
                feature, value = line.strip().split('\t')
                
                if current_feature != feature:
                    if current_feature:
                        self.output_encoding(current_feature, value_counts, total_count)
                    current_feature = feature
                    value_counts.clear()
                    total_count = 0
                
                value_counts[value] += 1
                total_count += 1
                    
            except Exception as e:
                continue
                
        if current_feature:
            self.output_encoding(current_feature, value_counts, total_count)
    
    def output_encoding(self, feature, value_counts, total_count):
        # Sort categories by count
        sorted_categories = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Create one-hot encoding mapping
        encoding = {cat: idx for idx, (cat, _) in enumerate(sorted_categories)}
        
        # Output statistics and encoding for each category
        for category, count in sorted_categories:
            percentage = (count / total_count) * 100
            encoded_value = [0] * len(sorted_categories)
            encoded_value[encoding[category]] = 1
            encoded_str = ','.join(map(str, encoded_value))
            
            print(f"{feature}\t{category}\t{count}\t{percentage:.2f}\t{encoded_str}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = EncodingMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = EncodingReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 