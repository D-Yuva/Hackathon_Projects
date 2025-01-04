from flask import Flask
from flask_cors import CORS
from routes.predict import predict_efficiency
from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import pdfplumber

app = Flask(__name__)
CORS(app)

# Hugging Face model setup
generator = pipeline("text-generation", model="gpt2")

# Global variables to store the datasets
data1 = pd.DataFrame()
data2 = pd.DataFrame()
index = None
vectorizer = None
merged_data = pd.DataFrame()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Route to upload CSV files
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    global data1, data2, merged_data, index, vectorizer

    if 'data1' not in request.files or 'data2' not in request.files:
        return jsonify({"error": "Please upload both CSV files."}), 400

    data1 = pd.read_csv(request.files['data1'])
    data2 = pd.read_csv(request.files['data2'])

    # Convert DateTime columns
    data1['DateTime'] = pd.to_datetime(data1['DateTime'])
    data2['Time'] = pd.to_datetime(data2['Time'])

    # Merge the datasets
    merged_data = pd.merge_asof(data1.sort_values('DateTime'),
                                data2.sort_values('Time'),
                                left_on='DateTime',
                                right_on='Time',
                                direction='nearest')
    merged_data.drop(['Time', 'DateTime'], axis=1, inplace=True)

    # Prepare the data for FAISS indexing
    merged_data['input_text'] = merged_data.apply(lambda row:
        f"RT: {row['RT']}, kW_Tot: {row['kW_Tot']}, CH Load: {row['CH Load']}, "
        f"CH1: {row['CH1']}, CH2: {row['CH2']}, CH3: {row['CH3']}, "
        f"Hz_CHP: {row['Hz_CHP']}, kW_CHP: {row['kW_CHP']}, GPM: {row['GPM']}, "
        f"DeltaCHW: {row['DeltaCHW']}, CDHI: {row['CDHI']}, WBT: {row['WBT']}",
        axis=1)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(merged_data['input_text']).toarray().astype(np.float32)

    # Build the FAISS index
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    return jsonify({"message": "CSV files uploaded and processed successfully."})

# Function to search the FAISS index and return relevant data
def retrieve(query, k=10):
    query_vec = vectorizer.transform([query]).toarray().astype(np.float32)
    _, I = index.search(query_vec, k)
    return merged_data.iloc[I[0]]

# Route to handle user query and return AI-generated insights
@app.route('/query', methods=['POST'])
def handle_query():
    if not index:
        return jsonify({"error": "Data not available. Please upload the CSV files first."}), 400

    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query is required."}), 400

    # Retrieve data using FAISS based on the query
    retrieved_data = retrieve(query)

    # Generate text from the retrieved data
    generated_answer = " ".join(retrieved_data['input_text'].tolist())

    # Call Hugging Face for recommendations
    row_to_evaluate = retrieved_data.iloc[0]
    prompt = f"""
    Based on the following parameters of the chiller system:
    - RT: {row_to_evaluate['RT']}
    - kW_Tot: {row_to_evaluate['kW_Tot']}
    - CH Load: {row_to_evaluate['CH Load']}
    - kW_CHP: {row_to_evaluate['kW_CHP']}
    - GPM: {row_to_evaluate['GPM']}
    - WBT: {row_to_evaluate['WBT']}
    What changes should be made to improve efficiency?
    """

    try:
        response = generator(prompt, max_length=200, num_return_sequences=1, temperature=0.9)
        ai_recommendation = response[0]['generated_text'].strip()
    except Exception as e:
        ai_recommendation = f"Error generating recommendation: {str(e)}"

    # Return the generated answer and recommendations
    return jsonify({
        "generated_answer": generated_answer,
        "recommendation": ai_recommendation
    })

# Route to predict efficiency
app.add_url_rule('/api/predict', 'predict_efficiency', predict_efficiency, methods=['POST'])

if __name__ == "__main__":
    app.run(debug=True)
