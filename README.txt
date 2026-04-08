# 🚀 Pathfinder 
### The Multi-Profile Growth Engine & Self-Improvement Calendar

Pathfinder Pro is a high-performance productivity tool designed to manage the "Time Horizons" of self-improvement. It separates **Work** and **Life** into distinct profiles and uses **Smart Date Logic** to ensure your tasks align with specific milestones throughout the year.

---

## 🛠 Features

### 1. Dual-Profile Tracking
Switch between **Work** and **Life** modes. Data is siloed so your professional tasks never clutter your personal growth habits.

### 2. Smart Date Selection Logic
The app automatically assigns "Target Dates" based on the horizon you select:
* **Daily**: Set to today's date.
* **Weekly**: Automatically targets the **Wednesday** of the current week.
* **Monthly**: Targets the **First Tuesday** of the month.
* **Half-Yearly**: Targets the **First Thursday** of Jan/July.
* **Yearly**: Targets the **First Monday** of the year.

### 3. CSV Bulk Upload
Don't enter tasks one by one. Use a single CSV file to populate your entire yearly roadmap across all horizons.

### 4. Advanced Task Management
* **Remarks & Nuance**: Finish tasks with optional progress notes/remarks.
* **Daily Reporting**: One-click summary generation and email delivery.
* **Cross-Platform**: Accessible via Windows/Linux standalone builds or as a Mobile Web App via Streamlit.

---

## 📂 Project Structure

```text
├── app.py              # Main Streamlit application code
├── requirements.txt    # Python dependencies (streamlit, pandas)
├── data.json           # Your local task database (auto-generated)
├── growth_data.csv     # Template for bulk uploads
└── README.md           # Project documentation