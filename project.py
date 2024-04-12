from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()

# Print the feature names and target names
print("Feature names:", iris.feature_names)
print("Target names:", iris.target_names)

# Print the first few samples
print("First few samples:")
for i in range(5):
    print("Sample", i+1, ":", iris.data[i], "-> Target:", iris.target[i])
