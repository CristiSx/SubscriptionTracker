# Subscription Tracker

## Descriere

Subscription Tracker este o aplicație web dezvoltată cu Flask care permite utilizatorilor să își gestioneze abonamentele recurente și cheltuielile unice într-un singur loc. Aplicația oferă statistici privind cheltuielile, proiecții financiare pentru următoarele 12 luni și notificări automate prin email înainte de reînnoirea sau încetarea unui abonament.

---

## Funcționalități

### Autentificare și gestionare utilizatori

* Înregistrare cont nou
* Autentificare utilizator
* Deconectare utilizator
* Parole stocate securizat folosind algoritmul `scrypt`

### Gestionarea abonamentelor

* Adăugare abonament
* Vizualizare abonamente active
* Ștergere abonamente
* Alegerea ciclului de facturare (lunar/anual)
* Stabilirea datei primei plăți și a datei de încetare

### Gestionarea cheltuielilor unice

* Adăugare cheltuieli fără subscriere
* Vizualizare cheltuieli
* Ștergere cheltuieli

### Dashboard

* Total cheltuieli
* Număr abonamente active
* Cost mediu per serviciu

### Proiecție financiară

* Estimarea cheltuielilor pentru următoarele 12 luni
* Grafic interactiv realizat cu Chart.js
* Tabel detaliat al costurilor estimate

### Sistem de notificări

* Notificări prin email înainte de reînnoirea unui abonament
* Notificări prin email înainte de încetarea unui abonament
* Verificare automată zilnică folosind APScheduler

---

## Tehnologii utilizate

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-Mail
* APScheduler

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2
* Chart.js

### Bază de date

* PostgreSQL (Neon Database)

---

## Arhitectura aplicației

Aplicația urmează modelul MVC (Model – View – Controller):

### Models

* User
* Subscription
* OneTimeExpense

### Views

* login.html
* register.html
* dashboard.html
* viewall.html
* projection.html

### Controllers

* auth.py
* home.py

---

## Structura bazei de date

### User

| Câmp     | Tip     |
| -------- | ------- |
| id       | Integer |
| username | String  |
| email    | String  |
| password | String  |

### Subscription

| Câmp            | Tip         |
| --------------- | ----------- |
| id              | Integer     |
| name            | String      |
| cost            | Float       |
| first_bill_date | Date        |
| due_date        | Date        |
| billing_cycle   | String      |
| user_id         | Foreign Key |

### OneTimeExpense

| Câmp    | Tip         |
| ------- | ----------- |
| id      | Integer     |
| name    | String      |
| cost    | Float       |
| date    | Date        |
| user_id | Foreign Key |

---

## Securitate

* Parolele sunt hash-uite folosind algoritmul `scrypt`.
* Utilizatorii pot accesa doar propriile date.
* Rutele sensibile sunt protejate cu `@login_required`.
* Credențialele sunt stocate în fișierul `.env`.

---

## Instalare

1. Clonarea proiectului:

```bash
git clone <repository_url>
cd SubscriptionTracker
```

2. Crearea mediului virtual:

```bash
python -m venv venv
```

3. Activarea mediului virtual:

Windows:

```bash
venv\Scripts\activate
```

Linux / MacOS:

```bash
source venv/bin/activate
```

4. Instalarea dependențelor:

```bash
pip install -r requirements.txt
```

5. Configurarea fișierului `.env`:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_app_password
```

6. Rularea aplicației:

```bash
python app.py
```

---

