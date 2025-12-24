💰 Spending Tracker Web Application

Spending Tracker เป็นเว็บแอปพลิเคชันสำหรับช่วยผู้ใช้ บันทึกรายจ่าย, ตั้งงบประมาณ, และ ติดตามการใช้เงิน ของตนเอง
พัฒนาโดยใช้ React (Frontend), Django (Backend) และ MongoDB (Database)

✨ Features

🔐 สมัครสมาชิก / เข้าสู่ระบบ

👤 จัดการข้อมูลผู้ใช้ (Profile + รูปโปรไฟล์)

💸 บันทึกรายจ่าย

🗂 จัดหมวดหมู่รายจ่าย

📊 ตั้งงบประมาณในแต่ละหมวด

⚠️ แจ้งเตือนเมื่อใช้เงินใกล้หรือเกินงบประมาณ

📈 ดูข้อมูลรายจ่ายย้อนหลัง

🛠 Tech Stack
Frontend

React (JSX)

JavaScript / HTML / CSS

Axios (เรียก API)

React Hooks

Backend

Python

Django

Django REST Framework

MongoDB (NoSQL Database)

Database

MongoDB

MongoDB Compass / MongoDB Atlas

## 🗂 Project Structure

```bash
spendingtrackerappproject/
├── backend/
│   ├── mybackend/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   │
│   ├── media/
│   │   └── profile_pictures/
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── myreactapp/
│   └── myfronend/
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── services/
│       │   └── App.jsx
│       │
│       ├── package.json
│       └── vite.config.js
│
└── README.md
```


⚙️ Installation & Setup
1️⃣ Clone Project
git clone https://github.com/your-username/spending-tracker.git
cd spendingtrackerappproject

2️⃣ Backend Setup (Django)
cd backend
python -m venv myenv
myenv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py runserver



3️⃣ Frontend Setup (React)
cd myreactapp/myfronend
npm install
npm run dev
