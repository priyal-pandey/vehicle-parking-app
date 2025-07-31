# Vehicle-Parking-App-V1

MAD1 Project T22025 - LOT AND FOUND

This is a Flask-based web application that allows users to book, release, and manage parking spots while allowing an admin to control parking lot infrastructure, view summaries, and monitor reservations.


### 1. Clone the repository
```
git clone https://github.com/23f2005558/vehicle-parking-app.git
cd vehicle-parking-app
```

### 2. Set up the virtual environment
#### For Windows:
```
python -m venv venv
venv\Scripts\activate
```

#### For Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy the sample file and adjust values as needed.
```
cp .env.sample .env
```

### 5. Run the Flask app
```
flask run
```

### 7. Access the App
Open your browser and go to: `http://localhost:5000`

---

## Default Admin Credentials

- **Email:** `admin@lotandfound.com`
- **Password:** `admin`

---

## File Structure Overview

- `app.py` – Main application setup and Flask app runner  
- `routes.py` – Controller logic and routing  
- `models.py` – SQLAlchemy database models  
- `config.py` – Centralized config class  
- `.env.sample` – Sample environment variables  
- `templates/` – HTML pages (user/admin folders)  
- `static/` – Static files like CSS and images  
- `requirements.txt` – Python dependencies  
- `README.md` – Project instructions  
- `.gitignore` – Ignores venv, __pycache__, etc.

---
