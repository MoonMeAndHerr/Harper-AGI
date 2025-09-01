# 🤖 Harper AI – An All-Rounder Assistant

Harper AI is a **modular, all-rounder personal assistant** designed to adapt to multiple roles — from market analysis to promotional strategy and meeting preparation.  
Built with flexibility in mind, Harper can run **online (powered by GPT)** or **offline (with deterministic mock responses)**.

---

## ✨ Features

- 📊 **Market Advisor** – Analyzes data trends and provides growth insights.  
- 🎯 **Promotional Advisor** – Suggests campaigns and strategies for outreach.  
- 📅 **Meeting Advisor** – Prepares structured agendas and action points.
- 
---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/harper-ai.git
cd harper-ai
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Max: source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_api_key_here   # optional if using GPT
streamlit run app.py
```

### 2. Project Structure, How It Works, Tech Stack, License & Contributing

```
harper-ai/
│── services/          # Specialized advisor modules (Market, Promo, Meeting, etc.)
│── utils/             # AI engine and helper functions
│── app.py            # Entry point for Harper AI
│── requirements.txt   # Dependencies
│── README.md          # Project documentation
|── assets             # Logo and images
|── sample_data         # Deterministic mockup
|── models         # Saved CNN Models
```

Harper AI uses a **central AI engine** that:
1. Connects to OpenAI GPT if a key is available.  
2. Falls back to **deterministic mock responses** if offline.  
3. Routes requests through different **advisors** depending on the task.  

**Tech Stack**  
- 🐍 Python 3.9+  
- ⚙️ OpenAI GPT API (optional)  
- 📦 Modular architecture for easy expansion  

**License**  
This project is licensed under the **MIT License**. Feel free to fork, modify, and contribute!  

**Contributing**  
- 🐛 Found a bug? Open an issue  
- 💡 Got an idea? Submit a pull request  
- 🔧 Want to improve Harper? Fork and hack away  

**Acknowledgements**  
Special thanks to inspiration from **OpenAI, DeepSeek, and modular AI design principles**. Harper AI is built with the vision of being a **versatile companion for productivity, insights, and strategy**.  
