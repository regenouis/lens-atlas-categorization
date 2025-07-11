import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Lens Atlas Categorization",
    layout="wide"
)

st.title("Lens Atlas Categorization POC")
st.write(
    "Upload a CSV of lens records. This app will auto-categorize mounts, focal lengths, and aperture classes."
)

# File uploader
uploaded_file = st.file_uploader("Upload your lens CSV", type=["csv"])

# Categorization functions
def get_focal_length_band(focal_length):
    if focal_length <= 14:
        return "Ultra-Wide"
    elif 15 <= focal_length <= 35:
        return "Wide"
    elif 36 <= focal_length <= 70:
        return "Standard"
    elif 71 <= focal_length <= 135:
        return "Short Telephoto"
    else:
        return "Telephoto"

def get_aperture_class(aperture):
    if aperture <= 1.2:
        return "Super Fast"
    elif 1.4 <= aperture <= 2.0:
        return "Fast"
    elif 2.1 <= aperture <= 4.0:
        return "Moderate"
    else:
        return "Variable/Slow"

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Expecting columns: Model
    df["Brand"] = df["Model"].apply(lambda x: "Cooke")
    
    # Extract Mount
    df["Mount"] = df["Model"].apply(
        lambda x: re.findall(r"\((.*?)\)", x)[-1] if "(" in x else "Unknown"
    )
    
    # Extract Focal Length
    df["Focal Length"] = df["Model"].apply(
        lambda x: int(re.findall(r"(\d+)mm", x)[0]) if re.findall(r"(\d+)mm", x) else None
    )
    
    # Extract Aperture T-stop
    df["Aperture (T)"] = df["Model"].apply(
        lambda x: float(re.findall(r"T([\d.]+)", x)[0]) if re.findall(r"T([\d.]+)", x) else None
    )
    
    # Categorize Focal Length Band
    df["Focal Length Band"] = df["Focal Length"].apply(
        lambda x: get_focal_length_band(x) if pd.notnull(x) else "Unknown"
    )
    
    # Categorize Aperture Class
    df["Aperture Class"] = df["Aperture (T)"].apply(
        lambda x: get_aperture_class(x) if pd.notnull(x) else "Unknown"
    )
    
    # Assign Specialty
    df["Specialty"] = "Cine Prime"

    st.subheader("Categorized Data")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Categorized CSV",
        data=csv,
        file_name="categorized_lenses.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file to get started.")
