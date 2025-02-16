# Pokec Social Network Analysis using MapReduce

## Overview
This project leverages the **Hadoop MapReduce** framework to analyze **Slovakia's largest social network, Pokec**. The goal is to gain insights into user behavior, profile completion patterns, and demographic characteristics. By utilizing **over 1.6 million user profiles**, this analysis involves processing vast amounts of data, including user features like age, gender, region, hobbies, and more.

The project aims to implement MapReduce logic for demographic analysis, feature engineering, machine learning model training, and clustering of user data. It also includes predictive modeling to analyze and predict **completion_percentage** of user profiles based on demographic and behavioral attributes.

## Dataset
The analysis uses the **Pokec Social Network Dataset** provided by **SNAP (Stanford Network Analysis Project)**. The dataset contains anonymized user data from the social network, including demographic information and behavioral attributes.

- **Source**: [Pokec Social Network Dataset](https://snap.stanford.edu/data/soc-Pokec.html)
- **Size**: 1,632,803 nodes (users), 30,622,564 edges
- **Features**: Age, gender, region, hobbies, interests, education, etc.
- **Language**: Slovak

## Project Structure
```plaintext
├── mapreduce_scripts/
│   ├── model_prep.py # Data preparation for modeling
│   ├── model_training.py # Model training implementation
│   ├── model_visualization.py # Visualization scripts
│   └── task.py # Task-specific implementations
├── results/
│   ├── models/ # Trained model files(visualizations+summaries)
│   ├── task/ # Task-wise results(visualizations+summaries)
└── README.md
```

## Key Features

### Demographic Analysis
- User feature analysis (age, gender, region)
- Statistical reporting
- Visualization of distributions

### Feature Engineering
- Categorical variable encoding
- Multi-label processing
- Temporal feature creation

### Machine Learning Models
- Random Forest Classifier
- Gradient Boosting Classifier
- Model performance comparison

### Clustering
- K-means clustering to group users based on age and completion rates
- Outlier detection and handling

## Implementation Details

### Prerequisites

Ensure you have the following tools and libraries installed:

- **Python 3.x**: The primary language for the project.
- **Hadoop 3.2.4**: For distributed computing and MapReduce operations.

Required Python packages:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn
```

### Setup Instructions

#### Clone the Repository:
```bash
git clone https://github.com/yourusername/pokec-analysis.git
```

#### Download the Dataset:
Download the dataset from SNAP.

#### Hadoop Configuration:
Start Hadoop services:

```bash
# Start HDFS and YARN
start-dfs.sh
start-yarn.sh
```

#### Run the Analysis:
Example command to run demographic analysis:
```bash
python mapreduce_scripts/task1_demographics.py
```

## Task Breakdown

### Task 1: Demographic Analysis
- Analyzed user features such as age, gender, and region.
- Generated statistical reports and visualized distributions.

### Task 2: Correlation Analysis
- Investigated correlations between completion_percentage and features like age, gender, and region.

### Task 3: Visualizations
- Generated boxplots, heatmaps, and other visualizations to represent the correlation between various features and completion_percentage.

### Task 4: K-means Clustering
- Used K-means clustering to group users based on age and completion_percentage.
- Analyzed the differences in completion rates across clusters.

### Task 5: Outlier Detection
- Detected outliers in user age and completion_percentage.
- Plotted outliers and used statistical methods for handling them.

### Task 6: Categorical Variable Encoding
- Encoded categorical variables like gender, region, and eye_color using one-hot encoding.

### Task 7: Multi-label Mapping
- Processed multi-label columns (e.g., hobbies, spoken_languages) using MapReduce word frequency counting.
- Visualized the distribution of different hobbies and sports categories.

### Task 8: Registration Days Calculation
- Computed days_since_registration from the registration and last login dates.

### Task 9: Age Statistics and Normalization
- Collected and analyzed age statistics, and applied Z-score normalization and min-max normalization.

## Model Building (HDFS-based)

- Implemented Random Forest and Gradient Boosting classifiers.
- Split data into training, testing, and validation sets and dropped non-predictive features (like user_id).
- Evaluated models and saved results.

## Key Results

### Model Performance

#### Random Forest Classifier:
- Accuracy: 62.19%
- Precision: 69.97%
- Recall: 75.14%
- F1 Score: 72.46%

#### Gradient Boosting Classifier:
- Accuracy: 67.41%
- Precision: 69.31%
- Recall: 91.12%
- F1 Score: 78.73%

### Feature Importance
- **days_since_registration**: Most significant predictor.
- **age**: Secondary importance.
- **completion_percentage**: Tertiary importance.

### Visualizations
The project includes various visualizations for a clearer interpretation of the analysis:
- **ROC curves**: To compare model performance.
- **Feature importance plots**: To visualize the significance of each feature.
- **Confusion matrices**: For model evaluation.
- **Feature distributions**: To analyze feature characteristics across target classes.


## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- **Stanford Network Analysis Project (SNAP)** for the dataset.
- **Hadoop community** for the distributed computing framework.