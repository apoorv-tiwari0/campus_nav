# 📍 Vision-Based Campus Navigation System

## 🧠 Overview

This project implements a **vision-based navigation system** for a college campus using image recognition and graph-based routing.

Instead of GPS, the system determines a user's location by matching a camera image against a database of campus pathway images, then computes the shortest route to a selected destination.

The backend is built using:

* 🧩 Deep Learning image embeddings (MobileNet)
* ⚡ FAISS vector similarity search
* 🗺️ Graph-based navigation routing
* 🎯 Landmark-based human navigation output
* 🎨 Digital Image Processing (CLAHE + Gaussian filtering)

This allows reliable navigation even in GPS-unfriendly environments such as large campuses or indoor areas.

---

## 🏗️ System Architecture

```
User Photo
   ↓
DIP Preprocessing (CLAHE + Gaussian Blur)
   ↓
CNN Embedding Model
   ↓
FAISS Similarity Search
   ↓
Matched Campus Frame
   ↓
Graph Routing Engine
   ↓
Human-Readable Navigation Instructions
```

---

## 📂 Repository Structure

```
backend/
 ├── app/
 │    ├── main.py              # FastAPI backend server
 │    ├── model.py             # CNN embedding generator
 │    ├── search.py            # FAISS similarity search
 │    ├── graph.py             # Campus routing engine
 │    ├── utils.py             # preprocessing + helper functions
 │    ├── build_graph.py       # auto-generate campus graph
 │    └── build_landmarks.py   # auto-generate destination mapping
 │
 ├── data/
 │    ├── graph.json           # generated campus topology
 │    ├── landmarks.json       # human destination mapping
 │    └── embeddings/          # cached embeddings (auto-generated)
 │
 └── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone repository

```
git clone <repo-url>
cd campus_nav/backend
```

---

### 2. Create virtual environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
pip install opencv-python
```

---

## 📸 Dataset Setup (VERY IMPORTANT)

The system requires campus pathway images.

### Expected dataset structure:

```
dataset_raw/
   GTKNS/
      frame_00001.jpg
   KNSTFB/
      frame_00001.jpg
   ...
```

Each folder represents:

```
START → END pathway
```

---

### Copy images into backend:

```
backend/data/images/<folder>/<frames>
```

⚠️ Keep folder names intact.
Do NOT flatten image files.

---

## 🗺️ Generate Navigation Graph

From:

```
backend/app/
```

Run:

```
python build_graph.py
```

---

## 📍 Generate Landmark Mapping

Run:

```
python build_landmarks.py
```

---

## 🚀 Start Backend Server

From:

```
backend/
```

Run:

```
uvicorn app.main:app --reload
```

Open browser:

```
http://127.0.0.1:8000/docs
```

---

## 🧭 Navigation API

### POST `/navigate`

Upload campus image and destination name.

Example response:

```
{
  "location": "Boys Hostel",
  "destination": "Juice World",
  "confidence": 0.91,
  "instructions": [
      "Start at Boys Hostel",
      "Move towards North Canteen",
      "Move towards Architecture Block",
      "Move towards Cafe Coffee Day",
      "Move towards Juice World",
      "You have arrived"
  ]
}
```

---

## 🧪 First Run Behavior

On first launch:

* embeddings are generated for all images
* saved into cache file

Later launches:

* embeddings load instantly

---

## 🎨 Digital Image Processing Used

Before feature extraction, the system applies:

* Adaptive Histogram Equalization (CLAHE)
* Gaussian filtering
* color space conversion

These improve robustness against lighting variation and noise.

---

## 👥 For Team Members Continuing Development

### Android Integration

The mobile app must:

1. Capture camera image
2. Send POST request to `/navigate`
3. Display returned instructions
4. Optionally show confidence score

---

### Possible Future Improvements

* 3D campus visualization
* multi-image localization
* voice navigation instructions
* confidence-based retake suggestion
* offline embedding on device

---

## 🏁 Project Status

✅ Backend navigation system complete
✅ Image localization working
✅ Graph routing working
✅ Human-readable instructions working
🔄 Android frontend integration pending

---

## 📜 License

Academic project – internal educational use.

---
