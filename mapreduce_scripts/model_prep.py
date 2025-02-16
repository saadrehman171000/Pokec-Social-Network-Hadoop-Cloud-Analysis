import sys
import random
from datetime import datetime

class DataPrepMapper:
    def __init__(self):
        # Define column indices
        self.columns = {
            'user_id': 0,
            'public': 1,
            'completion_percentage': 2,
            'gender': 3,
            'region': 4,
            'last_login': 5,
            'registration': 6,
            'age': 7,
            'body': 8,
            'I_am_working_in_field': 9
            # Add other relevant columns
        }
        
        # Define features to use
        self.feature_cols = [
            'completion_percentage',
            'age',
            'days_since_registration'  # We'll calculate this
        ]
        
        # Target variable (let's predict if profile is public)
        self.target_col = 'public'
        
        # Set random seed for consistent splits
        random.seed(42)
    
    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str.strip(), '%Y-%m-%d %H:%M:%S.%f')
        except:
            return None
    
    def map(self):
        """Map input data to features and split into train/test/validation"""
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                
                # Calculate days since registration
                last_login = self.parse_date(fields[self.columns['last_login']])
                registration = self.parse_date(fields[self.columns['registration']])
                
                if last_login and registration:
                    days_since_reg = (last_login - registration).days
                else:
                    continue
                
                # Get features
                features = {
                    'completion_percentage': float(fields[self.columns['completion_percentage']]),
                    'age': float(fields[self.columns['age']]) if fields[self.columns['age']] != "null" else 0,
                    'days_since_registration': days_since_reg
                }
                
                # Get target (convert to binary)
                target = 1 if fields[self.columns[self.target_col]] == "1" else 0
                
                # Randomly assign to train/test/validation
                split = random.random()
                if split < 0.7:  # 70% training
                    dataset = "train"
                elif split < 0.85:  # 15% testing
                    dataset = "test"
                else:  # 15% validation
                    dataset = "validation"
                
                # Output format: dataset \t target \t feature1 \t feature2 \t ...
                feature_values = [str(features[col]) for col in self.feature_cols]
                print(f"{dataset}\t{target}\t{'\t'.join(feature_values)}")
                
            except Exception as e:
                continue

class DataPrepReducer:
    def reduce(self):
        """Write data in format suitable for model training"""
        current_dataset = None
        
        for line in sys.stdin:
            try:
                parts = line.strip().split('\t')
                dataset = parts[0]
                
                # Print header for each new dataset
                if dataset != current_dataset:
                    if current_dataset is None:
                        print("dataset\ttarget\tcompletion_percentage\tage\tdays_since_registration")
                    current_dataset = dataset
                
                # Output the line as is
                print(line.strip())
                
            except Exception:
                continue

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = DataPrepMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = DataPrepReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1)