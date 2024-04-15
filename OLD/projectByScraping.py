import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures

# Load the CSV file into a DataFrame
data = pd.read_csv('test.csv')

# Preprocessing
# Remove non-numeric characters from 'price_USD' column
data['price_USD'] = data['price_USD'].str.extract('(\d+)').astype(float)
data['cnt_bedrooms'] = pd.to_numeric(data['cnt_bedrooms'], errors='coerce')  # Convert to numeric
data['cnt_baths'] = pd.to_numeric(data['cnt_baths'], errors='coerce')  # Convert to numeric
# Handle any other preprocessing steps here...

# Drop rows with missing values
data.dropna(inplace=True)

# Creating interaction term
data['bed_bath_ratio'] = data['cnt_bedrooms'] * data['cnt_baths']

# Splitting the data into features and target variable
X = data[['cnt_guests', 'cnt_bedrooms', 'cnt_beds', 'cnt_baths', 'bed_bath_ratio']]
y = data['price_USD']

# Introducing polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Initialize the Random Forest Regressor model
model = RandomForestRegressor(random_state=42)

# Fit the model on the entire data
model.fit(X_poly, y)

# Hard-coded pre-informed data
pre_informed_data = pd.DataFrame({
    'cnt_guests': [7, 2],
    'cnt_bedrooms': [3, 1],
    'cnt_beds': [5, 1],
    'cnt_baths': [2, 1],
    'bed_bath_ratio': [3, 0]
})

# Transform the pre-informed data to include polynomial features
pre_informed_data_poly = poly.transform(pre_informed_data)

# Predict prices for the pre-informed data
y_pre_informed_pred = model.predict(pre_informed_data_poly)

# Round the predicted prices to the nearest whole number
y_pre_informed_pred_rounded = np.round(y_pre_informed_pred)

# Print the predicted prices
print("Predicted prices for the pre-informed data:")
print(y_pre_informed_pred_rounded)
