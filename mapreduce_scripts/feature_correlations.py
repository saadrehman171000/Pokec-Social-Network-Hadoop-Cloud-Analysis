#!/usr/bin/env python3
import sys
from collections import defaultdict

class CorrelationMapper:
    def __init__(self):
        # Define indices for relevant columns
        self.completion_idx = 2  # completion_percentage
        self.age_idx = 7        # age
        self.gender_idx = 3     # gender
        self.region_idx = 4     # region
        self.public_idx = 1     # public profile indicator

    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.completion_idx, self.age_idx, self.gender_idx, self.region_idx):
                    continue

                completion = fields[self.completion_idx]
                if not completion.isdigit():
                    continue

                completion = int(completion)
                
                # Emit age correlations
                age = fields[self.age_idx]
                if age and age.isdigit() and 0 <= int(age) <= 100:
                    age_group = f"{(int(age) // 10) * 10}s"
                    print(f'AGE\t{age_group}\t{completion}')

                # Emit gender correlations (0=female, 1=male)
                gender = fields[self.gender_idx]
                if gender and gender.strip() in ['0', '1']:
                    gender_label = "Male" if gender.strip() == "1" else "Female"
                    print(f'GENDER\t{gender_label}\t{completion}')

                # Emit region correlations
                region = fields[self.region_idx]
                if region and region.strip():
                    main_region = region.split(',')[0].strip()
                    print(f'REGION\t{main_region}\t{completion}')

                # Emit public/private profile correlation
                public = fields[self.public_idx]
                if public and public.strip() in ['0', '1']:
                    profile_type = "Public" if public.strip() == "1" else "Private"
                    print(f'PROFILE_TYPE\t{profile_type}\t{completion}')

            except Exception as e:
                continue

class CorrelationReducer:
    def reduce(self):
        current_feature = None
        current_value = None
        completions = []
        
        stats = defaultdict(lambda: defaultdict(list))
        
        for line in sys.stdin:
            try:
                feature, value, completion = line.strip().split('\t')
                completion = int(completion)
                
                if current_feature == feature and current_value == value:
                    completions.append(completion)
                else:
                    if current_feature and current_value:
                        stats[current_feature][current_value] = completions
                    current_feature = feature
                    current_value = value
                    completions = [completion]
                    
            except Exception as e:
                continue
                
        if current_feature and current_value:
            stats[current_feature][current_value] = completions

        # Calculate and print statistics
        for feature in sorted(stats.keys()):
            print(f"\n{feature} Correlation with Completion Percentage:")
            print("Category\tCount\tAvg Completion\tMin\tMax\tMedian")
            print("-" * 70)
            
            for value in sorted(stats[feature].keys()):
                completions = stats[feature][value]
                if completions:
                    avg = sum(completions) / len(completions)
                    min_val = min(completions)
                    max_val = max(completions)
                    median = sorted(completions)[len(completions)//2]
                    
                    print(f"{value}\t{len(completions)}\t{avg:.2f}%\t{min_val}%\t{max_val}%\t{median}%")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = CorrelationMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = CorrelationReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 