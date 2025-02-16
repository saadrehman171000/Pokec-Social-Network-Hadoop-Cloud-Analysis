#!/usr/bin/env python3
import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

class ModelTrainer:
    def __init__(self):
        self.feature_cols = ['completion_percentage', 'age', 'days_since_registration']
        self.models = {
            'rf': RandomForestClassifier(n_estimators=100, random_state=42),
            'gb': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        self.X_train = []
        self.y_train = []
        self.X_test = []
        self.y_test = []
        self.X_val = []
        self.y_val = []
    
    def process_data(self, input_file):
        """Read and process the prepared data"""
        header = True
        for line in open(input_file):
            if header:
                header = False
                continue
                
            parts = line.strip().split('\t')
            dataset = parts[0]
            target = int(parts[1])
            features = [float(x) for x in parts[2:]]
            
            if dataset == 'train':
                self.X_train.append(features)
                self.y_train.append(target)
            elif dataset == 'test':
                self.X_test.append(features)
                self.y_test.append(target)
            else:  # validation
                self.X_val.append(features)
                self.y_val.append(target)
    
    def train_and_evaluate(self):
        """Train models and evaluate performance"""
        results = {}
        
        # Convert to numpy arrays
        X_train = np.array(self.X_train)
        y_train = np.array(self.y_train)
        X_test = np.array(self.X_test)
        y_test = np.array(self.y_test)
        X_val = np.array(self.X_val)
        y_val = np.array(self.y_val)
        
        print("\nModel Training and Evaluation Results")
        print("=" * 80)
        
        for name, model in self.models.items():
            print(f"\n{name.upper()} Classifier:")
            print("-" * 40)
            
            # Train model
            model.fit(X_train, y_train)
            
            # Save model
            with open(f'results/models/{name}_model.pkl', 'wb') as f:
                pickle.dump(model, f)
            
            # Evaluate on test set
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            metrics = {
                'Accuracy': accuracy_score(y_test, y_pred),
                'Precision': precision_score(y_test, y_pred),
                'Recall': recall_score(y_test, y_pred),
                'F1 Score': f1_score(y_test, y_pred)
            }
            
            # Print metrics
            for metric, value in metrics.items():
                print(f"{metric}: {value:.4f}")
            
            # Feature importance
            print("\nFeature Importance:")
            importances = model.feature_importances_
            for feat, imp in zip(self.feature_cols, importances):
                print(f"{feat}: {imp:.4f}")
            
            results[name] = metrics
        
        return results

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.process_data('results/models/prepared_data.txt')
    results = trainer.train_and_evaluate() 