# 📊 FinSum — Advanced Financial Document Summarizer

> 🚀 _Automatically extract, analyze, and summarize financial insights from annual reports, corporate filings, and result PDFs._

---

## 🧠 Overview

**FinSum** (Financial Summary Analyzer) is an **AI-driven Streamlit web application** that automates financial document analysis.  
Upload a company’s **annual report**, **quarterly results**, or **corporate announcement PDF**, and get a structured report with extracted:

- 💰 **Key Financial Metrics** — Revenue, PAT, PBT, EBITDA, EPS
- 🏛️ **Corporate Announcements** — Dividends, M&A, Appointments, Legal Cases
- ⚙️ **Regulatory & Environmental Updates**
- 🚀 **Business Operations Insights** — Orders, Projects, Expansions
- 📈 **Executive Summary** — Auto-generated and ready for reports

---

## 🧩 Features

✅ **Automated PDF Parsing** using `pdfplumber`  
✅ **Smart Pattern Recognition** with optimized RegEx filters  
✅ **Dynamic Streamlit UI** for interactive results  
✅ **Comprehensive Report Generation** (`.txt` download)  
✅ **Instant Visual Metrics Dashboard**

---

## 🏗️ Project Architecture

```
FinSum/
│
├── app.py                  # Main Streamlit Application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── sample_reports/         # (Optional) Example PDFs for testing
```

---

## 📂 Supported Documents

You can upload:

- 📘 Annual Reports (PDF)
- 📄 Quarterly Results
- 🏛️ Corporate Announcements
- 💼 Financial Filings

The app automatically identifies and extracts key data from text and tables.

---

## 🧠 How It Works

1. **PDF Parsing** → Uses `pdfplumber` to extract text and tables.
2. **Pattern Recognition** → Applies regex-based AI rules to identify:
   - Financial figures
   - Announcements and corporate actions
   - Legal, regulatory, and environmental details
3. **Semantic Cleanup** → Cleans and filters extracted data.
4. **Report Generation** → Outputs an organized, human-readable analysis.

---

## 🖥️ User Interface Preview

The app features:

- 🟦 **Modern Streamlit UI** with custom CSS
- 📤 File Upload Box
- 📈 Metric Cards for quick insights
- 🏛️ Categorized Announcements
- 📋 Expandable Detailed Report View
- 📥 Download button for full report

---

## 🔍 Tech Stack

| Component        | Description                       |
| ---------------- | --------------------------------- |
| **Python 3.8+**  | Core language                     |
| **Streamlit**    | Web interface framework           |
| **pdfplumber**   | PDF text and table extraction     |
| **re (Regex)**   | Text pattern matching             |
| **datetime, os** | File management and time tracking |

---

> 💬 _“Turning complex financial PDFs into actionable insights — instantly.”_
