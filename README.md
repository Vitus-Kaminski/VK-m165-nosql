# Cloud & Datenbanken – Modulübersicht

Dieses Repository enthält alle Abgaben und Dokumentationen für das Modul.

---

## Übersicht

| KN | Thema | Status |
|----|-------|--------|
| [KN02](#kn02) | REST-API & JSON-Datenmodellierung | ✅ Abgeschlossen |
| [KN03](#kn03) | Redis In-Memory und Caching-Strategien | ✅ Abgeschlossen |
| [KN04](#kn04) | Full-Stack Monitoring mit Prometheus & Grafana | ✅ Abgeschlossen |
| [KN05](#kn05) | Graphdatenbanken & Neo4j | ✅ Abgeschlossen |

---

## KN02

**Thema:** REST-API & JSON-Datenmodellierung

**Inhalt:**
- JSON-Datenstrukturen für Rezepte, Zutaten und Kategorien
- REST-API Design und Dokumentation

📁 [Zur KN02-Dokumentation](./KN02/KN02.md)

```
KN02/
├── KN02.md
├── recipes.json
├── ingredients.json
├── categories.json
└── image.png / image-1.png / image-2.png / image-3.png / image-4.png
```

---

## KN03

**Thema:** Redis In-Memory und Caching-Strategien  
**Szenario:** E-Commerce Produkt-Katalog

**Inhalt:**
- EC2-Instanz mit Redis via Cloud-Init provisioniert
- Cache-Aside Pattern implementiert (Python)
- Performance-Vergleich Cache Miss vs. Cache Hit (~4400× Beschleunigung)
- Cache Invalidation mit TTL demonstriert

📁 [Zur KN03-Dokumentation](./KN03/README.md)

```
KN03/
├── README.md
├── script.py
├── cloud-init.yaml
├── phase1/
│   └── inboundrules.png
├── phase3/
│   └── redisping.png
└── phase4/
    └── Resdisaufruf.png
```

---

## KN04

**Thema:** Full-Stack Monitoring mit Prometheus & Grafana  
**Szenario:** Login & Auth Server (Szenario C)

**Inhalt:**
- EC2-Instanz mit Prometheus & Grafana via Cloud-Init provisioniert
- Python-Script mit `prometheus_client` instrumentiert (Counter mit Labels)
- Prometheus Scraping auf Port 8000 konfiguriert
- Grafana Dashboard mit Success/Error-Panels erstellt

📁 [Zur KN04-Dokumentation](./KN04/KN04.md)

```
KN04/
├── KN04.md
├── ABGABE_ANTWORTEN.md
├── logs.png
├── Prometheus.png
├── prometues9090connection.png
├── Grafana.png
├── Grafananewconnection.png
├── Dashboards.png
├── updatepassword.png
├── Screenshot 2026-06-16 144603.png   ← /metrics Endpoint
├── Screenshot 2026-06-16 144957.png   ← Prometheus Targets UP
├── phase1/
├── phase2/
└── phase3/
```

---

## KN05

**Thema:** Graphdatenbanken & Neo4j  
**Szenario:** Recommendation Engine (E-Commerce)

**Inhalt:**
- Neo4j AuraDB Cloud-Instanz aufgesetzt
- Graph mit User/Product-Knoten und REVIEWED-Kanten (mit rating-Attribut) erstellt
- Fehlerhafte Recommendation-Query analysiert und korrigiert
- Index-Free Adjacency vs. SQL JOINs verglichen

📁 [Zur KN05-Dokumentation](./KN05/KN05.md)

```
KN05/
├── KN05.md
├── neo4jaura.png
├── neo4jkanten.png
├── Rating.png
└── maustastatur.png
```

---

## Datenbankvergleich

| Kriterium | SQL (relational) | Redis (In-Memory) | Neo4j (Graph) | Prometheus (TSDB) |
|---|---|---|---|---|
| **Stärke** | Strukturierte Abfragen, JOINs | Extrem schnell, Caching | Beziehungen & Traversierung | Zeitreihen, Monitoring |
| **Datenmodell** | Tabellen & Zeilen | Key-Value | Knoten & Kanten | Metriken & Zeitstempel |
| **Typischer Use Case** | Transaktionen, ERP | Session-Cache, Leaderboards | Empfehlungen, soziale Netze | Infrastruktur-Monitoring |