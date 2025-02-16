#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import pickle

class ModelVisualizer:
    def __init__(self):
        self.feature_cols = ['completion_percentage', 'age', 'days_since_registration']
        self.models = {}
        self.data = None
        
    def load_models(self):
        """Load the trained models"""
        model_files = {
            'Random Forest': 'results/models/rf_model.pkl',
            'Gradient Boosting': 'results/models/gb_model.pkl'
        }
        
        for name, path in model_files.items():
            with open(path, 'rb') as f:
                self.models[name] = pickle.load(f)
    
    def load_data(self):
        """Load the prepared data"""
        self.data = pd.read_csv('results/models/prepared_data.txt', sep='\t')
    
    def plot_feature_importance(self):
        """Plot feature importance comparison"""
        plt.figure(figsize=(12, 6))
        
        importances = []
        for name, model in self.models.items():
            imp = pd.DataFrame({
                'Feature': self.feature_cols,
                'Importance': model.feature_importances_,
                'Model': name
            })
            importances.append(imp)
        
        imp_df = pd.concat(importances)
        
        sns.barplot(data=imp_df, x='Feature', y='Importance', hue='Model')
        plt.title('Feature Importance Comparison')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('results/models/feature_importance.png')
        plt.close()
    
    def plot_roc_curves(self):
        """Plot ROC curves for both models"""
        plt.figure(figsize=(10, 6))
        
        # Get test data
        test_data = self.data[self.data['dataset'] == 'test']
        X_test = test_data[self.feature_cols].values
        y_test = test_data['target'].values
        
        for name, model in self.models.items():
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves Comparison')
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig('results/models/roc_curves.png')
        plt.close()
    
    def plot_confusion_matrices(self):
        """Plot confusion matrices for both models"""
        test_data = self.data[self.data['dataset'] == 'test']
        X_test = test_data[self.feature_cols].values
        y_test = test_data['target'].values
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        for i, (name, model) in enumerate(self.models.items()):
            y_pred = model.predict(X_test)
            cm = confusion_matrix(y_test, y_pred)
            
            sns.heatmap(cm, annot=True, fmt='d', ax=axes[i])
            axes[i].set_title(f'{name} Confusion Matrix')
            axes[i].set_xlabel('Predicted')
            axes[i].set_ylabel('Actual')
        
        plt.tight_layout()
        plt.savefig('results/models/confusion_matrices.png')
        plt.close()
    
    def plot_feature_distributions(self):
        """Plot feature distributions by target class"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        for i, feature in enumerate(self.feature_cols):
            sns.boxplot(data=self.data, x='target', y=feature, ax=axes[i])
            axes[i].set_title(f'{feature} Distribution by Target')
        
        plt.tight_layout()
        plt.savefig('results/models/feature_distributions.png')
        plt.close()

if __name__ == "__main__":
    visualizer = ModelVisualizer()
    visualizer.load_models()
    visualizer.load_data()
    
    # Generate all visualizations
    visualizer.plot_feature_importance()
    visualizer.plot_roc_curves()
    visualizer.plot_confusion_matrices()
    visualizer.plot_feature_distributions()
    
    print("Visualizations have been saved in results/models/ directory") 