import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.compose import make_column_selector as selector

# Load data
data = pd.read_csv('sample_clean.csv')

# Preprocess the target variable (convert to numerical values)
# Remove non-numeric characters from 'price_USD' column and convert to float
data['price_USD'] = data['price_USD'].str.replace(r'\D', '').astype(float)
y = data['price_USD']

# Data preprocessing
# Handle missing values if any

# Split data into features (X) and target variable (y)
X = data.drop(['price_USD'], axis=1)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing steps
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, selector(dtype_include=object))
])

# Define the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Make predictions on new data
new_listing = pd.DataFrame([['url', 'header', 'location', 'query', 'name', '...', '...']], columns=X.columns)
predicted_price = model.predict(new_listing)
print(f'Predicted Price: {predicted_price}')
