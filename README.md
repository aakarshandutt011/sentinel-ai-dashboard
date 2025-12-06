# 🛡️ Sentinel AI - SOC Threat Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-ff4b4b)
![Status](https://img.shields.io/badge/Status-Prototype-green)

**Sentinel AI** is a Next-Gen Security Operations Center (SOC) dashboard designed to visualize server logs, detect anomalies, and track threat patterns in real-time. Built with a focus on "Glassmorphism" UI design and data storytelling, it helps analysts reduce alert fatigue by highlighting critical threats (Brute Force, SQL Injection) automatically.

---

## 📸 Interface Preview

*(Upload a screenshot of your dashboard here later and delete this text)*
![Dashboard Preview](https://via.placeholder.com/800x400?text=Upload+Your+Dashboard+Screenshot+Here)

---

## 🚀 Key Features

*   **Ingestion Pipeline:** Automatically ingests and parses raw server logs (CSV format).
*   **Attack Detection:**
    *   **Brute Force:** Identifies high-velocity 401 Unauthorized spikes.
    *   **SQL Injection:** Flags suspicious query parameters and 500 Error clusters.
*   **Interactive Visualization:**
    *   **Neon Time-Series:** Dynamic bar charts that change color (Cyan → Red) based on traffic volume/risk thresholds.
    *   **Endpoint Heatmap:** Identifies which parts of the API are under attack.
*   **Modern UI/UX:** Dark-mode "Glassmorphism" aesthetic designed for low-light SOC environments.

---

## 🛠️ Architecture & Tech Stack

This project follows a lightweight **ETL (Extract, Transform, Load)** architecture:

1.  **Data Layer (Pandas):** Generates synthetic attack data (Brute Force/SQLi scenarios) and structures it into a DataFrame.
2.  **Logic Layer (Python):** Filters traffic, calculates risk metrics, and aggregates time-series data.
3.  **Presentation Layer (Streamlit & Plotly):** Renders the data using WebGL-accelerated charts and custom CSS for the visual interface.

---

## 💻 Installation & Usage

**1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/sentinel-ai-dashboard.git
cd sentinel-ai-dashboard
