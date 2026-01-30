🛒 Flipkart Smart Vision System

An AI-powered computer vision system that automates product recognition, freshness detection, expiry tracking, and inventory counting using multimodal AI and real-time cloud storage.
Built as a finalist project for Flipkart Grid 6.0.

🚀 Overview

The Flipkart Smart Vision System is designed to assist smart retail environments and warehouses by:
Identifying products automatically
Detecting expiry dates
Measuring fruit/vegetable freshness
Counting multiple products in an image
Logging everything into a live cloud database

This reduces human error, improves operational efficiency, and enables real-time inventory intelligence.

🧠 Core Features
✅ Product Feature Extraction
Detects brand and product name directly from an image.

Example:
(Oreo Biscuits)

🥬 Freshness Detection

Evaluates fruit/vegetable freshness using AI.
Output format:

(name, freshness score / 10, days left, spoiled yes/no)

Example:

(apple, 8, 3, No)

📅 Expiry Detection

Extracts expiry date and calculates days left automatically.

Example:

Brand: Maggi
Expiry: 10/05/2026
Expired: No
Days Left: 120

📦 Smart Product Counting

Counts multiple products in a single image.

Example:

(Oreo: 1)
(Maggi: 2)
Total: 3

🏗️ Tech Stack

Frontend: Streamlit
AI Model: Google Gemini 1.5 Pro (Multimodal)
Image Processing: PIL
Backend DB: Supabase (PostgreSQL)
Language: Python
Environment: dotenv

🗂️ Database Tables
productquantity
Field	Description
timestamp	detection time
brand	product name
count	quantity
expirydate	optional expiry
expired	yes/no
expected_lifespan_days	days left
freshnessdata
Field	Description
timestamp	detection time
name	produce name
freshness	score
days_left	estimated life
spoiled	yes/no

⚙️ Installation
1. Clone repo
git clone https://github.com/yourusername/flipkart-smart-vision.git
cd flipkart-smart-vision

2. Install dependencies
pip install -r requirements.txt

3. Add environment variables

Create .env:

GOOGLE_API_KEY5=your_api_key_here

4. Run app
streamlit run app.py

📸 How It Works
Upload image of product/produce
Select feature:
Extract product
Expiry date
Freshness
IR counting
Gemini AI analyzes image
Data stored in Supabase cloud DB
Results displayed in UI

🎯 Use Cases

Smart retail checkout systems
Warehouse automation
Grocery inventory tracking
Food waste reduction
Supply chain analytics
Smart refrigerators
E-commerce fulfillment centers

🔐 Security

API keys stored using environment variables
Supabase secure cloud backend
No local image persistence

🏁 Flipkart Grid 6.0
This project was developed as part of Flipkart Grid innovation challenge focusing on:
AI-powered smart retail and intelligent inventory management.
