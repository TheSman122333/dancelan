🕺 Just Dance Project
Welcome to my Just Dance remake called DanceLAN! This project brings the fun of dancing and mashes it up with a workout! Compare your local score with your friends, and compete to be the best.

🎯 Features
🎵 Choose a song and start dancing

📷 Real-time pose tracking using webcam

🧠 Intelligent scoring based on accuracy and timing

📈 Progress and performance feedback

🔥 Local High Score

🎨 Interactive and dynamic UI

🛠️ Built With
Python

OpenCV

MediaPipe (for pose detection)

HTML

JS

CSS

JSON

🚀 Getting Started
Prerequisites
Make sure you have Python 3.8+ installed.
pip install -r requirements.txt
(Only do this, if you want to add more custom songs. If not, just use the web deployed version)

🧪 How It Works
Pose Estimation: The camera captures your movement frame-by-frame using MediaPipe.

Pose Matching: Each frame is compared to a "reference" dance move dataset, stored in [songname].json.

Scoring: The system gives you points based on how closely your pose matches the ideal one and how well-timed your movements are with the beat.

Feedback: After the dance, you get a detailed report of your performance.

🎮 Dance Modes
Single Player: Dance solo and improve your scores.

📁 Folder Structure
dancelan
├── index.html          
├── songs/[songname].mp3               
├── data/[songname].json 
├── requirements.txt
├── nosignal.png
├── vidtolandmarks.py
└── README.md
🎯 Goals / Roadmap
 Multiplayer support
 Add more songs and move sets
 Create a custom dance editor

💡 Future Ideas
AI-generated dances

Integration with smartphones as controllers

Upload-your-own-song support

📜 License
This project is licensed under the All Rights Reserved License!

