import streamlit as st
import pandas as pd

# Create a function `generate_kotlin_class` that takes the class name and properties as input and generate the corresponding Kotlin class
def generate_kotlin_class(class_name, properties):
    # Remove 'Super Property\n' from the property names and convert the property names to snake_case
    properties = [prop.replace('Super Property\n', '').lower() for prop in properties]

    # Generate the Kotlin class definition
    class_definition = f"data class {class_name} (\n"
    for prop in properties:
        class_definition += f"    val {prop}: String,\n"
    class_definition = class_definition[:-2] + "\n)"  # Removing the trailing comma and adding a newline
    return class_definition

# Create a Streamlit app
st.title("CSV to Kotlin Classes Converter")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Drop rows where `Event Name in Firebase` or `Property name in Firebase` is null
    df.dropna(subset=['Event Name in Firebase', 'Property name in Firebase'], inplace=True)

    # Drop duplicated rows based on `Event Name in Firebase` and `Property name in Firebase`
    df.drop_duplicates(subset=['Event Name in Firebase', 'Property name in Firebase'], inplace=True)

    # Create a new column `class_name` by concatenating the string 'Event' with the values in `Event Name in Firebase` column
    df['class_name'] = 'Event' + df['Event Name in Firebase']

    # Group the data by `class_name` and aggregate the values of `Property name in Firebase` into a list
    grouped_data = df.groupby('class_name')['Property name in Firebase'].apply(list).reset_index()

    # Create a dictionary with the `class_name` as the key and a list of corresponding `Property name in Firebase` as the value
    class_properties = dict(zip(grouped_data['class_name'], grouped_data['Property name in Firebase']))

    # Generate Kotlin classes
    kotlin_classes = ""
    for class_name, properties in class_properties.items():
        kotlin_class = generate_kotlin_class(class_name, properties)
        kotlin_classes += kotlin_class + "\n\n"

    # Display Kotlin classes in a scrollable text box
    st.text_area("Generated Kotlin Classes", value=kotlin_classes, height=500)

    # Download Kotlin classes as a text file
    st.download_button(
        label="Download Kotlin Classes",
        data=kotlin_classes,
        file_name="kotlin_classes.txt",
        mime="text/plain",
    )
