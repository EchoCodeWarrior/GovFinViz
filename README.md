# GovFinViz



[](https://www.python.org/downloads/)
[](https://streamlit.io)
[](https://plotly.com/)
[](https://opensource.org/licenses/MIT)

GovFinViz is a cutting-edge, interactive web application designed for the in-depth analysis and visualization of government budget data. This dashboard transforms complex financial statements into intuitive charts and actionable insights, making fiscal data accessible to everyone from policy analysts to the general public.

The standout feature is an **AI-powered Budget Assistant**, which allows users to ask questions about the budget in plain English and receive instant, data-driven answers.

### 🚀 [**View the Live Demo**](https://gov-fin-viz.streamlit.app/)

-----

## ✨ Key Features

  * **📋 Yearly Overview:** Get a comprehensive snapshot of any budget year from 2016 to 2025, with key performance indicators (KPIs) for total expenditure, revenue, fiscal deficit, and expenditure-to-GDP ratio.
  * **🏛️ Ministry Deep-Dive:** Analyze detailed budget allocations for individual ministries, view historical funding trends, and explore major schemes.
  * **💰 Revenue vs. Expenditure:** A clear, balance-sheet-style view with interactive waterfall and breakdown charts to understand government income and spending.
  * **📈 AI-Powered Insights:** An automated analysis tab that reveals long-term trends in revenue sources, expenditure patterns, and overall fiscal health.
  * **⚖️ Multi-Year Comparison:** A powerful tool to compare key budget metrics, ministry allocations, and revenue sources across multiple years.
  * **🤖 AI Budget Assistant:** Engage with a Gemini-powered chatbot to ask complex questions in natural language and get instant, context-aware answers based on the underlying budget data.

## 🛠️ Technology Stack

  * **Frontend:** [Streamlit](https://streamlit.io/)
  * **Backend:** [Python](https://www.python.org/)
  * **Data Analysis:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
  * **Data Visualization:** [Plotly](https://plotly.com/)
  * **AI & LLM:** [Google Gemini](https://ai.google.dev/) (gemini-2.5-flash)

## 🗂️ Project Structure

The repository is organized to separate concerns, making the codebase clean and maintainable.

```
govfinviz/
│
├── .gitignore          # Specifies files to be ignored by Git
├── README.md           # This file
├── requirements.txt    # Lists Python dependencies for deployment
├── app.py              # Main Streamlit application file (UI and layout)
├── chatbot.py          # Handles all AI logic and interaction with the Gemini API
├── data_processor.py   # Responsible for loading, cleaning, and processing all data
├── styles.py           # Contains custom CSS and styling functions
├── visualizations.py   # Generates all Plotly charts and graphs
│
└── data/               # Directory for all raw CSV data files
    ├── budget_summary.csv
    ├── expenditures_detailed.csv
    ├── ... (and other data files)
```

## ⚙️ Setup and Local Installation

To run this dashboard on your local machine, follow these steps:

**1. Clone the Repository:**

```bash
git clone https://github.com/your-username/govfinviz.git
cd govfinviz
```

**2. Create and Activate a Virtual Environment:**

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Install Dependencies:**
The required libraries are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables:**
The application requires a Google Gemini API key to power the chatbot.

  * Create a file named `.env` in the root of the project directory.
  * Add your API key to this file:

<!-- end list -->

```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

The application is coded to automatically load this key for local development.

**5. Run the Streamlit App:**

```bash
streamlit run app.py
```

The application should now be running in your web browser\!

