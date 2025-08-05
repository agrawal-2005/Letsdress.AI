# 👗 Letsdress.AI – AI-Powered Fashion Personalization Tool

Letsdress.AI is a fashion-enhancement AI tool designed to recommend clothing styles using the power of image generation and prompt-based personalization. Built for intuitive interaction and visual impact, it brings your fashion sense to life with a friendly user interface.

---

## 📌 Overview

**Letsdress.AI** aims to revolutionize online fashion shopping by offering:
- 🧠 **Smart Recommendations** tailored to user preferences  
- 🔁 **Real-Time Trend Adaptation** to stay in sync with evolving styles  
- 💻 **Modern UI/UX** with interactive, visually rich components  

---

## 📁 Project Structure

```
Letsdress.AI/
│
├── authtoken.py                    # Authentication token for APIs (if used)
├── requirements.txt                # Python dependencies
├── feedback form.png               # Screenshot assets
├── prompt-insertion.png
├── result1.png
├── result2.png
├── startup-page.png
│
├── database/
│   ├── image_data.py               # Script to handle database I/O
│   ├── Image_data.db               # SQLite database
│   └── .idea/                      # IDE-specific config
│
├── static/                         # Static assets for frontend
│   ├── css/
│   │   ├── style.css
│   │   └── style_open.css
│   ├── images/
│   │   └── (Backgrounds, avatars, and results)
│   └── js/
│       └── script.js
│
├── templates/                      # HTML templates (Jinja2 for Flask)
│   ├── feedback.html
│   ├── index.html
│   └── opening.html
│
├── .idea/                          # JetBrains IDE configs
└── __pycache__/                    # Compiled Python files
```

---

## 🧠 Features

- 👤 **User Personalization** based on browsing history and style inputs  
- 🛍️ **Outfit Recommender** using machine learning models  
- 📈 **Trend-Aware Ranking** to highlight in-demand items  
- 💅 **Aesthetic UI** with intuitive navigation and filters  
- 📊 **Category Prediction** and intelligent filtering  

---

## 🧰 Tech Stack

| Frontend        | Backend             | Machine Learning        | Database/Misc     |
|-----------------|---------------------|-----------------------  |-------------------|
| HTML / CSS / JS | Flask               |Stable Diffusion, Jinja2 |    SQLite3        |

---

## 🔄 How it Works

1. **User Input Logging**: Tracks selected styles and inputs for better personalization  
2. **ML Model Inference**: Flask server handles prompt-based image generation and filtering  
3. **Flask Routing**: Backend routes connect frontend UI to model logic and database  
4. **Frontend Rendering**: Personalized visuals shown using responsive web UI  

---


## 🛠️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/agrawal-2005/Letsdress.AI.git
cd Letsdress.AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python authtoken.py
```

Open your browser and navigate to `http://localhost:5000`

---

## 🧬 Machine Learning

- Utilizes prompt-based image generation models (e.g., Stable Diffusion)
- Focused on enhancing personalization using visual outputs and style-based text prompts 
- Flask API serves predictions in real-time to the Node backend  

---

## 📸 Sample Screenshots

| Startup Page | Result Image |
|--------------|--------------|
| ![Startup](/startup-page.png) | ![Result1](/result.png) ![Result2](/result-1.png)|

---

## 🙋‍♂️ Feedback

Feel free to raise an issue or suggest improvements.  
Contact: [Prashant Agrawal](https://github.com/agrawal-2005)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file (if available).