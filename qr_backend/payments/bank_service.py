"""
Modul zur Simulation einer Bankschnittstelle.
"""

import uuid

def initiate_payment(data):
    """
    Simuliert die Einleitung einer Zahlungsanforderung bei einer Bank.
    Gibt eine Transaktions-ID und eine Zahlungs-URL zurück.
    """
    transaction_id = str(uuid.uuid4())
    payment_url = f"https://demo-bank.example.com/pay/{transaction_id}"
    return {
        "transaction_id": transaction_id,
        "payment_url": payment_url
    }

def check_status(transaction_id):
    """
    Simuliert das Abfragen des Zahlungsstatus einer Transaktion.
    Mögliche Rückgabewerte: 'pending', 'completed', 'failed'.
    """
    # Zum Test immer 'completed' zurückgeben
    return {
        "transaction_id": transaction_id,
        "status": "completed"
    }
