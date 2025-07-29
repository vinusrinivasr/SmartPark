# Parking App
This is a web app designed to streamline 4-wheeler parking management. It features separate user and admin roles, allowing users to sign up, log in, and manage their parking reservations, while the admin can manage all parking lots, manage users, and perform lot searches efficiently.


## 🤖 Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Auth:** Session-based login for both user and admin


## 📝 Features
### User
- Register and log in
- Search for parking lots by location/pincode
- Book and release parking spots
- View reservation history
- Edit Profile and Change Password

### Admin
- No registration — exists by default
- Add/Edit/Delete parking lots and spots
- View all users and their reservations
- Search for parking lots by location/pincode


## 🏗️ Models/Tables
- **User:** `user_id`, `username`, `password`, `name`, `address`, `pincode`
- **ParkingLot:** `id`, `location`, `price`, `address`, `pin_code`, `max_spots`
- **ParkingSpot:** `id`, `lot_id`, `status`
- **Reservation:** `id`, `spot_id`, `user_id`, `parking_timestamp`, `leaving_timestamp`, `parking_cost`, `vehicle_no`


## ⚙️ Installation and Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/24f1001669/parking-app.git
   cd parking-app
   ```

2. **Create virtual environment (optional)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  --> Linux/ Mac                  .venv\Scripts\activate  --> Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the database**
   ```bash
   python create_db.py
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

Go to [http://localhost:5000] and you must see the app running


## 🔐 Default Admin Credentials
Username: admin
Password: admin123


## 👥 Contributors
- **Vinu Srinivas R (24f1001669)** — Developer