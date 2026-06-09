import time
import random

# --- AUFGABE 1: IMPORTIEREN ---
from prometheus_client import start_http_server, Counter

# --- AUFGABE 2: METRIK ERSTELLEN ---
auth_metric = Counter(
    'auth_attempts_total',
    'Anzahl der Logins',
    ['methode', 'status']
)

def process_login():
    methods = ['password', 'oauth_google', 'mfa_token']
    method = random.choice(methods)

    # 70% Erfolgsquote
    if random.random() > 0.3:
        status = 'success'
        print(f"[AUTH] Login erfolgreich via {method}.")
    else:
        status = 'error_invalid_credentials'
        print(f"[AUTH] FEHLER: Falsche Daten via {method}!")

    # --- AUFGABE 3: METRIK ERHÖHEN ---
    auth_metric.labels(methode=method, status=status).inc()

if __name__ == '__main__':
    print("Starte Login Server Simulation...")
    # --- AUFGABE 4: METRIK-SERVER STARTEN ---
    start_http_server(8000)

    while True:
        process_login()
        time.sleep(random.uniform(0.1, 1.0))
