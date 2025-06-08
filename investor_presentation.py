import os
import requests
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Google Gemini API Setup
API_KEY = ""  # 🔹 Replace with your actual Google Gemini API key
genai.configure(api_key=API_KEY)

# ✅ Initialize WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

# ✅ Scrape latest Investor Presentation PDF from Screener
def get_pdf_link(company_symbol):
    driver = init_driver()
    url = f"https://www.screener.in/company/{company_symbol}/consolidated/"
    driver.get(url)
    print(f"🟢 Loaded Screener page for {company_symbol}")

    wait = WebDriverWait(driver, 15)

    try:
        first_row = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'documents concalls')]//ul[@class='list-links']/li[1]")))
        print("✅ Located the first row of the Concall table.")

        try:
            ppt_element = first_row.find_element(By.XPATH, ".//a[contains(text(), 'PPT')]")
            pdf_link = ppt_element.get_attribute("href")
            print(f"✅ Found latest Investor Presentation PDF: {pdf_link}")
            driver.quit()
            return pdf_link

        except:
            print("❌ No recent Investor Presentation found.")
            driver.quit()
            return None

    except Exception as e:
        print("❌ No Concall data available.")
        driver.quit()
        return None

# ✅ Download the PDF
def download_pdf(pdf_url, company_symbol):
    if not pdf_url:
        print("⚠️ No PDF link available.")
        return None

    folder = "pdfs"
    os.makedirs(folder, exist_ok=True)
    pdf_path = os.path.join(folder, f"{company_symbol}.pdf")

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

# ✅ Generate Business Insights using Google Gemini API
def analyze_pdf_text(text):
    print("🔍 Analyzing Investor Presentation with Google Gemini...")

    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
    You are a financial analyst. Summarize the key insights from this investor presentation:

    {text}

    Provide:
    1. Overall business performance summary
    2. Key management commentary and future guidance
    3. Notable financial trends, risks, and opportunities
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

# ✅ Main Function: Scrape, Download & Analyze
if __name__ == "__main__":
    company_symbol = input("🔍 Enter company symbol (e.g., TCS, RELIANCE): ").strip().upper()
    
    pdf_url = get_pdf_link(company_symbol)

    if pdf_url:
        pdf_path = download_pdf(pdf_url, company_symbol)

        if pdf_path:
            pdf_text = extract_text_from_pdf(pdf_path)

            if pdf_text:
                insights = analyze_pdf_text(pdf_text)
                
                if insights:
                    print("\n📊 **Business Insights:**\n")
                    print(insights)
                else:
                    print("⚠️ Failed to generate insights.")
            else:
                print("❌ No text extracted from PDF.")
        else:
            print("⚠️ Failed to download PDF.")
    else:
        print("⚠️ No recent investor presentation available.")
