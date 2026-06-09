import time
import random
import redis
import json

# KONFIGURATION
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    print("Verbunden mit Redis")
except Exception as e:
    print(f"Konnte nicht mit Redis verbinden: {e}")
    r = None

CACHE_TTL = 15  # Sekunden (für Phase 4)

def query_product_db(product_id):
    """Simuliert eine langsame relationale Datenbank-Abfrage mit vielen JOINs"""
    print(f"... Führe 5 JOINs in der SQL-Datenbank für '{product_id}' aus (bitte warten) ...")
    time.sleep(2.2)  # Künstliche Verzögerung

    # Simuliertes Datenbank-Resultat
    product = {
        "id": product_id,
        "name": f"Premium Artikel {product_id}",
        "description": "Ein hervorragendes Produkt für den Alltag.",
        "price": random.choice([19.90, 49.00, 129.50]),
        "stock": random.randint(0, 50)
    }
    return json.dumps(product)


def get_product(product_id):
    """
    Cache-Aside Pattern:
    1. Prüfen ob der Key in Redis existiert (Cache Hit?)
    2. Cache Hit  -> Wert direkt aus Redis zurückgeben
    3. Cache Miss -> Langsame DB-Abfrage, Ergebnis in Redis speichern (mit TTL), zurückgeben
    """
    cache_key = f"product:{product_id}"

    # 1. Cache-Lookup
    if r is not None:
        cached_value = r.get(cache_key)
        if cached_value is not None:
            print(f"[CACHE HIT] Key '{cache_key}' gefunden – Daten aus Redis geladen.")
            return cached_value

    # 2. Cache Miss – Daten aus der "Datenbank" holen
    print(f"[CACHE MISS] Key '{cache_key}' nicht im Cache – Datenbankabfrage wird gestartet.")
    result = query_product_db(product_id)

    # 3. Ergebnis in Redis speichern (mit TTL für automatischen Ablauf)
    if r is not None:
        r.setex(cache_key, CACHE_TTL, result)
        print(f"[CACHE SET] Ergebnis unter '{cache_key}' für {CACHE_TTL}s gespeichert.")

    return result


# TEST-ABLAUF
test_id = "PROD-9901"

print("\n--- Erster Aufruf (Cache Miss - sollte langsam sein) ---")
start = time.time()
print(f"Produktdaten: {get_product(test_id)}")
print(f"Dauer: {time.time() - start:.4f} Sekunden")

print("\n--- Zweiter Aufruf (Cache Hit - sollte blitzschnell sein) ---")
start = time.time()
print(f"Produktdaten: {get_product(test_id)}")
print(f"Dauer: {time.time() - start:.4f} Sekunden")
