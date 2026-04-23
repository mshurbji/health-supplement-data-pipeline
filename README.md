Health & Supplement Data Pipeline

This project builds a simple data engineering pipeline that cleans and merges multiple datasets related to user health, supplement usage, and experiments. The final output is a single dataset that combines all relevant information for analysis.

---

## What this project does

* Cleans and standardizes raw data
* Converts dates into proper format
* Converts dosage units (mg → grams)
* Handles missing values
* Creates age groups from user age
* Merges multiple datasets into one
* Ensures one row per user per day (with multiple entries if multiple supplements exist)

---

## Project structure

* `data/` → input datasets (CSV files)
* `src/` → main data processing logic
* `assets/` → images (e.g. schema)
* `output/` → reserved for future outputs

---

## How to run

Install requirements:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```python
from src.merge_data import merge_all_data

df = merge_all_data(
    "data/user_health_data.csv",
    "data/supplement_usage.csv",
    "data/experiments.csv",
    "data/user_profiles.csv"
)
```

---

## Notes

* This project was built as part of a practical Data Engineering exam
* It demonstrates data cleaning, transformation, and integration
* The output dataset can be used for analysis and insights
* Sample data is included for testing
