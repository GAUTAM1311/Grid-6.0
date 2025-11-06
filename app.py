# Importing necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import re
import sqlite3
from datetime import datetime
from supabase import create_client, Client
import io

# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY5"))

# Supabase configuration
SUPABASE_URL = 'https://bxeanvxilpcswieocvej.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4ZWFudnhpbHBjc3dpZW9jdmVqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU5MjYxODcsImV4cCI6MjA1MTUwMjE4N30.exoXaJLn1qiuMERvacjEtm_oMEOIWc0mJQR7z59gM3o'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Utility ---
def pil_to_bytes(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return buf.getvalue()


def call_gemini(prompt, image):
    """Send text + image to Gemini and return plain text output"""
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    img_bytes = pil_to_bytes(image)

    response = model.generate_content([
        prompt,
        {"mime_type": "image/png", "data": img_bytes}
    ])
    return response.text.strip() if response.text else ""


# --- DB Functions ---
def store_indb_feature(prompt, image):
    try:
        resp_text = call_gemini(prompt, image)
        print("Gemini Response:", resp_text)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "timestamp": current_time,
            "brand": resp_text,
            "count": 1
        }
        result = supabase.table("productquantity").insert(data).execute()
        print("Data stored successfully in Supabase!", result)
        return resp_text
    except Exception as e:
        return f"Error in feature extraction: {e}"


def store_indb_freshness(prompt, image):
    try:
        resp_text = call_gemini(prompt, image)
        print("Gemini Response:", resp_text)

        # Expected format: (name,freshness,days_left,spoiled)
        parts = resp_text.strip("()").split(",")
        if len(parts) < 4:
            raise ValueError("Unexpected response format")

        name, freshness, days_left, spoiled = [p.strip() for p in parts]

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "timestamp": current_time,
            "name": name,
            "freshness": freshness,
            "days_left": days_left,
            "spoiled": spoiled
        }
        result = supabase.table("freshnessdata").insert(data).execute()
        print("Data stored successfully in Supabase!", result)

        res = f"""- Produce: {name}
- Freshness: {freshness}
- Days left: {days_left}
- Spoiled: {spoiled}"""
        return res
    except Exception as e:
        return f"Error in freshness: {e}"


def store_indb_expiry(prompt, image):
    try:
        resp_text = call_gemini(prompt, image)
        print("Gemini Response:", resp_text)

        # Expected format: (name,dd/mm/yyyy,Yes/No)
        parts = resp_text.strip("()").split(",")
        if len(parts) < 3:
            raise ValueError("Unexpected response format")

        name = parts[0].strip()
        useby = parts[1].strip()
        expired1 = parts[2].strip()

        # Calculate days left safely
        daysleft = "NA"
        try:
            expiry_date = None
            try:
                expiry_date = datetime.strptime(useby, "%d/%m/%Y")
            except ValueError:
                expiry_date = datetime.strptime(useby, "%m/%Y").replace(day=1)

            if expiry_date:
                daysleft = (expiry_date - datetime.now()).days
        except Exception:
            pass

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "timestamp": current_time,
            "brand": name,
            "count": 1,
            "expirydate": useby,
            "expired": expired1,
            "expected_lifespan_days": daysleft
        }
        result = supabase.table("productquantity").insert(data).execute()
        print("Data stored successfully in Supabase!", result)

        res = f"""- Brand/Product: {name}
- Expiry Date: {useby}
- Expired: {expired1}
- Days Left: {daysleft} days
"""
        return res
    except Exception as e:
        return f"Error in expiry: {e}"


def store_product_quantity(prompt, image):
    try:
        resp_text = call_gemini(prompt, image)
        print("Gemini Response:", resp_text)

        # Expected format: ((oreo,1),(maggi,2))
        product_entries = re.findall(r'\((.*?)\s*,\s*(\d+)\)', resp_text)
        if not product_entries:
            raise ValueError("No valid product entries found")

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        res_lines = []
        total_count = 0
        for name, quantity in product_entries:
            name = name.strip()
            quantity = int(quantity.strip())
            total_count += quantity

            data = {
                "timestamp": current_time,
                "brand": name,
                "count": quantity
            }
            supabase.table("productquantity").insert(data).execute()
            res_lines.append(f"- {name} : {quantity}N")

        res_lines.append(f"- Total : {total_count}N")

        return "\n".join(res_lines)
    except Exception as e:
        return f"Error in counting: {e}"


# --- Streamlit UI ---
st.set_page_config(page_title="Flipkart Smart Vision System")
st.header("Flipkart Smart Vision System")

uploaded_file = st.file_uploader("Take/Upload Image", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)

prompts = {
    "Freshness_db": "you will be given image of Fruit/vegetable you have ot give output as (name,freshness out of 10,days left before spoiled,spoiled-yes/no)",
    "ircount_db": "you will be give an image containing different products/fruits/vegetables give output as ((oreo,1),(maggi,1),(lays classic,1))",
    "expiry_db": "i will give you an image of product you have to give me its expirydate output as (brand,dd/mm/yyyy,Yes/No)",
    "feature_db": "i will give you an image of the product give me the brand name and product name output as (oreo biscuits)"
}

response = None
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Extract Features") and image:
        response = store_indb_feature(prompts["feature_db"], image)

with col2:
    if st.button("Expiry Date") and image:
        response = store_indb_expiry(prompts["expiry_db"], image)

with col3:
    if st.button("IR Counting") and image:
        response = store_product_quantity(prompts["ircount_db"], image)

with col4:
    if st.button("Freshness Level") and image:
        response = store_indb_freshness(prompts["Freshness_db"], image)

if response:
    st.subheader("Response")
    st.write(response)
