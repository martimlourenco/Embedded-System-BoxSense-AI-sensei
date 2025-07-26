📦 Sensei – Embedded-System Box Condition Detection w AI
---
```
   _____ ______ _   _  _____ ______ _____  
  / ____|  ____| \ | |/ ____|  ____|_   _| 
 | (___ | |__  |  \| | (___ | |__    | |   
  \___ \|  __| | . ` |\___ \|  __|   | |   
  ____) | |____| |\  |____) | |____ _| |_  
 |_____/|______|_| \_|_____/|______|_____| 
                                           
                                           
```

---
**Sensei** is an embedded system designed to monitor and detect the condition of cardboard boxes using a custom-trained YOLOv8 model.

### 🔍 What it does
- Captures real-time images from a Raspberry Pi-based camera.
- Detects whether a box is **damaged** or **in good condition**.
- Displays results with timestamps and sends them to an external OutSystems API.
- Provides a live feed and a simple user interface (Tkinter).

### 🧠 Model Info
- Trained using [YOLOv8](https://github.com/ultralytics/ultralytics) in Google Colab.
- Dataset created and annotated via [Roboflow](https://roboflow.com).
- Best model weights saved as `best.pt`.



### 🚀 Getting Started
Make sure you have:
- Python 3.8+
- Ultralytics (YOLOv8)
- OpenCV, Pillow, Tkinter, Requests

```bash
pip install ultralytics opencv-python pillow requests
```
## Publications

- [My article on Sensei ](https://media.licdn.com/dms/document/media/v2/D4D2DAQFMQjEvsGZRWA/profile-treasury-document-pdf-analyzed/B4DZUel3y7HIAk-/0/1739975003673?e=1754524800&v=beta&t=fIbaEfO_92AYDacqnKNckN6EdV73JdBM2zI5mCyoHq4)

