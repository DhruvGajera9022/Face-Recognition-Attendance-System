# 🎓 Face Recognition Attendance System

A real-time face recognition attendance system built using **OpenCV**, **scikit-learn**, and **Streamlit**. The system captures face data, trains a KNN classifier, and logs attendance with timestamps. Features a live dashboard for tracking attendance records.

---

## 📌 Features

- 🎥 **Real-time face detection and recognition** via webcam
- 👨‍🏫 **KNN-based face recognition** (no deep learning required)
- 💾 **Daily attendance logging** in CSV format
- 🔊 **Voice feedback** on successful attendance (Windows only)
- 📊 **Live Streamlit dashboard** with auto-refresh
- 🧠 **Easy user registration** with sample capture script
- 🛡️ **Error handling** and duplicate entry prevention

---

## 📂 Project Structure

```
Face-Recognition-Attendance-System/
├── data/
│   ├── haarcascade_frontalface_default.xml
│   ├── faces_data.pkl
│   └── names.pkl
├── Attendance/
│   └── Attendance_<DD-MM-YYYY>.csv
├── add_faces.py          # Capture face data for new users
├── test.py               # Real-time face recognition and attendance
├── app.py                # Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Webcam/Camera access
- Windows OS (for voice feedback feature)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DhruvGajera9022/Face-Recognition-Attendance-System.git
   cd Face-Recognition-Attendance-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create necessary directories**
   ```bash
   mkdir data Attendance
   ```

### Usage

#### Step 1: Register New Users

Run the face capture script to add new users to the system:

```bash
python add_faces.py
```

- Enter the user's name when prompted
- Look directly at the camera
- The system will capture multiple face samples
- Data is automatically saved to `data/faces_data.pkl` and `data/names.pkl`

#### Step 2: Start Attendance System

Launch the real-time attendance marking system:

```bash
python attendance.py
```

**Controls:**
- Press **'o'** to mark attendance for recognized faces
- Press **'q'** to quit the application

#### Step 3: View Dashboard

Start the Streamlit dashboard to monitor attendance:

```bash
streamlit run app.py
```

**Dashboard Features:**
- Displays today's attendance records
- Auto-refreshes every 2 seconds
- Shows attendance count and timestamps
- Clean, responsive interface

---

## 🔧 Configuration

### Face Detection Settings

The system uses Haar Cascade classifier for face detection. You can adjust detection parameters in the code:

- `scaleFactor`: Image pyramid scaling parameter
- `minNeighbors`: Minimum neighbors required for detection
- `minSize`: Minimum face size for detection

### KNN Classifier

The K-Nearest Neighbors classifier can be tuned by modifying:

- `n_neighbors`: Number of neighbors to consider
- `weights`: Weight function for predictions

---

## 📊 Data Storage

### Face Data
- **faces_data.pkl**: Encoded face features
- **names.pkl**: Corresponding user names

### Attendance Records
- Stored in `Attendance/` directory
- File format: `Attendance_DD-MM-YYYY.csv`
- Contains: Name, Time, Date

---

## 🛠️ Tech Stack

- **Python** - Core programming language
- **OpenCV** - Computer vision and face detection
- **scikit-learn** - KNN classifier implementation
- **Streamlit** - Web dashboard framework
- **pywin32** - Text-to-speech functionality (Windows)
- **Pandas** - Data manipulation and CSV handling
- **NumPy** - Numerical computations

---

## 🔍 How It Works

1. **Face Registration**: Captures multiple face samples using OpenCV's Haar Cascade
2. **Feature Extraction**: Converts face images to numerical features
3. **Model Training**: KNN classifier learns from face features
4. **Real-time Recognition**: Webcam feed is processed for face detection
5. **Attendance Logging**: Recognized faces trigger attendance marking
6. **Dashboard Display**: Streamlit shows live attendance data

---

## 🚨 Troubleshooting

### Common Issues

**Camera not detected:**
- Check camera permissions
- Ensure no other applications are using the camera
- Try changing camera index in code (0, 1, 2...)

**Face not recognized:**
- Ensure good lighting conditions
- Register more face samples for the user
- Check if face is clearly visible and frontal

**Voice feedback not working:**
- Feature only available on Windows
- Install pywin32: `pip install pywin32`

**Dashboard not loading:**
- Check if Streamlit is properly installed
- Ensure port 8501 is available
- Try running: `streamlit run app.py --server.port 8502`