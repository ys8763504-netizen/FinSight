# 💰 FinSight - Expense Management System

FinSight is a modern web-based expense management system built using Django. It helps users track their daily expenses, manage monthly budgets, and gain insights into their spending habits.

---

## 🚀 Features

* 👤 User Registration & Login
* 🛡️ Admin Panel (Staff Access)
* 💸 Add / Edit / Delete Expenses
* 📅 Monthly Expense Tracking
* 📊 Budget Management (Month-wise)
* ⚠️ Budget Limit Alerts
* 📈 Dashboard Overview
* 📱 Responsive UI Design

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (Default Django DB)
* **Authentication:** Django Built-in Auth System

---

## 📂 Project Structure

```
FinSight/
│── manage.py
│── db.sqlite3
│
├── FinSight/          # Project settings
│
├── app1/              # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
└── templates/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/finsight.git
cd finsight
```

### 2️⃣ Create virtual environment

```bash
python -m venv env
```

### 3️⃣ Activate environment

* Windows:

```bash
env\Scripts\activate
```

* Mac/Linux:

```bash
source env/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Apply migrations

```bash
python manage.py migrate
```

### 6️⃣ Create superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7️⃣ Run server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

* **Admin Users:** Access admin panel using `is_staff=True`
* **Normal Users:** Manage personal expenses and budgets

---

## 📊 Core Functionalities

### ✅ Expense Management

* Add daily expenses
* Categorize spending
* Track monthly totals

### ✅ Budget Control

* Set monthly budget
* Prevent overspending
* Get alerts when exceeding limit

### ✅ Dashboard Insights

* Total expenses
* Monthly expenses
* Remaining budget

---

## ⚠️ Important Notes

* Budget is stored in **YYYY-MM format**
* Expense filtering is based on **month & year**
* Uses Django session & authentication system

---

## 🧠 Future Improvements

* 📉 Charts & Graphs (Analytics)
* 📤 Export Reports (PDF/Excel)
* 🔔 Email Notifications
* 🌙 Dark Mode UI
* 📱 Mobile App Version

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the project and submit pull requests.

---

## 📧 Contact

For any queries or suggestions:

* Developer: **Yash Solanki**

---

## ⭐ Acknowledgements

* Django Documentation
* Open-source community

---

## 📌 License

This project is for educational purposes.
