# 💼 Azure Intelligent Search Application

**Author:** Pranaykumar  
**Project Type:** TCS iON — Building Intelligent Application with Azure AI Search  
**Status:** ✅ Coding Completed | ✅ Documentation Completed  

---

## 🌐 Project Overview

This project implements an **Azure Intelligent Search Application** for an internal **self-service portal**, allowing employees to search company policies, HR documents, and other internal content using **natural language queries**.

It leverages **Azure Cognitive Search** and **Azure Blob Storage**, integrating:
- An automated **data preprocessing pipeline (Python + NLP)**
- **Intelligent indexing** with Azure AI Search
- A responsive **Flask web interface** for dynamic querying

---

##  System Architecture

**Flow Diagram:**
```bash
Raw Documents (.docx / .pdf)
↓
Preprocessing (Python + NLP)
↓
Cleaned Dataset (combined_data.json)
↓
Clustered dataset (combined_cluster.json)
↓
Azure Blob Storage (Container: policydata)
↓
Azure Cognitive Search
├── Data Source
├── Indexer
├── Index with Scoring Profile
↓
Flask Search Interface
```
---

## ⚙️ Technologies Used

| Category | Tools / Services |
|-----------|------------------|
| **Cloud Services** | Azure Cognitive Search, Azure Blob Storage |
| **Programming** | Python 3.8+ |
| **Libraries** | Flask, pandas, numpy, python-docx, PyPDF2, azure-search-documents, azure-storage-blob, python-dotenv |
| **Development Tools** | Visual Studio Code, PowerShell, Azure CLI |

---

## 📁 Folder Structure

```bash
Azure-Intelligent-Search-Final/
│
├── code/
│ ├── app/
│ │ ├── static/ (JS, CSS)
│ │ ├── templates/ (HTML)
│ │ ├── azure/ (create_index, run_indexer, upload_blob, search_query)
│ │ ├── preprocessing/ (clean_data, extract_text, merge_policies, preprocess_policies,cluster_policies)
│ │ └── config/ (.env, config.json)
│ │
│ ├── data/
│ │ ├── raw/ (unprocessed docs)
│ │ └── processed/ 
│ │        └── combined_data.json
| |        └── combined_clustered.json
│ ├── app.py
│ └── README.md
│
├── docs/
│ ├── Project_Report.pptx
│ ├── Project_Report.pdf
│ ├── Test_Cases.docx
│ ├── Test_Design.docx
│ ├── Test_Scenarios.docx
│ └── Visualization_Report.pdf
│
└── Video Project 6.mp4

```
---

## 🧩 Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/Pranaykumar-adepu/Azure-Intelligent-Search-Final.git
cd Azure-Intelligent-Search-Final
 ```
Step 2: Install Dependencies
bash
```bash
pip install -r requirements.txt
```
Step 3: Create .env File in /config/
```bash
AZURE_STORAGE_CONNECTION_STRING=
AZURE_CONTAINER_NAME=policydata
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_ADMIN_KEY=
AZURE_SEARCH_INDEX_NAME=company-policies-index
AZURE_SEARCH_SERVICE_NAME=
```
## 🏃‍♂️ How to Run
Preprocess Data

```bash
python preprocessing/preprocess_policies.py
Cleans raw .docx/.pdf files and generates combined_data.json.
Clusting data from combined_data.json to produce combined_cluster.json
```
Upload Data to Blob Storage

```bash
python azure/upload_blob.py
```
Create Azure Search Index
```bash
python azure/create_index.py
```
Run the Indexer

```bash
python azure/run_indexer.py
```
Query the Search Engine
```bash
python azure/search_query.py
Or use the Azure Portal Search Explorer for manual queries.
```
💡 You can also test queries visually in Azure Portal → Search Explorer.


## 🔍 Testing Scenarios

|Test |ID	Description	Expected Result|
|------|----------------------------------------------|
|TC01	|Search for “encryption”	Returns Encryption Policy|
|TC02	|Search for “incident response”	Returns ISMS or Incident Policy|
|TC03	|Check title boosting	Prioritizes exact title matches|
|TC04	|Run indexer manually	Indexer shows “Success” in Azure Portal|
|TC05	|Upload invalid file	Graceful error handling in UI|


## 📦 Repository & Resources
🔗 **GitHub Repository**:(https://github.com/Pranaykumar-adepu/Azure-Intelligent-Search.git)

🎥 **Demo Video**: https://drive.google.com/file/d/17-t4cp2n_XHN9rNLxnb1eWO1mx6M5ZHj/view?usp=drive_link

📄 **Documentation**: Available in /docs/ folder


## 🧭 Future Enhancements
**Integrate Azure OpenAI for conversational and semantic queries**

**Add multilingual support (English, Hindi, Telugu)**

**Build Admin Dashboard for analytics and usage metrics**


## 🙏 Acknowledgment
**Special thanks to TCS iON for providing the opportunity to build this industry project and explore Azure AI’s intelligent search capabilities.**
