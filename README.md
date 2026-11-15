# 💼 Business Information Retrieval System

A Business Information Retrieval System built with **Python** and **Apache Spark (PySpark)**. The project focuses on indexing, searching, and ranking business-related documents using core Information Retrieval techniques.

## 📌 Overview

This project implements an Information Retrieval system that processes a collection of business documents and retrieves relevant information based on user queries.

It demonstrates how text indexing, term weighting, query processing, and similarity measures can be combined to provide effective document retrieval and ranking.

## 🎯 Objectives

- Build a Positional Index using Apache Spark.
- Calculate Term Frequency (TF), Document Frequency (DF), and Inverse Document Frequency (IDF).
- Generate and normalize TF-IDF document vectors.
- Support Phrase Queries using positional information.
- Process Boolean Queries using AND and AND NOT operators.
- Calculate Cosine Similarity and rank retrieved documents by relevance.

## 🛠️ Technologies Used

- 🐍 **Python 3.11**
- ⚡ **Apache Spark 4.3.0**
- 🔥 **PySpark 4.3.0**
- ☕ **Java JDK 17**
- 🐙 **Git & GitHub**

## ✨ Key Features

- Distributed text processing using PySpark.
- Positional Index construction.
- TF-IDF weighting and document vector normalization.
- Phrase and Boolean query processing.
- Cosine Similarity-based document ranking.

## 📂 Project Structure

```text
IR_Business_Project/
│
├── dataset/
│   ├── d1.txt
│   ├── d2.txt
│   ├── ...
│   └── d10.txt
│
├── src/
│   ├── positional_index.py
│   ├── term_statistics.py
│   ├── tfidf.py
│   ├── query_processing.py
│   ├── similarity.py
│   └── main.py
│
├── outputs/
├── screenshots/
└── README.md
```

## ⚙️ Installation & Setup

### 📋 Prerequisites

Make sure the following tools are installed:

- Python 3.11
- Java JDK 17
- Anaconda
- Apache Spark / PySpark 4.3.0

### 1️⃣ Create and Activate the Environment

```bash
conda create -n ir_project python=3.11 -y
conda activate ir_project
```

### 2️⃣ Install PySpark

```bash
python -m pip install pyspark==4.3.0
```

## 🚀 Usage

*Implementation in progress.*

Instructions for running the complete system will be added once all modules are integrated.

## 📊 Sample Results

*Results and output examples will be added after implementation and testing.*

## 🖼️ Screenshots

Screenshots demonstrating the system's functionality will be added here.

## 👥 Team Members

This project is developed collaboratively as part of the **Information Retrieval** course.

*Team member names and contributions will be added here.*

---

📌 **Project Status:** In Progress
