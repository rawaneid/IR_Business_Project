# 💼 Business Information Retrieval System

A **Business Information Retrieval System** built using **Python**, **Apache Spark (PySpark)**, and **Streamlit**. The system processes business-related documents, builds an information retrieval index, and allows users to search for relevant documents through an interactive web interface.

It combines core Information Retrieval techniques, including Positional Indexing, TF-IDF weighting, Phrase and Boolean Queries, and Cosine Similarity, to retrieve and rank documents based on their relevance to user queries.

---

## 📌 Overview

The Business Information Retrieval System is designed to retrieve relevant information from a collection of business documents.

The system processes text documents, builds a Positional Index, calculates term statistics, generates normalized TF-IDF document vectors, and supports different query types.

An interactive **Streamlit GUI** allows users to upload their own document collections, build the index, perform searches, and explore the generated statistics and results.

---

## 🎯 Project Objectives

- Build a **Positional Index** using Apache Spark.
- Calculate Term Frequency (TF) and Weighted Term Frequency.
- Calculate Document Frequency (DF) and Inverse Document Frequency (IDF).
- Generate TF-IDF weights for terms across documents.
- Normalize document vectors.
- Support Phrase Queries using positional information.
- Support Boolean Queries using logical operators.
- Calculate Cosine Similarity between queries and documents.
- Rank retrieved documents according to their relevance.
- Provide an interactive interface for searching and exploring results.

---

## ✨ Key Features

### 1. Document Processing
- Process collections of business-related text documents.
- Upload individual TXT files or ZIP archives through the interface.
- Build the index and generate the required statistics.

### 2. Information Retrieval Techniques
- Positional Index construction.
- Term Frequency (TF).
- Weighted Term Frequency.
- Document Frequency (DF).
- Inverse Document Frequency (IDF).
- TF-IDF weighting.
- Document vector normalization.

### 3. Query Processing

**Phrase Queries**
- Search for exact phrases.
- Use positional information to identify documents containing the queried phrase.

**Boolean Queries**
- Search using logical operators.
- Support AND and AND NOT operations.

### 4. Document Ranking
- Calculate Cosine Similarity between the query and matching documents.
- Rank retrieved documents based on their similarity scores.

### 5. Interactive Dashboard
- View collection statistics and document counts.
- Explore the generated Positional Index.
- Inspect TF, Weighted TF, DF, and IDF.
- Explore TF-IDF values and document vector lengths.
- View normalized TF-IDF values.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Main programming language |
| Apache Spark 4.3.0 | Distributed data processing |
| PySpark 4.3.0 | Python API for Apache Spark |
| Java JDK 17 | Java runtime required by Spark |
| Streamlit | Interactive web application |
| Pandas | Data handling |
| Git & GitHub | Version control and collaboration |

---

## 📂 Project Structure

```text
IR_Business_Project/
│
├── dataset/
│   ├── d1.txt
│   ├── d2.txt
│   └── ...
│
├── outputs/
│   ├── generated/
│   ├── full_output.json
│   ├── positional_index.json
│   ├── term_statistics.json
│   └── tfidf.json
│
├── screenshots/
│
├── src/
│   ├── positional_index.py
│   ├── term_statistics.py
│   ├── tfidf.py
│   ├── query_processing.py
│   ├── similarity.py
│   ├── gui_backend.py
│   └── main.py
│
├── app.py
├── requirements.txt
├── packages.txt
├── .gitignore
└── README.md
```

### Main Modules

| File | Description |
|---|---|
| `positional_index.py` | Builds the Positional Index. |
| `term_statistics.py` | Calculates TF, Weighted TF, DF, and IDF. |
| `tfidf.py` | Generates TF-IDF weights and normalized document vectors. |
| `query_processing.py` | Processes Phrase and Boolean Queries. |
| `similarity.py` | Calculates Cosine Similarity and ranks documents. |
| `gui_backend.py` | Connects the retrieval modules with the Streamlit interface. |
| `main.py` | Runs the main indexing and processing pipeline. |
| `app.py` | Implements the Streamlit web application. |

---

## ⚙️ Installation & Setup

### 📋 Prerequisites

Make sure you have the following installed:

- Python 3.11
- Java JDK 17 or later
- Anaconda (recommended)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/rawaneid/IR_Business_Project.git
```

Navigate to the project directory:

```bash
cd IR_Business_Project
```

### 2. Create and Activate the Environment

```bash
conda create -n ir_project python=3.11 -y
conda activate ir_project
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Make sure Java is installed and available in your system PATH.

Check the Java installation:

```bash
java -version
```

---

## 🚀 Running the Application

After installing the dependencies and activating the environment, run:

```bash
streamlit run app.py
```

The application will open in your default browser.

You can also access it through the local URL displayed in the terminal.

---

## 🖥️ Using the System

The application provides three main sections:

### 1. IR Workspace
- Upload a collection of TXT documents or a ZIP archive.
- Build the Positional Index and calculate the required statistics.
- Select the query type.
- Enter a Phrase or Boolean Query.
- View matching documents and their similarity scores.
- Explore the ranked search results.

### 2. Dashboard
Explore the generated information retrieval statistics through interactive sections, including:

- Positional Index
- TF
- Weighted TF
- DF & IDF
- TF-IDF
- Document Vector Lengths
- Normalized TF-IDF

### 3. About
View information about the project, its purpose, and the development team.

---

## 📊 Sample Results

The system was tested using a sample collection of **10 business documents**.

The generated index contains **25 unique terms**.

Example queries:

**Phrase Query:**
```text
customer service
```

Matching documents:
- d1
- d2
- d5
- d10

The matching documents are ranked according to their Cosine Similarity scores.

**Boolean Query:**
```text
customer service AND sales growth
```

Matching document:
- d5

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

The deployment configuration includes:

- `requirements.txt` for Python dependencies.
- `packages.txt` for system-level dependencies, including Java.

**Live Application:** [Business Information Retrieval System](https://ir-business-project.streamlit.app/)

**GitHub Repository:** [IR_Business_Project](https://github.com/rawaneid/IR_Business_Project)

---

## 👥 Team Members

This project was developed collaboratively as part of the **Information Retrieval** course.

- Rawan Saad
- Habiba Kamal
- Olivia Nagy
- Zezef Ashraf
- Sara Hessin
- Febronia Fathy

---

## 📚 Project Topics

This project demonstrates practical applications of:

- Information Retrieval
- Text Processing
- Positional Indexing
- Term Weighting
- TF-IDF
- Phrase and Boolean Searching
- Cosine Similarity
- Document Ranking
- Distributed Processing with Apache Spark

---

**Project Status:** Completed

**Course:** Information Retrieval

**Developed using:** Python, PySpark, and Streamlit