import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from flask import request, jsonify
import tempfile

# Load model
model = keras.models.load_model(r'models/Plant_efficiency.h5')

def preprocess_data(data):
    """
    Preprocess the input dataset for prediction, following your defined logic.
    """
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    
    def categorize_time(time):
        if pd.isnull(time):
            return None
        if time.hour < 6 or (time.hour == 6 and time.minute == 0):
            return 1
        elif (time.hour == 6 and time.minute > 0) or (time.hour < 12 or (time.hour == 12 and time.minute == 0)):
            return 2
        elif (time.hour == 12 and time.minute > 0) or (time.hour < 18 or (time.hour == 18 and time.minute == 0)):
            return 3
        else:
            return 4
    
    data['Time_Category'] = data['Time'].apply(categorize_time)
    data_pp = data.drop(columns=['Time'])
    data_pp['Plant_Efiiciency'] = data_pp.pop('kW_RT')
    data_pp = data_pp.drop(columns=['CH1', 'CH2', 'CH3', 'CH4', 'kW_CHS', 'Hz_CHS'])
    data_final = data_pp[data_pp['Plant_Efiiciency'] != 0]
    
    return data_final

def predict_efficiency():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        file.save(temp_file.name)
        temp_filepath = temp_file.name
    
    data = pd.read_csv(temp_filepath)
    os.remove(temp_filepath)

    preprocessed_data = preprocess_data(data)
    X = preprocessed_data.drop('Plant_Efiiciency', axis=1)
    predictions = model.predict(X)
    
    result = {
        "Time_Category": preprocessed_data["Time_Category"].tolist(),
        "Predicted_Efficiency": predictions.flatten().tolist()
    }

    return jsonify(result), 200


