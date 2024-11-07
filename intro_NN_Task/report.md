## Time Series Forecasting Report: Jena Climate Dataset

### 1. Introduction
The objective of this project was to perform time series forecasting on the **Jena Climate dataset** using deep learning models. The dataset contains various atmospheric parameters recorded over time, with the temperature (`T (degC)`) selected as the target variable for prediction. This task employed a recurrent neural network (RNN) model, specifically an LSTM, due to its ability to capture temporal dependencies in time series data.

### 2. Data Preparation and Preprocessing

#### 2.1 Data Loading
The dataset was loaded and cleaned, with the `Date Time` column set as the index. Missing values were checked, and none were found.

#### 2.2 Feature Scaling
To aid model training and ensure numerical stability, a **MinMaxScaler** was applied to scale the feature values between 0 and 1. The target temperature values were retained in their original form for interpretability after predictions.

#### 2.3 Dataset Splitting
The dataset was split into:
- **Training set (70%)**
- **Validation set (15%)**
- **Test set (15%)**

Each set retained the chronological order, essential for time series forecasting tasks.

#### 2.4 Sequence Creation
Sliding windows were used to create sequences with a specified `sequence length` of 5 time steps. Each sequence had the last time step as its target, ensuring that the model could predict the next temperature value based on recent history.

### 3. Model Architecture

A recurrent neural network model with an **LSTM** layer was chosen for this task. The architecture included:
- **LSTM Layer**: Captures temporal dependencies with hidden states across time steps.
- **Fully Connected (FC) Layer**: Maps the output of the LSTM layer to the desired output dimension (temperature value).
  
The final model architecture parameters included:
- **Input Size**: Number of features in the dataset (excluding the target).
- **Hidden Size**: 32 (determined by hyperparameter tuning).
- **Number of Layers**: 2 (determined by hyperparameter tuning).
- **Output Size**: 1 (predicting one temperature value).

### 4. Hyperparameter Tuning

Optuna was used for hyperparameter optimization, testing combinations of the following parameters:
- **Learning Rate**: [0.001, 0.01]
- **Batch Size**: [16, 32, 64]
- **Number of Layers**: [2, 4, 6]
- **Hidden Size**: [32, 64]

After 5 trials, the best-performing hyperparameters were:
- **Learning Rate**: `0.0031`
- **Batch Size**: `64`
- **Number of Layers**: `2`
- **Hidden Size**: `32`

These optimal hyperparameters improved the model’s performance, yielding a validation loss (MSE) of **0.0495**.

### 5. Training Process

The model was trained on the training set with the best hyperparameters found during tuning:
- **Loss Function**: Mean Squared Error (MSE), suitable for regression tasks.
- **Optimizer**: Adam optimizer, selected for its adaptive learning rate capability with a learning rate of `0.0031`.
- **Batch Size**: 64

The training process ran for 10 epochs, with training and validation losses monitored after each epoch. The `shuffle` parameter was set to `False` for all DataLoaders to preserve the time series order, ensuring that each mini-batch contained sequential data points.

### 6. Model Evaluation

After training with the best hyperparameters, the model was evaluated on the test set using MSE and RMSE as metrics:
- **Final Test Loss (MSE)**: 0.0459
- **Final Test Loss (RMSE)**: 0.2143

This implies that the model's average error is approximately ±0.2°C, demonstrating good predictive accuracy.

### 7. Results Visualization

To visually assess the model's performance, the **actual vs. predicted temperature values** on the test set were plotted. As shown in the plot, the model's predictions closely follow the actual data trend. The overlap between the actual and predicted values indicates that the model captures the general temperature pattern accurately.

### 8. Conclusion

The LSTM model demonstrated effective time series forecasting on the Jena Climate dataset. Key conclusions include:
- **Accurate Forecasting**: The model achieved a low RMSE, indicating high accuracy in temperature prediction.
- **Model Generalization**: Despite the complexities of climate data, the model generalized well, as shown by the close alignment of actual and predicted values on the test set.
- **Hyperparameter Optimization**: Optuna proved useful for fine-tuning model parameters, significantly enhancing performance without manual trial and error.
