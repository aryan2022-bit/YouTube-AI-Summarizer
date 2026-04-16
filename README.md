# 📺 YouTube AI Summarizer

Transform any YouTube video into a clean, concise, and detailed summary in seconds using the power of Google's Gemini AI.

## ✨ Features
* **⚡ Gemini AI Powered**: Utilizes Google's extreme-speed `gemini-2.5-flash-lite` model for generating highly accurate and detailed summaries.
* **🌑 Sleek Dark UI**: A completely custom, eye-friendly dark mode interface tailored over Streamlit.
* **🎯 Key Point Extraction**: Intelligently extracts the most important aspects of the transcript into easily readable sub-headings and bullet points.
* **🛡️ Secure & Optimized**: Gracefully handles YouTube IP restrictions, rate limits, and protects API keys via dotenv configuration.

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/aryan2022-bit/YouTube-AI-Summarizer.git
cd YouTube-AI-Summarizer
```

### 2. Install dependencies
Ensure you have Python installed. Run this terminal command:
```bash
pip install -r requirements.txt
```

### 3. Set up your API Key
Create a `.env` file in the root directory of the project and add your Google API key:
```env
GOOGLE_API_KEY="your_api_key_here"
```

### 4. Run the application
```bash
streamlit run app.py
```

## 🛠️ Built With
* Streamlit — Python Framework
* Google Generative AI (Gemini) — AI Backend
* YouTube Transcript API — Transcript scraper
