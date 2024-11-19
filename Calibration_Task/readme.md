### **Documentation for The Model Name Prediction API**

---

### **Introduction**
This Flask-based API server provides predictions using a pre-trained **XGBoost** classification model. The server accepts input features in JSON format, validates and preprocesses them, and returns sorted class probabilities for each instance.

---

### **Setup and Prerequisites**
#### **Environment Setup**
1. **Python Version**: Ensure you have Python 3.7+ installed.  
2. **Dependencies**: Install the required libraries using the following command:
   ```bash
   pip install flask numpy pandas xgboost scikit-learn
   ```

3. **Required Files**:
   - `model.pkl`: Pre-trained XGBoost model.
   - `features_order.pkl`: File containing the ordered list of feature names.
   - `class_names_order.pkl`: File containing the class names in the correct order.
   - `scaler.pkl`: Pre-trained scaler for feature normalization.

#### **Starting the Server**
To run the server:
```bash
python server.py
```

The server will be accessible locally at:
```
http://127.0.0.1:5000
```

---

### **API Endpoints**

#### **1. `POST /predict`**

##### **Description**
Accepts a JSON payload containing multiple instances with their respective feature values and returns the predicted probabilities for each class, sorted in descending order.

##### **Request Format**
- **Method**: `POST`  
- **URL**: `/predict`  
- **Content-Type**: `application/json`  
- **Body**:  
   The request body should be a dictionary where:
   - Keys are instance identifiers (e.g., `"0"`, `"1"`).
   - Values are dictionaries containing feature names and their respective values.

##### **Example Request**
```json
{
  "0": {
    "num_clients": 10,
    "Sum of Instances in Clients": 13821,
    "Max. Of Instances in Clients": 1383,
    "Min. Of Instances in Clients": 1382,
    "Stddev of Instances in Clients": 0.3,
    "Average Dataset Missing Values %": 4.99,
    "Min Dataset Missing Values %": 4.12,
    "Max Dataset Missing Values %": 5.57,
    "Stddev Dataset Missing Values %": 0.44,
    "Average Target Missing Values %": 4.99,
    "Min Target Missing Values %": 4.12,
    "Max Target Missing Values %": 5.57,
    "Stddev Target Missing Values %": 0.44,
    "No. Of Features": 3,
    "No. Of Numerical Features": 3,
    "No. Of Categorical Features": 0,
    "Sampling Rate": 0.1667,
    "Average Skewness of Numerical Features": 0.07,
    "Minimum Skewness of Numerical Features": 0.0000113,
    "Maximum Skewness of Numerical Features": 1.30,
    "Stddev Skewness of Numerical Features": 0.24,
    "Average Kurtosis of Numerical Features": 1.35,
    "Minimum Kurtosis of Numerical Features": 0.31,
    "Maximum Kurtosis of Numerical Features": 1.50,
    "Stddev Kurtosis of Numerical Features": 0.19,
    "Avg No. of Symbols per Categorical Features": 0,
    "Min. No. Of Symbols per Categorical Features": 0,
    "Max. No. Of Symbols per Categorical Features": 0,
    "Stddev No. Of Symbols per Categorical Features": 0,
    "Avg No. Of Stationary Features": 1,
    "Min No. Of Stationary Features": 0,
    "Max No. Of Stationary Features": 2,
    "Stddev No. Of Stationary Features": 0.44,
    "Avg No. Of Stationary Features after 1st order": 2.2,
    "Min No. Of Stationary Features after 1st order": 1,
    "Max No. Of Stationary Features after 1st order": 3,
    "Stddev No. Of Stationary Features after 1st order": 0.6,
    "Avg No. Of Significant Lags in Target": 2.9,
    "Min No. Of Significant Lags in Target": 2,
    "Max No. Of Significant Lags in Target": 3,
    "Stddev No. Of Significant Lags in Target": 0.3,
    "Entropy of Target Stationarity": 0.0098
  },
  "1": {
    "num_clients": 9,
    "Sum of Instances in Clients": 13821,
    "Max. Of Instances in Clients": 1383,
    "Min. Of Instances in Clients": 1382,
    "Stddev of Instances in Clients": 0.3,
    "Average Dataset Missing Values %": 4.99,
    "Min Dataset Missing Values %": 4.12,
    "Max Dataset Missing Values %": 5.57,
    "Stddev Dataset Missing Values %": 0.44,
    "Average Target Missing Values %": 4.99,
    "Min Target Missing Values %": 4.12,
    "Max Target Missing Values %": 5.57,
    "Stddev Target Missing Values %": 0.44,
    "No. Of Features": 3,
    "No. Of Numerical Features": 3,
    "No. Of Categorical Features": 0,
    "Sampling Rate": 0.1667,
    "Average Skewness of Numerical Features": 0.07,
    "Minimum Skewness of Numerical Features": 0.0000113,
    "Maximum Skewness of Numerical Features": 1.30,
    "Stddev Skewness of Numerical Features": 0.24,
    "Average Kurtosis of Numerical Features": 1.35,
    "Minimum Kurtosis of Numerical Features": 0.31,
    "Maximum Kurtosis of Numerical Features": 1.50,
    "Stddev Kurtosis of Numerical Features": 0.19,
    "Avg No. of Symbols per Categorical Features": 0,
    "Min. No. Of Symbols per Categorical Features": 0,
    "Max. No. Of Symbols per Categorical Features": 0,
    "Stddev No. Of Symbols per Categorical Features": 0,
    "Avg No. Of Stationary Features": 1,
    "Min No. Of Stationary Features": 0,
    "Max No. Of Stationary Features": 2,
    "Stddev No. Of Stationary Features": 0.44,
    "Avg No. Of Stationary Features after 1st order": 2.2,
    "Min No. Of Stationary Features after 1st order": 1,
    "Max No. Of Stationary Features after 1st order": 3,
    "Stddev No. Of Stationary Features after 1st order": 0.6,
    "Avg No. Of Significant Lags in Target": 2.9,
    "Min No. Of Significant Lags in Target": 2,
    "Max No. Of Significant Lags in Target": 3,
    "Stddev No. Of Significant Lags in Target": 0.3,
    "Entropy of Target Stationarity": 0.0098
  }
}
```

##### **Response Format**
- **Content-Type**: `application/json`  
- **Body**:  
   A dictionary where:
   - Keys are instance identifiers.
   - Values are dictionaries containing class names and their predicted probabilities, sorted in descending order.

##### **Example Response**
```json
{
    "0": {
        "HUBERREGRESSOR": 0.6630844473838806,
        "LinearSVR": 0.26084282994270325,
        "LASSO": 0.04548843204975128,
        "QUANTILEREGRESSOR": 0.006027398630976677,
        "XGBRegressor": 0.02271716296672821,
        "ELASTICNETCV": 0.001839689095504582
    },
    "1": {
        "XGBRegressor": 0.2971716296672821,
        "HUBERREGRESSOR": 0.1630844473838806,
        "LinearSVR": 0.26084282994270325,
        "LASSO": 0.04548843204975128,
        "QUANTILEREGRESSOR": 0.006027398630976677,
        "ELASTICNETCV": 0.001839689095504582
    }
}
```

##### **Error Responses**
1. **Invalid Input Format**:
   - **Status Code**: `400`  
   - **Body**:
     ```json
     {
         "error": "Invalid input format"
     }
     ```

2. **Missing Features**:
   - **Status Code**: `500`  
   - **Body**:
     ```json
     {
         "error": "Missing feature: [FEATURE_NAME]"
     }
     ```

3. **Unexpected Error**:
   - **Status Code**: `500`  
   - **Body**:
     ```json
     {
         "error": "[Error Message]"
     }
     ```

---

### **Server Logic**

1. **Feature Validation**:
   - The `validate_and_reorder_features` function ensures that all required features are present and orders them according to the model's expected input.
   - If any feature is missing, the server raises an error.

2. **Prediction**:
   - Features are scaled using the pre-loaded `scaler.pkl`.
   - Predictions are made using the `predict_proba` method of the XGBoost model.
   - The results are formatted into a dictionary and sorted by probability in descending order.

3. **Error Handling**:
   - Comprehensive error handling ensures the server responds appropriately to missing features or malformed input.
---