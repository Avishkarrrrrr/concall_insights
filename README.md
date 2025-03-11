
# Investor Presentation & Conference Call Insights Generator

## 🚀 Overview
This project automates the process of fetching, downloading, and analyzing investor presentations and conference call transcripts of publicly traded companies. Using **web scraping, PDF processing, and AI-powered analysis**, it provides **valuable insights** into a company's financial performance, strategy, and risks.

## 🎯 Key Features
- **🔍 Automated Scraping:** Retrieves the latest investor presentations & conference call transcripts from Screener.in.
- **📥 PDF Downloading:** Downloads and saves the documents for offline access.
- **📑 Text Extraction:** Extracts meaningful content from PDFs using `PyMuPDF`.
- **🤖 AI-Powered Analysis:** Uses **Google Gemini AI** to summarize key insights from the reports.
- **📊 Business Intelligence:** Provides insights into financial trends, company outlook, risks, and opportunities.

---

## 🛠️ Technologies Used
- **Python** - Main programming language
- **Selenium** - Web scraping automation
- **Requests** - Handling HTTP requests
- **PyMuPDF (fitz)** - PDF text extraction
- **Google Gemini AI** - AI-powered analysis

---

## 📌 Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/https://github.com/Avidarling19/concall_insight.git
cd investor-presentation-scraper
```

### 2️⃣ Install Dependencies
Ensure you have Python 3 installed, then run:
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Google Gemini API Key
Replace `API_KEY` in both `concall.py` and `investor_presentation.py` with your **Google Gemini API Key**.

---

## 📄 How It Works
### **1️⃣ Scraping Investor Presentations** (`investor_presentation.py`)
- Fetches the latest **Investor Presentation PDF** from Screener.in.
- Downloads and extracts text from the PDF.
- Analyzes key insights using **Google Gemini AI**.

Run it:
```sh
python investor_presentation.py
```

### **2️⃣ Scraping Conference Call Transcripts** (`concall.py`)
- Fetches the latest **Conference Call Transcript** from Screener.in.
- Downloads and extracts text from the PDF.
- Generates a summary using **Google Gemini AI**.

Run it:
```sh
python concall.py
```

---

## 💡 Why is This Project Useful?
✅ **Saves Time** – No need to manually search, download, and analyze PDFs.  
✅ **AI-Powered Insights** – Quickly get key takeaways without reading lengthy reports.  
✅ **Investor-Friendly** – Helps traders, investors, and analysts make informed decisions.  
✅ **Scalable & Customizable** – Can be extended to fetch reports from multiple sources.

---

## 🔧 Future Enhancements
- ✅ **Web Dashboard** for user-friendly analysis
- ✅ **Sentiment Analysis** of investor reports
- ✅ **Multi-source Support** (BSE, NSE, SEBI, etc.)

---

## 🤝 Contributing
We welcome contributions! Feel free to fork this repository and submit a pull request.

---

## 📜 License
This project is licensed under the **MIT License**.

---

### ⭐ Star this Repo if You Found It Useful! 🚀
```
