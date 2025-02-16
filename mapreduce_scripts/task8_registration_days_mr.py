#!/usr/bin/env python3
import sys
from datetime import datetime

class RegistrationMapper:
    def __init__(self):
        self.registration_idx = 6  # Registration date column
        self.last_login_idx = 5    # Last login column
        
    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str.strip(), '%Y-%m-%d %H:%M:%S.%f')
        except:
            return None
    
    def map(self):
        for line in sys.stdin:
            try:
                fields = line.strip().split('\t')
                if len(fields) <= max(self.registration_idx, self.last_login_idx):
                    continue
                
                user_id = fields[0]
                last_login = self.parse_date(fields[self.last_login_idx])
                registration = self.parse_date(fields[self.registration_idx])
                
                if last_login and registration:
                    days = (last_login - registration).days
                    print(f"{user_id}\t{days}")
                    
            except Exception:
                continue

class RegistrationReducer:
    def reduce(self):
        print("user_id\tdays_since_registration")
        
        for line in sys.stdin:
            try:
                user_id, days = line.strip().split('\t')
                print(f"{user_id}\t{days}")
            except Exception:
                continue

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py [mapper|reducer]")
        sys.exit(1)
        
    if sys.argv[1] == "mapper":
        mapper = RegistrationMapper()
        mapper.map()
    elif sys.argv[1] == "reducer":
        reducer = RegistrationReducer()
        reducer.reduce()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'")
        sys.exit(1) 