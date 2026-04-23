import pandas as pd


def merge_all_data(user_health_data, supplement_usage, experiments, user_profiles):
    # Load datasets
    hd  = pd.read_csv(user_health_data)
    su  = pd.read_csv(supplement_usage)
    exp = pd.read_csv(experiments)
    up  = pd.read_csv(user_profiles)

    # Clean user_health_data
    # Parse dates to date format
    hd['date'] = pd.to_datetime(hd['date']).dt.date

    # Clean sleep_hours: strip trailing 'h' / 'H' then convert to float
    hd['sleep_hours'] = (
        hd['sleep_hours']
        .astype(str)
        .str.replace(r'[hH]$', '', regex=True)
        .astype(float)
    )

    # Clean supplement_usage
    su['date'] = pd.to_datetime(su['date']).dt.date

    # Convert dosage to grams (all values are in mg)
    su['dosage_grams'] = su.apply(
        lambda r: r['dosage'] / 1000 if r['dosage_unit'].strip().lower() == 'mg' else r['dosage'],
        axis=1
    )

    # Attach experiment name from experiments table
    su = su.merge(exp[['experiment_id', 'name']], on='experiment_id', how='left')
    su = su.rename(columns={'name': 'experiment_name'})

    # Add age-group to user_profiles
    def age_group(age):
        if pd.isna(age):
            return 'Unknown'
        age = int(age)
        if age < 18:
            return 'Under 18'
        elif age <= 25:
            return '18-25'
        elif age <= 35:
            return '26-35'
        elif age <= 45:
            return '36-45'
        elif age <= 55:
            return '46-55'
        elif age <= 65:
            return '56-65'
        else:
            return 'Over 65'

    up['user_age_group'] = up['age'].apply(age_group)

    # Merge health data with supplement usage (left join)
    # Keep all health-data rows; supplement rows for the same user+date are joined in
    su_cols = su[['user_id', 'date', 'experiment_name', 'supplement_name',
                  'dosage_grams', 'is_placebo']]
    merged = hd.merge(su_cols, on=['user_id', 'date'], how='left')

    # Days with no supplement record → 'No intake'
    merged['supplement_name'] = merged['supplement_name'].fillna('No intake')

    # Merge user profile information
    merged = merged.merge(
        up[['user_id', 'email', 'user_age_group']],
        on='user_id',
        how='left'
    )

    # Select and order final columns
    result = merged[[
        'user_id', 'date', 'email', 'user_age_group',
        'experiment_name', 'supplement_name', 'dosage_grams', 'is_placebo',
        'average_heart_rate', 'average_glucose', 'sleep_hours', 'activity_level'
    ]]

    return result
