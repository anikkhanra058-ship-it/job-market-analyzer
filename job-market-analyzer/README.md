
A Python data analysis project that explores job listings,
skill mentions, locations, and salary ranges.

The dataset used in this project is synthetic and is intended
for learning and demonstration purposes.

## Features
- Data inspection and cleaning with Pandas
- Job title and location analysis
- Skill frequency analysis
- Salary range analysis
- SQL analysis using MySQL
- Visualizations using Matplotlib
- Exportable summary metrics

## Technologies
- Python
- Pandas and NumPy
- MySQL
- Matplotlib
- JupyterLab

## Project Structure
- data/: Raw and cleaned datasets
- notebooks/: Analysis notebook
- outputs/: Charts and summary CSV

## Outputs
- Top skills chart
- Top job titles chart
- Top cities chart
- Salary distribution chart
- Project summary CSV

## Limitations
The dataset is synthetic, so the results do not represent
actual job market demand or real-world salary benchmarks.

## Author
Add Anik Khanra

A basic job-title classifier built using scikit-learn.

1. Create broad job categories from job titles using simple rules.
2. Split the dataset into training and testing sets.
3. Convert job titles into TF-IDF features.
4. Train a Logistic Regression classifier.
5. Evaluate predictions using accuracy, precision, recall, and F1-score.
6. Save the trained model and TF-IDF vectorizer with joblib.

- outputs/job_category_model.pkl
- outputs/tfidf_vectorizer.pkl

The categories were generated using title-based rules. The model
therefore learns to reproduce those rules, rather than learning
independently verified job classifications. The dataset is synthetic,
so the results should not be interpreted as real-world job-market insights.
