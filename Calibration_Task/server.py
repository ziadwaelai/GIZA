from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the pre-trained XGBoost model
xgb_model = pickle.load(open("model.pkl", "rb"))
features_order = pickle.load(open("features_order.pkl", "rb"))
class_names = pickle.load(open("class_names_order.pkl", "rb"))

def validate_and_reorder_features(input_features):
    ordered_features = []
    for feature_name in features_order:
        if feature_name in input_features:
            ordered_features.append(input_features[feature_name])
        else:
            raise ValueError(f"Missing feature: {feature_name}")
    return np.array(ordered_features)

def custom_predict(model, X):
    x = X.reshape(1, -1)
    y_pred = model.predict_proba(x)
    y_pred = pd.DataFrame(y_pred, columns=class_names).to_dict(orient="records")[0]
    # sort the predictions by probability
    y_pred = dict(sorted(y_pred.items(), key=lambda x: x[1], reverse=True))
    # print(y_pred)
    return y_pred

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({"error": "Invalid input format"}), 400
        predictions = {}

        for instance_id, features in input_data.items():
            ordered_features = validate_and_reorder_features(features)
            predictions[instance_id] = custom_predict(xgb_model, ordered_features)
            print(predictions)
        return jsonify(predictions) , 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)