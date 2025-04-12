import streamlit as st

st.markdown(
    """
    <style>
    .body {
        background-color: grey;
        color: white;
    }
    .stApp {
        background: grey;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 36px;
    }
    .stButton>button{
        background-color: blue;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 5px;
        transition: 0.3s ease;
    }
    .stButton>button:hover{
        transform: scale(1.05);
        background: linear-gradient(45deg, #92fe9d, #0094cc);
        color: black;
    }
    .result-box {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        background: grey;
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 5px 15px rgba(0, 201, 255, 0.3);
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1> Unit Converter </h1>", unsafe_allow_html=True)
st.write("Easily convert between different units of measurement with our intuitive converter.")


conversion_type = st.sidebar.selectbox("Select Conversion Type", ["Length", "Weight", "Temperature"])
value = st.number_input("Enter the value:", value=0.0, min_value=0.0, step=0.1)
col1, col2 = st.columns(2)

if conversion_type == "Length":
    with col1:
        from_unit = st.selectbox("From Unit", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Feet", "Yards", "Inches"])
    with col2:
        to_unit = st.selectbox("To Unit", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Feet", "Yards", "Inches"])

elif conversion_type == "Weight":
    with col1:
        from_unit = st.selectbox("From Unit", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
    with col2:
        to_unit = st.selectbox("To Unit", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From Unit", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To Unit", ["Celsius", "Fahrenheit", "Kelvin"])


# converted function
def length_conversion(value, from_unit, to_unit):
    length_units = {
     'Meters': 1,
     'Kilometers': 0.001,
     'Centimeters': 100,
     'Millimeters': 1000,
     'Miles': 0.000621371,
     'Yards': 1.09361,
     'Feet': 3.28084,
     'Inches': 39.3701
  }

    return value / length_units[from_unit] * length_units[to_unit]

def weight_conversion(value, from_unit, to_unit):
    weight_units = {
    'Kilograms': 1,
    'Grams': 1000,
    'Milligrams': 1000000,
    'Pounds': 2.20462262185,
    'Ounces': 35.27396194958
}

    return value / weight_units[from_unit] * weight_units[to_unit]

def temperature_conversion(value, from_unit, to_unit):
    if from_unit == "Celsius":
        return (value * 9/5 + 32) if to_unit == "Fahrenheit" else value + 273.15 if to_unit == "Kelvin" else value
    elif from_unit == "Fahrenheit":
        return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15 if to_unit == "Kelvin" else value
    elif from_unit == "Kelvin":
        return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32 if to_unit == "Fahrenheit" else value
    return value

if st.button("Convert"):
    if conversion_type == "Length":
        result = length_conversion(value, from_unit, to_unit)
    elif conversion_type == "Weight":
        result = weight_conversion(value, from_unit, to_unit)
    elif conversion_type == "Temperature":
        result = temperature_conversion(value, from_unit, to_unit)

    st.markdown(f'<div class="result-box">{value} {from_unit} = {result:.4f} {to_unit}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Created by Shafique Ur Rehman</div>', unsafe_allow_html=True)