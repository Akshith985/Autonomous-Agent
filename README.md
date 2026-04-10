# 🤖 Autonomous SRE Agent
### **The Self-Healing "Single Pane of Glass" Pipeline**

[![Groq](https://img.shields.io/badge/AI-Groq%20LPU-orange)](https://groq.com/)
[![LocalStack](https://img.shields.io/badge/Cloud-LocalStack-blue)](https://localstack.cloud/)
[![Grafana](https://img.shields.io/badge/Dashboard-Grafana-orange)](https://grafana.com/)

## 🌟 Overview
The **Autonomous SRE Agent** is a proactive DevSecOps tool that bridges the gap between local development and infrastructure observability. Unlike traditional tools that simply alert you when something is wrong, this agent **identifies, alerts, and remediates** security vulnerabilities and performance bottlenecks in real-time.

By combining **Groq’s sub-second AI inference** with **LocalStack’s simulated AWS environment**, we’ve created a "Self-Healing" loop that fixes code before it even reaches a Pull Request.

---

## 🚀 Key Features
* **Real-Time Watchdog:** Instantly detects file saves in your IDE via `PollingObserver`.
* **Sub-Second AI Audit:** Uses Groq's LPU (Llama-3.1-8B) to perform Root Cause Analysis (RCA) in milliseconds.
* **Autonomous Remediation:** Automatically generates a new Git branch with a security patch applied.
* **Unified Observability:** Streams `CRITICAL` and `WARNING` logs to a Grafana dashboard via LocalStack CloudWatch.
* **Security-First:** Specifically tuned to detect SQL Injections, Hardcoded Secrets, and Null Pointer Exceptions.

---

## 🏗️ System Architecture
1.  **Develop:** Developer saves a Java file (`App.java`) with a vulnerability.
2.  **Analyze:** The Python Watcher triggers a request to the **Groq LPU**.
3.  **Alert:** If a risk is found, a categorized log is pushed to **LocalStack** using `boto3`.
4.  **Visualize:** **Grafana** displays the real-time threat level on the "Single Pane of Glass."
5.  **Heal:** The agent executes `git checkout -b` and overwrites the file with a secure, AI-generated version.

---

## 🛠️ Tech Stack
* **Inference Engine:** [Groq Cloud](https://groq.com/) (LPU Technology)
* **Cloud Simulation:** [LocalStack](https://localstack.cloud/) (S3, CloudWatch, Logs)
* **Visualization:** [Grafana](https://grafana.com/)
* **Automation:** Python, Boto3, Watchdog
* **Version Control:** Git

---

## 🚦 Getting Started

### 1. Prerequisites
* Docker Desktop (for LocalStack/Grafana)
* Python 3.10+
* Groq API Key

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/Akshith985/Autonomous-Agent.git](https://github.com/Akshith985/Autonomous-Agent.git)
cd Autonomous-Agent

# Install dependencies
pip install -r requirements.txt
