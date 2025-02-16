#!/usr/bin/env python3
import sys
from collections import defaultdict

class VisualizationMapper:
    def __init__(self):
        self.completion_idx = 2
        self.age_idx = 7
        self.color_idx = 8  # Assuming favorite_color is in this column
        self.height_weight_idx = 8  # Column containing height and weight info

    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.completion_idx, self.age_idx, self.color_idx):
                    continue

                completion = fields[self.completion_idx]
                if not completion.isdigit():
                    continue
                completion = int(completion)

                # Emit color vs completion data for boxplots
                height_weight = fields[self.height_weight_idx]
                if height_weight and 'cm' in height_weight:
                    try:
                        height = int(height_weight.split('cm')[0].strip())
                        print(f'HEIGHT\t{height}\t{completion}')
                    except:
                        pass

                # Emit age vs completion for correlation
                age = fields[self.age_idx]
                if age and age.isdigit() and 0 <= int(age) <= 100:
                    print(f'AGE\t{age}\t{completion}')

            except Exception as e:
                continue

class VisualizationReducer:
    def reduce(self):
        current_feature = None
        stats = defaultdict(list)
        
        for line in sys.stdin:
            try:
                feature, value, completion = line.strip().split('\t')
                value = float(value)
                completion = int(completion)
                
                stats[feature].append((value, completion))
                    
            except Exception as e:
                continue

        # Calculate statistics for each feature
        for feature in sorted(stats.keys()):
            print(f"\n{feature} vs Completion Percentage Statistics:")
            print("Value Range\tCount\tAvg Completion\tMin\tMax\tQ1\tMedian\tQ3")
            print("-" * 80)
            
            # Group data into ranges
            data = stats[feature]
            data.sort(key=lambda x: x[0])  # Sort by value
            
            # Create value ranges
            if feature == 'HEIGHT':
                range_size = 5  # 5cm ranges
            else:
                range_size = 10  # 10 year ranges
            
            ranges = defaultdict(list)
            for value, completion in data:
                range_start = (value // range_size) * range_size
                ranges[range_start].append(completion)
            
            # Calculate statistics for each range
            for range_start in sorted(ranges.keys()):
                completions = sorted(ranges[range_start])
                n = len(completions)
                if n > 0:
                    range_end = range_start + range_size
                    avg = sum(completions) / n
                    min_val = completions[0]
                    max_val = completions[-1]
                    q1 = completions[n//4] if n >= 4 else min_val
                    median = completions[n//2] if n >= 2 else min_val
                    q3 = completions[3*n//4] if n >= 4 else max_val
                    
                    print(f"{range_start}-{range_end}\t{n}\t{avg:.1f}%\t{min_val}%\t{max_val}%\t{q1}%\t{median}%\t{q3}%")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = VisualizationMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = VisualizationReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 