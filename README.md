# 🌊 AquaBot — Groundwater Intelligence Chatbot

AquaBot is a Flask-based intelligent chatbot designed to analyze and visualize groundwater data across districts and blocks of Uttar Pradesh.  

It provides:
- Structured groundwater reports
- Extraction statistics
- Recharge analytics
- Future availability projections
- Dynamic graph generation

Deployed on Render (Live Cloud Service).

---

## 🚀 Live Demo

🔗 https://aquabot-ivga.onrender.com  

*(Free tier may take ~30 seconds to wake up after inactivity.)*

---

## 📊 Features

### 1️⃣ District-Level Reports
- Total Annual Ground Water Recharge
- Natural Discharges
- Annual Extractable Resource
- Net Availability for Future Use
- Stage of Ground Water Extraction (%)

### 2️⃣ Block-Level Condition Queries
Example:
### 3️⃣ Dynamic Graph Generation
- Recharge trend over years
- Future availability trend
- Auto-saved plots using Matplotlib
- Timestamp-based file generation

Example:
### 4️⃣ Smart Query Routing
- Keyword detection
- Regex-based district matching
- Context-aware response formatting

---

## 🏗️ Tech Stack

### Backend
- Python 3
- Flask
- Gunicorn (Production server)

### Data Processing
- Pandas
- Regex-based parsing

### Visualization
- Matplotlib (Agg backend for server-safe rendering)

### Deployment
- Render (Free Instance)
- GitHub Version Control

---

## 📂 Project Structure
AquaBot/
│
├── app.py
├── chatbot.py
├── data_loader.py
├── requirements.txt
│
├── templates/
│ └── index.html
│
├── static/
│ └── plots/
│
├── up.csv
├── up2.csv
├── rechargefinal.csv
├── availablefinal.csv
---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Sahilmish23/AquaBot.git
cd AquaBot
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000
👨‍💻 Author

Sahil Mishra
B.Tech — VIT Chennai
Backend & AI Systems Enthusiast
