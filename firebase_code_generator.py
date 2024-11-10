import streamlit as st
import pandas as pd

# Function to convert camelCase to snake_case
def camel_to_snake_case(name):
    return ''.join(['_' + char.lower() if char.isupper() else char for char in name]).lstrip('_')

def generate_kotlin_code(df):
    # Drop rows with null `Event Name in Firebase`
    df_dropped = df.dropna(subset=['Event Name in Firebase'])

    # Group the data by `Event Name in Firebase`, `Properties`, and `Property name in Firebase`
    grouped_data = df_dropped.groupby(['Event Name in Firebase', 'Properties', 'Property name in Firebase']).apply(lambda x: x.values.tolist()).tolist()

    # Create a dictionary where keys are event names and values are a list of properties
    events = {}
    for event in grouped_data:
        event_name = event[0][3]
        property_name = event[0][6]
        if event_name not in events:
            events[event_name] = []
        events[event_name].append(property_name)

    # Convert the dictionary to a list of strings
    event_strings = []
    for event_name, properties in events.items():
        event_string = f'data class {event_name.replace("_", "").upper()}Event('
        for property_name in properties:
            if property_name is not None and 'Super Property' not in property_name:
                event_string += f'val {camel_to_snake_case(property_name.replace(" ", "_"))}: String, '
        event_string = event_string[:-2] + ')'  # Remove trailing comma and space
        event_strings.append(event_string)

    # Generate the complete Kotlin code
    kotlin_code = "\n".join(event_strings)
    return kotlin_code

# Streamlit app
st.title("Kotlin Code Generator for Firebase Events")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    kotlin_code = generate_kotlin_code(df)

    st.header("Generated Kotlin Code:")
    st.code(kotlin_code, language="kotlin")
