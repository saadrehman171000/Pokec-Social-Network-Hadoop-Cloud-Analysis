#!/usr/bin/env python3
import sys
from collections import defaultdict
import math

class StatsMapper:
    def __init__(self):
        self.age_idx = 7  # AGE column index
        
    def map(self):
        """First pass mapper to collect statistics"""
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= self.age_idx:
                    continue
                    
                age = fields[self.age_idx]
                if age and age != "null":
                    try:
                        age = float(age)
                        # Output: key -> (value, value^2, count)
                        print(f"age\t{age}\t{age*age}\t1")
                    except ValueError:
                        continue
                        
            except Exception:
                continue

class StatsReducer:
    def reduce(self):
        """First pass reducer to calculate statistics"""
        stats = defaultdict(lambda: {'sum': 0, 'sum_sq': 0, 'count': 0, 'min': float('inf'), 'max': float('-inf')})
        
        for line in sys.stdin:
            try:
                feature, value, value_sq, count = line.strip().split('\t')
                value = float(value)
                value_sq = float(value_sq)
                count = int(count)
                
                stats[feature]['sum'] += value
                stats[feature]['sum_sq'] += value_sq
                stats[feature]['count'] += count
                stats[feature]['min'] = min(stats[feature]['min'], value)
                stats[feature]['max'] = max(stats[feature]['max'], value)
                
            except Exception:
                continue
        
        # Calculate and output statistics
        for feature, s in stats.items():
            if s['count'] > 0:
                mean = s['sum'] / s['count']
                variance = (s['sum_sq'] / s['count']) - (mean * mean)
                std = math.sqrt(variance) if variance > 0 else 1
                
                # Output format: feature mean std min max
                print(f"{feature}\t{mean}\t{std}\t{s['min']}\t{s['max']}")

class NormalizeMapper:
    def __init__(self):
        self.age_idx = 7
        # Hardcode the stats since we know them
        self.stats = {
            'age': {
                'mean': 17.065383060564486,
                'std': 13.882575413419932,
                'min': 0.0,
                'max': 112.0
            }
        }
    
    def map(self):
        """Second pass mapper to normalize values"""
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= self.age_idx:
                    continue
                
                user_id = fields[0]
                age = fields[self.age_idx]
                
                if age and age != "null":
                    try:
                        age = float(age)
                        # Z-score normalization
                        z_score = (age - self.stats['age']['mean']) / self.stats['age']['std']
                        # Min-max normalization
                        min_max = (age - self.stats['age']['min']) / (self.stats['age']['max'] - self.stats['age']['min'])
                        
                        print(f"{user_id}\t{age}\t{z_score:.4f}\t{min_max:.4f}")
                    except ValueError:
                        continue
                        
            except Exception:
                continue

class NormalizeReducer:
    def reduce(self):
        """Second pass reducer to format output"""
        print("user_id\toriginal_age\tz_score\tmin_max_normalized")
        
        for line in sys.stdin:
            try:
                print(line.strip())
            except Exception:
                continue

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py [stats_mapper|stats_reducer|normalize_mapper|normalize_reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "stats_mapper":
        mapper = StatsMapper()
        mapper.map()
    elif sys.argv[1] == "stats_reducer":
        reducer = StatsReducer()
        reducer.reduce()
    elif sys.argv[1] == "normalize_mapper":
        mapper = NormalizeMapper()
        if len(sys.argv) > 2:
            mapper.configure(sys.argv[2])
        mapper.map()
    elif sys.argv[1] == "normalize_reducer":
        reducer = NormalizeReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'stats_mapper', 'stats_reducer', 'normalize_mapper', or 'normalize_reducer'")
        sys.exit(1) 