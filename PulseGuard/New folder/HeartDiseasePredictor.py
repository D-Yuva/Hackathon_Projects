import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping

data='/content/heart.csv'
df = pd.read_csv(data)

df = df.drop_duplicates()

y = df['target']
X = df.drop('target', axis=1)
y = to_categorical(y, num_classes=2)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(13,)),  # Input layer with 4 features
    tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')  # Output layer with 2 classes
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',  # Use categorical_crossentropy for one-hot encoded labels
              metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_accuracy', patience=40, mode='max', verbose=1)

model.fit(X_train, y_train, epochs=100, batch_size=8, validation_split=0.1, callbacks=[early_stopping])

test_loss, test_acc = model.evaluate(X_test, y_test)

st.title("Welcome to Heart Disease Predictor")

def get_user_input():
    column_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    user_input = []
    for column_name in column_names:
        value = st.number_input(f"Enter data for {column_name}: ", key = column_name)
        user_input.append(value)
    return user_input

user_data = get_user_input()

user_df = pd.DataFrame([user_data], columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

user_data_scaled = scaler.transform(user_df)

predictions = model.predict(user_data_scaled)

predicted_labels = np.argmax(predictions, axis=1)

accuracy_0 = predictions[0][0] * 100
accuracy_1 = predictions[0][1] * 100

if accuracy_1 > accuracy_0 :
  st.write(f"There is a  {accuracy_0:.2f}% chance u suffer from a heart disease")
else:
  st.write(f"There is a  {accuracy_1:.2f}% chance u DON'T suffer a from heart disease")