             # 🚦 SmartFlow — AI-Powered Traffic Prediction & Signal Control

> *Because red lights shouldn't make you late. Science should.*

---

```
  🚗 💨  ──────────────────────────────────────────────────────► 🏁
         [ Sensors ] → [ AI Brain ] → [ FastAPI ] → [ Green Light ]
```

---

## 🧠 What Is This?

**SmartFlow** is an intelligent traffic management system that doesn't just react to congestion — it *predicts* it. Using a trained Random Forest model, the system forecasts traffic bottlenecks **5 minutes into the future** and dynamically adjusts traffic signal timings before gridlock even begins.

No more staring at red lights while the intersection ahead is empty.

---

## ✨ Features

| Feature | Status |
|---|---|
| 🔮 Predict congestion 5 min ahead | ✅ Live |
| ⚡ FastAPI prediction endpoint | ✅ Live |
| 🌐 Node.js / browser integration | ✅ Live |
| 🚦 Smart traffic light syncing | ✅ Live |
| 🗺️ Multi-intersection support | 🔜 Coming Soon |
| 📊 Real-time dashboard | 🔜 Coming Soon |
| 🎛️ Adaptive signal auto-adjust | 🔜 Coming Soon |

---

## 🗺️ How It Works

```
   📷 Traffic Sensors / Cameras
              │
              ▼
   📡 Real-Time Traffic Data
              │
              ▼
   🔧 Preprocessing & Feature Engineering
              │
              ▼
   🤖 Random Forest Classifier (Future Prediction)
              │
              ▼
   🚀 FastAPI  →  POST /predict
              │
              ▼
   🖥️  Node.js / Frontend Dashboard
              │
              ▼
   🚦 Smart Traffic Light Controller
              │
              ▼
   ✅ Optimized Signal Timings → Less Wait, Better Flow
```

---

## 📁 Project Structure

```
PythonProject4/
├── 🗂️  backend/
│    ├── models/
│    │    └── traffic_model_future.pkl   ← Trained ML brain
│    └── ml_api/
│         ├── api.py                     ← FastAPI server
│         └── __init__.py
├── 🎓  ai_training/
│    └── train_traffic_model_future.py   ← Model training script
└── 🌐  node_predict.js                  ← Node.js API client
```

---

## 🚀 Getting Started

### Step 1 — Set Up Python Environment

```bash
# Create & activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn scikit-learn pandas joblib
```

### Step 2 — Train the Model

```bash
python ai_training/train_traffic_model_future.py
```

This produces `backend/models/traffic_model_future.pkl` — your AI traffic oracle. 🔮

### Step 3 — Launch the API

```bash
cd backend
uvicorn ml_api.api:app --reload --host 0.0.0.0 --port 8000
```

Visit the interactive Swagger docs at:
👉 **http://127.0.0.1:8000/docs**

### Step 4 — Run Node.js Integration

```javascript
// node_predict.js
const fetch = require("node-fetch");

async function getFuturePrediction() {
  const response = await fetch("http://127.0.0.1:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      feature1: 12,
      feature2: 5,
      feature3: 0
      // add all features your model expects
    }),
  });

  const data = await response.json();
  console.log("🔮 Future congestion prediction:", data.prediction);
}

getFuturePrediction();
```

```bash
node node_predict.js
# Output: 🔮 Future congestion prediction: HIGH
```

---

## 🛠️ Tech Stack

```
🐍 Python          →  ML model training, data preprocessing
🌲 scikit-learn    →  Random Forest Classifier
⚡ FastAPI          →  High-performance prediction API
🦄 Uvicorn         →  ASGI server
🟢 Node.js         →  Frontend / API integration layer
📦 joblib / pandas →  Model serialization & data handling
```

---

## 🔭 Roadmap

- [ ] **Multi-intersection orchestration** — coordinate signals across an entire city grid
- [ ] **Live sensor data streams** — real-time feeds from cameras and IoT sensors
- [ ] **Visual dashboard** — watch predictions roll in on a live map
- [ ] **Adaptive signal control** — fully automatic, no human in the loop
- [ ] **Cloud deployment** — scale beyond localhost to city infrastructure

---

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#forest)
- [Node.js Fetch API](https://nodejs.org/en/blog/announcements/v18-release-announce#fetch-api)

---

## 🤝 Contributing

Pull requests are welcome! If you have ideas to make traffic smarter, let's build it together.

---

<p align="center">
  Built with ☕, 🧠, and a deep hatred of rush-hour traffic.
</p>
