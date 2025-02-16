#!/usr/bin/env python3
from collections import defaultdict
import sys

class DemographicsMapper:
    def __init__(self):
        # Update indices based on actual file structure
        self.age_idx = 7        # AGE is in column 8
        self.gender_idx = 3     # gender is in column 4 (0=female, 1=male)
        self.region_idx = 4     # region is in column 5

    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.age_idx, self.gender_idx, self.region_idx):
                    continue
                
                # Extract and validate age
                age = fields[self.age_idx]
                if age and age.isdigit() and 0 <= int(age) <= 100:
                    age_group = (int(age) // 10) * 10
                    print(f'AGE\t{age_group}\t1')
                
                # Extract and validate gender (0=female, 1=male)
                gender = fields[self.gender_idx]
                if gender and gender.strip():
                    gender_label = "Male" if gender.strip() == "1" else "Female"
                    print(f'GENDER\t{gender_label}\t1')
                
                # Extract and validate region
                region = fields[self.region_idx]
                if region and region.strip():
                    # Extract just the main region name before the comma
                    main_region = region.split(',')[0].strip()
                    print(f'REGION\t{main_region}\t1')
                    
            except Exception as e:
                continue

class DemographicsReducer:
    def reduce(self):
        current_category = None
        current_key = None
        current_count = 0
        
        stats = defaultdict(lambda: defaultdict(int))
        
        for line in sys.stdin:
            try:
                category, key, count = line.strip().split('\t')
                count = int(count)
                
                if current_category == category and current_key == key:
                    current_count += count
                else:
                    if current_category and current_key:
                        stats[current_category][current_key] = current_count
                    current_category = category
                    current_key = key
                    current_count = count
                    
            except Exception as e:
                continue
                
        if current_category and current_key:
            stats[current_category][current_key] = current_count
            
        # Print results with total counts
        for category in sorted(stats.keys()):
            total = sum(stats[category].values())
            print(f"\n{category} Distribution (Total: {total}):")
            for key in sorted(stats[category].keys()):
                percentage = (stats[category][key] / total) * 100
                print(f"{key}: Count={stats[category][key]} ({percentage:.2f}%)")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = DemographicsMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = DemographicsReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 