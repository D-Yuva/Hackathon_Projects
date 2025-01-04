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
from sklearn.preprocessing import LabelEncoder

data='/content/Lung_Cancer_Dataset.csv'
df = pd.read_csv(data)

df = df.drop_duplicates()

label_encoder = LabelEncoder()
df['category_label_encoded'] = label_encoder.fit_transform(df['LUNG_CANCER'])
df['GENDER'] = label_encoder.fit_transform(df['GENDER'])

df = df.drop(columns=['LUNG_CANCER'])

last_column = df.columns[-1]  # Get the name of the last column
df = pd.concat([df[last_column], df.drop(columns=last_column)], axis=1)
df = df.rename(columns={'category_label_encoded': 'target'})

y = df['target']
X = df.drop('target', axis=1)
y = to_categorical(y, num_classes=2)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=21)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(15,)),  # Input layer with 4 features
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

st.title("Welcome to Lung Cancer Predictor")

def get_user_input():
    user_input = []

    value = st.radio(label="Gender",options=['Male','Female'])
    if value == "Male":
      user_input.append(1)
    else:
      user_input.append(2)
    value1 = st.number_input("Enter Age: ")
    user_input.append(value1)
    value2 = st.radio(label="Smoking",options=['Yes','No'])
    if value2 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value3 = st.radio(label="Yellow Fingers",options=['Yes','No'])
    if value3 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value83 = st.radio(label="Anxiety",options=['Yes','No'])
    if value83 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value4 = st.radio(label="Peer Pressure",options=['Yes','No'])
    if value4 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value5 = st.radio(label="Chronic Disease",options=['Yes','No'])
    if value5 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value6 = st.radio(label="Fatigue",options=['Yes','No'])
    if value6 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value7 = st.radio(label="Allergy",options=['Yes','No'])
    if value7 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value8 = st.radio(label="Wheezing",options=['Yes','No'])
    if value8 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value89 = st.radio(label="Alcohol Consumption",options=['Yes','No'])
    if value89 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value9 = st.radio(label="Coughing",options=['Yes','No'])
    if value9 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value10 = st.radio(label="Shortness of Breath",options=['Yes','No'])
    if value10 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value11 = st.radio(label="Swallowing Difficulty",options=['Yes','No'])
    if value11 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    value12 = st.radio(label="Chest Pain",options=['Yes','No'])
    if value12 == "Yes":
      user_input.append(1)
    else:
      user_input.append(2)
    return user_input

user_data = get_user_input()

user_df = pd.DataFrame([user_data], columns=['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ', 'ALLERGY ', 'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY', 'CHEST PAIN'])

user_data_scaled = scaler.transform(user_df)

predictions = model.predict(user_data_scaled)

predicted_labels = np.argmax(predictions, axis=1)

accuracy_0 = predictions[0][0] * 100
accuracy_1 = predictions[0][1] * 100

if accuracy_0 > accuracy_1 :
  st.write(f"There is a  {accuracy_0:.2f}% chance you suffer from lung cancer")
else:
  st.write(f"There is a  {accuracy_1:.2f}% chance you don't suffer from lung cancer")