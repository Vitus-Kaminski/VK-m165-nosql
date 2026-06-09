# KN04 – Gruppe C: Login & Auth Server
## Abgaben & Antworten

---

## Phase 1 – Infrastruktur & Cloud-Init

**Datei:** `phase1/cloud-init.yaml`

### Antwort: Was ist das Hauptmerkmal einer Time-Series Database (TSDB)?

Eine Time-Series Database speichert Datenpunkte immer zusammen mit einem Zeitstempel und ist darauf optimiert, zeitlich geordnete Sequenzen effizient zu schreiben und abzufragen. Im Gegensatz zu einer relationalen Datenbank (die beliebige Datensätze verwaltet) dreht sich bei einer TSDB alles um den zeitlichen Verlauf eines Wertes – z. B. „Wie viele Logins pro Sekunde gab es in den letzten 5 Minuten?"

### Antwort: Warum sind Terminal-Logs in der Cloud ungeeignet?

In einer modernen Cloud-Umgebung mit hunderten von Servern müsste man sich manuell auf jeden einzelnen Server per SSH verbinden, um dessen Logs zu lesen – das ist bei einem Fehler um 3 Uhr nachts schlicht nicht praktikabel. Terminal-Logs sind zudem flüchtig (verschwinden bei Neustart), nicht durchsuchbar über alle Server hinweg, und geben keinen Überblick über Trends oder Muster im Gesamtsystem. Ein zentrales Monitoring-System wie Prometheus sammelt die Daten automatisch und erlaubt es, Anomalien in Echtzeit über alle Instanzen hinweg zu erkennen.

---

## Phase 2 – Instrumentierung (Code)

**Datei:** `phase2/script.py`

### Erklärung der Änderungen

| Aufgabe | Was wurde gemacht |
|---|---|
| Import | `from prometheus_client import start_http_server, Counter` |
| Metrik | `Counter('auth_attempts_total', '...', ['methode', 'status'])` – zwei Labels für Methode und Ergebnis |
| Erhöhen | `auth_metric.labels(methode=method, status=status).inc()` in `process_login()` |
| Server | `start_http_server(8000)` vor der Endlosschleife |

---

## Phase 3 – Prometheus Konfiguration

**Datei:** `phase3/prometheus.yml`

Den folgenden Block in `/etc/prometheus/prometheus.yml` am Ende einfügen:

```yaml
  - job_name: 'login_server'
    static_configs:
      - targets: ['localhost:8000']
```

Danach Dienst neu starten:
```bash
sudo systemctl restart prometheus
sudo systemctl status prometheus
```

---

## Phase 4 – Grafana Visualisierung

**Login:** http://<Public-IP>:3000 → admin / admin

**Data Source URL:** `http://localhost:9090`

### Empfohlene PromQL-Queries für die Panels

**Panel 1 – Login-Rate pro Methode (nur Erfolge):**
```promql
rate(auth_attempts_total{status="success"}[1m])
```

**Panel 2 – Fehlerrate pro Methode:**
```promql
rate(auth_attempts_total{status="error_invalid_credentials"}[1m])
```

### Antwort: Was passiert bei unterschiedlichen Time Ranges?

Bei einer grossen Zeitspanne (z. B. „Last 1 hour") aggregiert Grafana viele Datenpunkte zu einem einzigen Pixel zusammen (Downsampling/Glättung), wodurch die Linie glatter und weniger detailliert wirkt. Bei einer kleinen Zeitspanne (z. B. „Last 5 minutes") sind alle einzelnen Messpunkte sichtbar, was zu einer „zackigeren" Darstellung führt, die die tatsächliche Variabilität zeigt.

---

## Phase 5 – Architektur-Reflexion

### Warum `localhost` in Prometheus und Grafana?

Prometheus und das Python-Script laufen auf **demselben EC2-Server**. Prometheus scrapt also `localhost:8000`, weil das Script lokal auf demselben Host läuft – keine Netzwerkkommunikation über das Internet nötig. Ebenso greift Grafana auf `localhost:9090` zu, weil Grafana ebenfalls auf dieser Instanz läuft. Nur **Sie** als Nutzer greifen von aussen über die Public-IP zu – die Dienste selbst kommunizieren intern über loopback.

### Labels vs. SQL-Tabellen – welcher Vorteil?

In SQL müsste man für jede neue Kombination (z. B. neue Methode "sso_saml") eine neue Tabelle oder Spalte anlegen und die Abfragen anpassen. Mit Prometheus-Labels fügt man einfach einen neuen Label-Wert hinzu – Prometheus erstellt automatisch eine neue Zeitreihe. Bei der Auswertung kann man mit einer einzigen PromQL-Query über alle Dimensionen aggregieren oder filtern (z. B. `{status="error"}` für alle Fehlermethoden auf einmal), ohne Schema-Änderungen.

### Die Zeitstempel-Magie (Pull-Modell)

Im Python-Code wird **nie** manuell ein Timestamp gesetzt, weil das Pull-Modell diesen Schritt übernimmt: Prometheus kontaktiert aktiv alle 15 Sekunden (standardmässig) den `/metrics`-Endpunkt und notiert beim Abholen der Daten selbst die aktuelle Uhrzeit. Dieser Zeitpunkt des Scrapings wird als Timestamp in der TSDB gespeichert. Die App muss sich darum nicht kümmern – sie stellt nur den aktuellen Zählerstand bereit, Prometheus gibt ihm den zeitlichen Kontext.
