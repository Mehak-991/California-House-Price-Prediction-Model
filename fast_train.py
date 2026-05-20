import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor

# Load Data
housing = pd.read_csv("housing.csv")

# Create Income Categories for Stratified Split
housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                               labels=[1, 2, 3, 4, 5])

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

# Separate features and labels
housing_train = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

# Pipeline configuration
housing_num = housing_train.drop("ocean_proximity", axis=1)
num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('std_scaler', StandardScaler()),
])

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(), cat_attribs),
])

# Fit Full Pipeline
housing_prepared = full_pipeline.fit_transform(housing_train)

print('Training RandomForestRegressor...')
# Train Model
forest_reg = RandomForestRegressor(n_estimators=30, max_features=6, random_state=42) # Best params from grid search visually
forest_reg.fit(housing_prepared, housing_labels)

# Save the Pipeline and Model
joblib.dump(full_pipeline, 'preprocessing_pipeline.joblib')
joblib.dump(forest_reg, 'house_price_model.joblib')

print('Fast training done and files saved!')
