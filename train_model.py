import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("biofouling_dataset.csv")

# Map to 3 classes (0,1,2)
data["fouling_severity"] = data["fouling_severity"].replace({3: 2})

# Features
X = data[[
    "sea_temperature",
    "salinity",
    "idle_days",
    "avg_speed",
    "days_since_cleaning",
    "hull_roughness",
    "friction_coeff",
    "fuel_penalty"
]]

# Target
y = data["fouling_severity"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(multi_class="multinomial", solver="lbfgs", class_weight="balanced", max_iter=2000))
])

# Hyperparameter grid
param_grid = {
    "logreg__C": [0.01, 0.1, 1, 10, 100],
    "logreg__max_iter": [1000, 2000, 3000]
}

# Grid Search
grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

grid.fit(X_train, y_train)

# Best model
best_model = grid.best_estimator_
print("Best Parameters:", grid.best_params_)

# Evaluate
y_pred = best_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save best model
joblib.dump(best_model, "biofouling_model.pkl")
print("Best model saved!")
