import os
import requests
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Google Gemini API Setup
API_KEY = ""  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# ✅ Initialize WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

# ✅ Scrape latest conference call transcript PDF from Screener
def get_concall_pdf_link(company_symbol):
    driver = init_driver()
    url = f"https://www.screener.in/company/{company_symbol}/consolidated/"
    driver.get(url)
    print(f"🟢 Loaded Screener page for {company_symbol}")

    wait = WebDriverWait(driver, 15)

    try:
        # Locate the Concalls section and extract the first available transcript link
        transcript_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'documents concalls')]//ul[@class='list-links']/li[1]/a[contains(text(), 'Transcript')]")))
        pdf_link = transcript_element.get_attribute("href")

        print(f"✅ Found latest Conference Call Transcript PDF: {pdf_link}")
        driver.quit()
        return pdf_link

    except Exception as e:
        print("❌ No recent conference call transcript found.")
        driver.quit()
        return None

# ✅ Download the PDF
def download_pdf(pdf_url, company_symbol, doc_type="concall"):
    if not pdf_url:
        print("⚠️ No PDF link available.")
        return None

    folder = "pdfs"
    os.makedirs(folder, exist_ok=True)
    pdf_path = os.path.join(folder, f"{company_symbol}_{doc_type}.pdf")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.bseindia.com/"
    }

    try:
        response = requests.get(pdf_url, headers=headers, stream=True)
        response.raise_for_status()

        with open(pdf_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"✅ PDF Downloaded Successfully: {pdf_path}")
        return pdf_path

    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading PDF: {e}")
        return None

# ✅ Extract text from the downloaded PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

# ✅ Generate Conference Call Analysis using Google Gemini API
def analyze_concall_text(text):
    print("🔍 Analyzing Conference Call Transcript with Google Gemini...")

    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
    You are a financial analyst. Summarize the key insights from this conference call transcript.

    **Analysis should include:**
    - 🔹 **Recent business developments** 
    - 🔹 **Future projections & company outlook**
    - 🔹 **Key highlights from the management**
    - 🔹 **Any financial trends, risks, or opportunities mentioned**

    **Transcript:**  
    {text}
    """

    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

        print("⚠️ No insights generated.")
        return None

    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

# ✅ Main Function: Scrape, Download & Analyze Conference Call
if __name__ == "__main__":
    company_symbol = input("🔍 Enter company symbol (e.g., TCS, RELIANCE): ").strip().upper()
    
    pdf_url = get_concall_pdf_link(company_symbol)

    if pdf_url:
        pdf_path = download_pdf(pdf_url, company_symbol, doc_type="concall")

        if pdf_path:
            pdf_text = extract_text_from_pdf(pdf_path)

            if pdf_text:
                insights = analyze_concall_text(pdf_text)
                
                if insights:
                    print("\n📊 **Conference Call Insights:**\n")
                    print(insights)
                else:
                    print("⚠️ Failed to generate insights.")
            else:
                print("❌ No text extracted from PDF.")
        else:
            print("⚠️ Failed to download PDF.")
    else:
        print("⚠️ No recent conference call transcript available.")
