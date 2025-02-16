#!/usr/bin/env python3
import sys
from collections import defaultdict

class ClusterMapper:
    def __init__(self):
        self.age_idx = 7        # age column index
        self.completion_idx = 2  # completion_percentage column index
        # Initialize k-means centroids (we'll use 5 age groups)
        self.centroids = [20, 30, 40, 50, 60]  # Initial centroids

    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.age_idx, self.completion_idx):
                    continue

                age = fields[self.age_idx]
                completion = fields[self.completion_idx]

                if age and age.isdigit() and 0 <= int(age) <= 100:
                    age = int(age)
                    completion = int(completion)
                    
                    # Find nearest centroid
                    nearest_centroid = min(self.centroids, 
                                        key=lambda x: abs(x - age))
                    
                    # Emit: key=centroid, value=(age,completion)
                    print(f'{nearest_centroid}\t{age},{completion}')
                    
            except Exception as e:
                continue

class ClusterReducer:
    def reduce(self):
        current_centroid = None
        ages = []
        completions = []
        
        print("Cluster\tSize\tAvg_Age\tAvg_Completion\tMin_Completion\tMax_Completion")
        
        for line in sys.stdin:
            try:
                centroid, values = line.strip().split('\t')
                age, completion = map(int, values.split(','))
                
                if current_centroid != centroid:
                    if current_centroid and ages:
                        self.output_stats(current_centroid, ages, completions)
                    current_centroid = centroid
                    ages = [age]
                    completions = [completion]
                else:
                    ages.append(age)
                    completions.append(completion)
                    
            except Exception as e:
                continue
                
        if current_centroid and ages:
            self.output_stats(current_centroid, ages, completions)

    def output_stats(self, centroid, ages, completions):
        size = len(ages)
        avg_age = sum(ages) / size
        avg_completion = sum(completions) / size
        min_completion = min(completions)
        max_completion = max(completions)
        
        print(f"{centroid}\t{size}\t{avg_age:.1f}\t{avg_completion:.1f}\t{min_completion}\t{max_completion}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = ClusterMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = ClusterReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 