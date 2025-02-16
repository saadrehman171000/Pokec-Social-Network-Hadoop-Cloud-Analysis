import sys
from collections import defaultdict
import re

class MultilabelMapper:
    def __init__(self):
        self.hobbies_idx = 11
        self.sports_idx = 39
        
        # Common hobby categories in Slovak
        self.hobby_categories = {
            'music': re.compile(r'(hudba|spev|tanec|koncert)'),
            'sports': re.compile(r'(sport|cvicenie|pohyb)'),
            'travel': re.compile(r'(cestovanie|turistika)'),
            'photography': re.compile(r'(foto|fotografovanie)'),
            'reading': re.compile(r'(citanie|knihy)'),
            'cooking': re.compile(r'(varenie|pecenie)'),
            'gardening': re.compile(r'(zahrada|pestovanie)'),
            'shopping': re.compile(r'(nakupovanie|moda)'),
            'art': re.compile(r'(malovanie|kreslenie)'),
            'social': re.compile(r'(priatelia|party|zabava)')
        }

        # Sports categories
        self.sports_categories = {
            'ball_sports': re.compile(r'(futbal|volejbal|basketbal|tenis)'),
            'winter_sports': re.compile(r'(lyzovanie|hokej|korculovanie)'),
            'fitness': re.compile(r'(posilnovanie|fitnes|aerobik|behanie)'),
            'cycling': re.compile(r'(bicykel|cyklistika)'),
            'swimming': re.compile(r'(plavanie)')
        }
    
    def map(self):
        sample_count = 0
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.hobbies_idx, self.sports_idx):
                    continue
                
                # Print first 1000 samples of all fields to understand the data better
                if sample_count < 1000:
                    for i, field in enumerate(fields):
                        if field and field != "null":
                            print(f"sample\t{i}\t{field}")
                    sample_count += 1
                
                # Process hobbies
                hobbies = fields[self.hobbies_idx]
                if hobbies and hobbies != "null":
                    for category, pattern in self.hobby_categories.items():
                        if pattern.search(hobbies.lower()):
                            print(f"hobby\t{category}")
                            break
                
                # Process sports
                sports = fields[self.sports_idx]
                if sports and sports != "null":
                    for category, pattern in self.sports_categories.items():
                        if pattern.search(sports.lower()):
                            print(f"sport\t{category}")
                            break
                            
            except Exception:
                continue

class MultilabelReducer:
    def reduce(self):
        current_type = None
        label_counts = defaultdict(int)
        field_samples = defaultdict(list)  # To store samples for each field
        
        print("Type\tLabel\tCount\tPercentage")
        
        for line in sys.stdin:
            try:
                parts = line.strip().split('\t')
                label_type = parts[0]
                
                if label_type == 'sample':
                    # Store field samples: field_index -> value
                    field_idx = int(parts[1])
                    field_value = parts[2]
                    if len(field_samples[field_idx]) < 10:  # Store first 10 samples per field
                        field_samples[field_idx].append(field_value)
                    continue
                
                label = parts[1]
                if current_type and current_type != label_type:
                    self.output_frequencies(current_type, label_counts)
                    label_counts.clear()
                
                current_type = label_type
                label_counts[label] += 1
                    
            except Exception as e:
                continue
                
        if current_type:
            self.output_frequencies(current_type, label_counts)
        
        # Output field samples
        print("\nField Samples:")
        print("=" * 80)
        for field_idx in sorted(field_samples.keys()):
            print(f"\nField {field_idx}:")
            print("-" * 40)
            for sample in field_samples[field_idx]:
                print(sample)
    
    def output_frequencies(self, label_type, counts):
        total = sum(counts.values())
        if total == 0:
            return
            
        # Sort and output top results
        sorted_labels = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        for label, count in sorted_labels:
            if count >= 100:  # Increased threshold for significance
                percentage = (count / total) * 100
                print(f"{label_type}\t{label}\t{count}\t{percentage:.2f}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = MultilabelMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = MultilabelReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1)