# QR Pay Generator

Ein vollständiges Projekt zur Erzeugung und zum Scannen von SEPA-Zahlungs-QR-Codes mit moderner Frontend- und Backend-Architektur.

---

## Projektübersicht

**Backend:** Django (REST API, QR-Code-Generierung, User, Payment)  
**Frontend:** Quasar/Vue (UI, QR-Scan, QR-Generierung)  
**DevOps:** Empfohlen: Virtuelle Umgebung für Python, Node.js für das Frontend

---

## Projektstruktur

```
project-root/
│
├── qr_backend/         # Django-Backend (API, QR-Code-Generierung, User, Payment)
│   ├── manage.py
│   ├── requirements.txt
│   ├── qr_payment_service/   # Django-Projekt (settings, urls, wsgi, asgi)
│   └── media/                # QR-Codes und andere Medien
│
├── qr_frontend/        # Quasar/Vue-Frontend (UI, QR-Scan, QR-Generierung)
│   ├── src/
│   ├── package.json
│   └── quasar.conf.js
│
├── venv/               # Virtuelle Python-Umgebung
│
└── README.md           # Diese Datei
```

---

## Features

- **SEPA QR-Code-Generator:** Erstellen Sie EPC-konforme Zahlungs-QR-Codes.
- **QR-Code-Scanner:** Scannen Sie SEPA-QR-Codes direkt im Browser.
- **Vorlagenverwaltung:** Speichern, bearbeiten und löschen Sie eigene Zahlungs-Vorlagen.
- **Benutzerverwaltung:** Login/Logout, Authentifizierung.
- **Simulation von Zahlungen:** Keine echten Transaktionen, nur Demo.
- **Moderne UI:** Responsive, übersichtlich und einfach zu bedienen.

---

## Voraussetzungen

- **Backend:** Python 3.10+, Django 5+, djangorestframework, qrcode, Pillow
- **Frontend:** Node.js 18+, Quasar CLI, npm oder yarn

---

## Installation

### Backend (Django)

```bash
cd qr_backend
python -m venv venv
venv\Scripts\activate  # Windows
# oder: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (Quasar/Vue)

```bash
cd qr_frontend
npm install
quasar dev
```

---

## Nutzung

1. **Frontend starten:** Öffnen Sie [http://localhost:9000](http://localhost:9000) im Browser.
2. **Backend starten:** API läuft standardmäßig auf [http://127.0.0.1:8000](http://127.0.0.1:8000).
3. **QR-Code generieren:** Zahlungsdaten eingeben und QR-Code erstellen.
4. **QR-Code scannen:** Mit Webcam oder Smartphone-Frontkamera scannen.
5. **Vorlagen:** Eigene Vorlagen speichern, bearbeiten oder löschen.

---

## Hinweise

- **QR-Codes werden im Backend im Verzeichnis `/media/qr_codes/` gespeichert.**
- **Alle Zahlungen sind Simulationen – keine echten Banktransaktionen!**
- **Für Produktion: Einstellungen für Sicherheit, CORS, Datenbank usw. anpassen.**