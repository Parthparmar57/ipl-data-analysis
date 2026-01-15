# 🏏 IPL Data Analysis Report Generator

A Python-based data analysis project that processes **IPL (Indian Premier League) ball-by-ball delivery data** to generate a **professional, multi-page PDF report** with rich visual insights. The project uses **Pandas** for data manipulation and **Matplotlib** for high-quality visualizations.

---

## 📌 Project Overview

The script analyzes historical IPL delivery-level data and automatically generates a **7-page PDF report** (`report.pdf`) summarizing key batting statistics, trends, and record performances. The output is suitable for presentations, academic projects, or portfolio demonstrations.

---

## 📊 Key Features

The script `create_ipl_report.py` generates the following report sections:

1. **Executive Summary**

   * Title page with high-level IPL statistics
   * Total matches
   * Total runs scored
   * Number of unique batsmen

2. **Top Run Scorers**

   * Horizontal bar chart of the **Top 10 highest run-scorers** in IPL history

3. **Power Hitters Analysis**

   * Batsmen with the most **sixes (6s)**
   * Batsmen with the most **fours (4s)**

4. **Run Distribution**

   * Pie chart showing frequency of different run values (0s, 1s, 2s, 4s, 6s, etc.)
   * Histogram showing overall run distribution

5. **Death Over Specialists & Strike Rate Analysis**

   * Top boundary hitters in **death overs (16–20)**
   * Strike rate comparison of top batsmen (minimum 500 runs)

6. **Player Spotlight – Virat Kohli**

   * Detailed breakdown of Virat Kohli’s performance against different teams

7. **Record Performances**

   * Styled table of the **Top 5 highest individual scores** in a single IPL match

---

## 🛠️ Tech Stack & Requirements

* **Python**: 3.x
* **Libraries Used**:

  * `pandas`
  * `numpy`
  * `matplotlib`

---

## 📥 Installation

1. Clone the repository or download the project files.
2. Install the required Python libraries:

```bash
pip install pandas numpy matplotlib
```

3. **Dataset Setup**:

   * Ensure the dataset file `deliveries.csv` is available.
   * Place it in:

     * The project root directory **OR**
     * A `content/` subdirectory

---

## 🚀 How to Run

Execute the main script using the command below:

```bash
python create_ipl_report.py
```

### What happens after execution?

* The dataset is loaded and processed
* All charts and tables are generated
* A **7-page PDF report** (`report.pdf`) is saved in the project directory
* A brief summary is printed in the terminal

---

## 📂 Project Structure

```text
.
├── create_ipl_report.py   # Main data analysis & report generation script
├── deliveries.csv         # IPL delivery-level dataset (required)
├── report.pdf             # Auto-generated PDF report
└── README.md              # Project documentation
```

---

## 🎨 Visualization & Styling

The report uses a clean and professional visual style:

* **Matplotlib Style**: `seaborn-v0_8-darkgrid`
* **Custom Color Palettes** for better readability
* **Gradient Backgrounds** on the title page
* **Annotated Charts** with:

  * Value labels
  * Ranking badges (🥇 🥈 🥉)
* **Formatted Tables** for record performances

---

## 🎯 Use Cases

* Data Analysis & Visualization practice
* Sports analytics projects
* Academic mini-projects
* Portfolio showcase for Python / Data Science roles

---

## 📜 License

This project is intended for **educational and learning purposes**. Dataset ownership and usage rights depend on the original data source.

---


