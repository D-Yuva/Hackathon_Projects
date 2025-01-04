import streamlit as st
import pandas as pd
import re

# Load data
df = pd.read_csv('/content/Disease precaution.csv', index_col='Disease', encoding='utf-8')

# User input using Streamlit text_input
user_sentence = st.text_input("Enter the query: ")
user_sentence = user_sentence.title()  # Convert to title case

# Check if the user has provided input
if user_sentence:
    if user_sentence in df.index:
        row = df.loc[user_sentence]

        # Display information using Streamlit text
        st.text("Disease Name:")
        st.text(user_sentence)
        st.text("\nPrecautions:")
        st.text(f"  1: {row['Precaution_1']}")
        st.text(f"  2: {row['Precaution_2']}")
        st.text(f"  3: {row['Precaution_3'] if not pd.isna(row['Precaution_3']) else 'N/A'}")
        st.text(f"  4: {row['Precaution_4'] if not pd.isna(row['Precaution_4']) else 'N/A'}")
    else:
        matched_diseases = []

        for disease in df.index:
            pattern = re.compile(re.escape(user_sentence), re.IGNORECASE)
            if re.search(pattern, disease):
                matched_diseases.append(disease)

        matched_diseases = list(set(matched_diseases))

        if matched_diseases:
            match_found = False

            for matched_disease in matched_diseases:
                row = df.loc[matched_disease]

                # Display information using Streamlit text
                st.text("Disease Name: ")
                st.text(matched_disease)
                st.text("\nPrecautions:")
                st.text(f"  1: {row['Precaution_1']}")
                st.text(f"  2: {row['Precaution_2']}")
                st.text(f"  3: {row['Precaution_3'] if not pd.isna(row['Precaution_3']) else 'N/A'}")
                st.text(f"  4: {row['Precaution_4'] if not pd.isna(row['Precaution_4']) else 'N/A'}")
                st.text()
                match_found = True

            if not match_found:
                st.text("Data not present")
        else:
            st.text("Data not present")
else:
    st.text("Please enter a query.")
