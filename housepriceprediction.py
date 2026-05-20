#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Hello, World!")


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# The 'r' before the string is important for Windows paths
file_path = "housing.csv"

# Load the data from your local file into a DataFrame called 'housing'
try:
    housing = pd.read_csv(file_path)
    print("✅ Dataset loaded successfully!")
    
    # Display the first 5 rows to confirm it's loaded correctly
    print("First 5 rows of your dataset:")
    print(housing.head())
    
except FileNotFoundError:
    print("❌ Error: The file was not found at the specified path.")
    print("Please make sure the path is correct and the file exists.")


# In[3]:


housing.info()


# In[4]:


housing["ocean_proximity"].value_counts()


# In[5]:


housing.describe()


# In[6]:


import matplotlib.pyplot as plt

housing.hist(bins=50, figsize=(20, 15))
pass # plt.show()


# In[7]:


import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

# 1. Create an income category from the continuous median income data
housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                               labels=[1, 2, 3, 4, 5])

# 2. Perform the stratified split
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

# 3. Remove the temporary 'income_cat' attribute
for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

print("✅ Training and test sets created successfully!")
print(f"You have {len(strat_train_set)} samples in your training set.")
print(f"You have {len(strat_test_set)} samples in your test set.")


# In[8]:


# Create a copy of the training set for exploration
housing = strat_train_set.copy()


# In[9]:


housing.plot(kind="scatter", x="longitude", y="latitude")
pass # plt.show()


# In[10]:


housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)
pass # plt.show()


# In[11]:


housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
    s=housing["population"]/100, label="population", figsize=(10,7),
    c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True,
)
plt.legend()
pass # plt.show()


# In[12]:


# Calculate the correlation matrix
corr_matrix = housing.corr(numeric_only=True)

# See how much each attribute correlates with the median house value
corr_matrix["median_house_value"].sort_values(ascending=False)


# In[13]:


from pandas.plotting import scatter_matrix

attributes = ["median_house_value", "median_income", "total_rooms", "housing_median_age"]
scatter_matrix(housing[attributes], figsize=(12, 8))
pass # plt.show()


# In[14]:


housing.plot(kind="scatter", x="median_income", y="median_house_value", alpha=0.1)
pass # plt.show()


# In[15]:


housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"]/housing["total_rooms"]
housing["population_per_household"]=housing["population"]/housing["households"]


# In[16]:


corr_matrix = housing.corr(numeric_only=True)
corr_matrix["median_house_value"].sort_values(ascending=False)


# In[17]:


# Separate features and labels
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()


# In[18]:


# Get a list of the numerical column names
housing_num = housing.drop("ocean_proximity", axis=1)
num_attribs = list(housing_num)


# In[19]:


from sklearn.impute import SimpleImputer

# Create an imputer that will fill missing values with the median
imputer = SimpleImputer(strategy="median")

# The imputer can only be fitted to numerical data
imputer.fit(housing_num)

# The result is a plain NumPy array, so we'll wrap it back into a DataFrame
X = imputer.transform(housing_num)
housing_tr = pd.DataFrame(X, columns=housing_num.columns)


# In[20]:


from sklearn.preprocessing import OneHotEncoder

# Get the categorical column
housing_cat = housing[["ocean_proximity"]]

# Create and apply the one-hot encoder
cat_encoder = OneHotEncoder()
housing_cat_1hot = cat_encoder.fit_transform(housing_cat)

# The output is a sparse matrix. You can see it as a dense array with .toarray()
housing_cat_1hot.toarray()


# In[21]:


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

# Get list of numerical and categorical column names
num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]

# This is the pipeline for all numerical transformations
num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('std_scaler', StandardScaler()),
    ])

# This is the full pipeline that handles both numerical and categorical data
full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(), cat_attribs),
    ])

# Now, apply the entire pipeline to the housing data
housing_prepared = full_pipeline.fit_transform(housing)

print("✅ Preprocessing pipeline created and applied successfully!")
print("Shape of prepared data:", housing_prepared.shape)


# In[22]:


from sklearn.linear_model import LinearRegression

# Create and train the model
lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

# Let's test it on a few instances from the training set
some_data = housing[:5]
some_labels = housing_labels.iloc[:5]
some_data_prepared = full_pipeline.transform(some_data)

print("Predictions:", lin_reg.predict(some_data_prepared))
print("Actual Labels:", list(some_labels))


# In[23]:


from sklearn.metrics import mean_squared_error
import numpy as np

housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
print(f"Linear Regression RMSE: ${lin_rmse:,.2f}")


# In[24]:


from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)

# Now, let's measure its RMSE on the training set
housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)
print(f"Decision Tree RMSE: ${tree_rmse:,.2f}")


# In[25]:


from sklearn.model_selection import cross_val_score

# Evaluate the Decision Tree model using 10-fold cross-validation
scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                         scoring="neg_mean_squared_error", cv=10)
tree_rmse_scores = np.sqrt(-scores)

# Display the results
def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())

print("--- Decision Tree Cross-Validation Scores ---")
display_scores(tree_rmse_scores)


# In[26]:


from sklearn.ensemble import RandomForestRegressor

forest_reg = RandomForestRegressor()
forest_reg.fit(housing_prepared, housing_labels)

# Let's get its training set RMSE
housing_predictions = forest_reg.predict(housing_prepared)
forest_mse = mean_squared_error(housing_labels, housing_predictions)
forest_rmse = np.sqrt(forest_mse)
print(f"Random Forest Training RMSE: ${forest_rmse:,.2f}")

# And now its more reliable cross-validation RMSE
forest_scores = cross_val_score(forest_reg, housing_prepared, housing_labels,
                                scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-forest_scores)

print("\n--- Random Forest Cross-Validation Scores ---")
display_scores(forest_rmse_scores)


# In[27]:


from sklearn.model_selection import GridSearchCV

# Define the hyperparameter grid to search
param_grid = [
    # Try 3x4 = 12 combinations of hyperparameters
    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
    # Then try 2x3 = 6 combinations with bootstrap set to False
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]},
  ]

forest_reg = RandomForestRegressor(random_state=42)

# Set up the grid search with 5-fold cross-validation
grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                           scoring='neg_mean_squared_error',
                           return_train_score=True)

# Run the grid search
grid_search.fit(housing_prepared, housing_labels)

print("✅ Grid search complete!")


# In[28]:


# Display the best parameters found
grid_search.best_params_


# In[29]:


# Get the feature importances
feature_importances = grid_search.best_estimator_.feature_importances_

# Get the attribute names from our pipeline
cat_encoder = full_pipeline.named_transformers_["cat"]
cat_one_hot_attribs = list(cat_encoder.categories_[0])
attributes = num_attribs + cat_one_hot_attribs

# Display the features and their importance scores
sorted(zip(feature_importances, attributes), reverse=True)


# In[30]:


# Get the final model from the grid search
final_model = grid_search.best_estimator_

# Separate the test set features and labels
X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()


# In[31]:


# Apply the pipeline to transform the test data
X_test_prepared = full_pipeline.transform(X_test)

# Make predictions on the prepared test data
final_predictions = final_model.predict(X_test_prepared)

# Calculate the final RMSE
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)

print(f"Final RMSE on the test set: ${final_rmse:,.2f}")


# In[32]:


# Installed gradio

# In[34]:


import joblib

# Save the trained model to a file
joblib.dump(final_model, 'house_price_model.joblib')

# Save the data processing pipeline to a file
joblib.dump(full_pipeline, 'preprocessing_pipeline.joblib')

print("✅ Model and pipeline have been saved successfully to your project folder!")


# In[35]:


import gradio as gr
import pandas as pd
import joblib  # <-- CHANGE 1: Import joblib

# --- CHANGE 2: Load the saved model and pipeline ---
# This replaces the 30-minute training process
loaded_model = joblib.load('house_price_model.joblib')
loaded_pipeline = joblib.load('preprocessing_pipeline.joblib')


# --- Prediction Function ---
def predict_house_price(longitude, latitude, housing_median_age, total_rooms,
                        total_bedrooms, population, households, median_income,
                        ocean_proximity):
    """
    Predicts the house price based on the input features.
    """
    input_data = pd.DataFrame({
        'longitude': [longitude], 'latitude': [latitude],
        'housing_median_age': [housing_median_age], 'total_rooms': [total_rooms],
        'total_bedrooms': [total_bedrooms], 'population': [population],
        'households': [households], 'median_income': [median_income],
        'ocean_proximity': [ocean_proximity]
    })

    # --- CHANGE 3: Use the loaded pipeline and model ---
    prepared_data = loaded_pipeline.transform(input_data)
    prediction = loaded_model.predict(prepared_data)

    return f"${prediction[0]:,.2f}"

print('Script finished')


# In[ ]:




