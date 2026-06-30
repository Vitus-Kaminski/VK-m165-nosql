# KN 07 – Vektordatenbanken & Semantische Suche mit ChromaDB
## Szenario E: Rezept-Finder

## Inhalt dieses Ordners
- `setup_db.py` – Phase 1: erstellt die ChromaDB-Datenbank und befüllt sie mit 4 Rezepten
- `search_db_FEHLERHAFT.py` – Phase 2: der ursprüngliche, fehlerhafte Code des Junior-Entwicklers (zum Vergleich)
- `search_db.py` – Phase 2: der korrigierte Code mit semantischer Suche (`query()`)
- `Antworten.md` – alle schriftlichen Antworten zu Phase 1–3 (Screenshots noch selbst einfügen!)
- `requirements.txt` – benötigtes Python-Paket

## Setup-Anleitung

1. Terminal im entpackten Ordner öffnen.
2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
   *(Beim ersten Start lädt ChromaDB automatisch ein Embedding-Modell herunter – das kann 1–2 Minuten dauern.)*
4. Datenbank befüllen:
   ```bash
   python setup_db.py
   ```
   → Screenshot der Ausgabe für die Abgabe machen.
5. Fehlerhafte Suche testen (liefert bewusst kein Ergebnis):
   ```bash
   python search_db_FEHLERHAFT.py
   ```
6. Korrigierte, semantische Suche ausführen:
   ```bash
   python search_db.py
   ```
   → Screenshot der Ausgabe (mit Treffern) für die Abgabe machen.

## Wichtiger Hinweis
Die Screenshots der Terminal-Ausgaben müssen noch selbst erstellt und in die Abgabe (z. B. in `Antworten.md` oder ein separates Dokument) eingefügt werden, da diese erst beim eigenen Ausführen auf dem eigenen Rechner entstehen.
