# KN 07 – Antworten
## Szenario E: Rezept-Finder (Zutaten & Geschmack)

---

## Phase 1: Setup & Das Embedding-Wunder

**Frage: Was passiert im Hintergrund, wenn ChromaDB den Text in die Datenbank speichert? Was ist ein Embedding-Modell?**

Wenn `collection.add()` aufgerufen wird, schickt ChromaDB jeden Text automatisch an ein lokal geladenes Embedding-Modell (standardmässig ein kleines Sentence-Transformer-Modell). Dieses Modell wandelt den Text nicht einfach in Buchstaben um, sondern berechnet einen mehrdimensionalen Zahlen-Vektor (z. B. 384 Dimensionen), der die *Bedeutung* des Textes repräsentiert. Texte mit ähnlichem Sinn landen dabei nahe beieinander im Vektorraum, auch wenn sie unterschiedliche Wörter verwenden. Genau dieser Vektor – nicht der reine Text – wird zusammen mit dem Originaltext in der Datenbank abgelegt und später für Ähnlichkeitsvergleiche genutzt.

**Screenshot:** *(hier den eigenen Terminal-Screenshot nach erfolgreichem Ausführen von `setup_db.py` einfügen)*

---

## Phase 2: Die fehlerhafte KI-Abfrage

**Frage: Warum hat die ursprüngliche `get(where=...)`-Abfrage keine Resultate geliefert, obwohl der Inhalt sinngemäss in der Datenbank existiert?**

`get(where={...})` ist eine rein lexikalische Abfrage auf Metadaten-Felder – sie funktioniert wie ein `WHERE`-Filter in SQL und verlangt einen exakten String-Match. In unserem Fall existiert aber gar kein Metadatenfeld namens `"text"`; die Rezepttexte wurden beim `add()` als `documents` gespeichert, nicht als Metadaten. Selbst wenn es ein solches Feld gäbe, müsste der gesamte Suchsatz Zeichen für Zeichen mit einem gespeicherten Wert übereinstimmen. Da die Suchanfrage ("Etwas Leichtes und Erfrischendes für heisse Tage") nirgendwo wortwörtlich in der Datenbank steht, kann `get()` nichts finden – obwohl inhaltlich ein perfekt passendes Rezept (der Sommer-Salat) vorhanden ist.

**Korrigierter Code:** siehe `search_db.py`

**Screenshot:** *(hier den eigenen Terminal-Screenshot mit den korrekten Treffern einfügen)*

---

## Phase 3: Architektur-Reflexion

**Frage: Warum können Vektordatenbanken erkennen, dass "Hund" und "Welpe" extrem ähnlich sind, während `WHERE text LIKE '%Hund%'` den Welpen nie finden würde?**

Eine SQL-Datenbank vergleicht nur Zeichenketten: `LIKE '%Hund%'` prüft, ob die exakte Buchstabenfolge "Hund" im Text vorkommt. "Welpe" enthält diese Buchstabenfolge nicht, also liefert SQL kein Ergebnis – unabhängig davon, dass beide Wörter inhaltlich eng verwandt sind. Eine Vektordatenbank hingegen vergleicht keine Buchstaben, sondern die Position der Wörter im hochdimensionalen Vektorraum. Da das Embedding-Modell beim Training gelernt hat, dass "Hund" und "Welpe" in ähnlichen sprachlichen Kontexten auftreten, liegen ihre Vektoren im Raum sehr nahe beieinander (kleine euklidische bzw. Kosinus-Distanz). Die Vektordatenbank sucht also nicht nach exakten Wörtern, sondern nach den Einträgen mit der geringsten Distanz zum Such-Vektor – und findet dadurch auch semantisch verwandte, aber wörtlich unterschiedliche Begriffe.

**Frage: Metadaten vs. Vektoren – warum ist es oft nötig, semantische Suche (`query`) mit einem Metadaten-Filter (`where`) zu kombinieren? Beispiel.**

Semantische Suche findet sehr gut *inhaltlich passende* Ergebnisse, kann aber harte Geschäftsregeln oder eindeutige Kategorien nicht zuverlässig abbilden, da sie auf Ähnlichkeit statt auf exakten Kriterien basiert. Ein rein semantisch passendes Resultat kann z. B. trotzdem die falsche Kategorie, das falsche Jahr oder eine ungewünschte Eigenschaft haben. Deshalb kombiniert man in der Praxis beide Ansätze: `query` liefert die inhaltlich relevantesten Treffer, `where` schränkt diese zusätzlich auf exakte, strukturierte Kriterien ein.

*Beispiel für den Rezept-Finder:* Ein Nutzer sucht semantisch nach "etwas Schnelles und Herzhaftes", möchte aber nur **vegane** Rezepte sehen. Dazu könnte man beim Speichern Metadaten wie `{"vegan": True}` mitgeben und die Abfrage so kombinieren:

```python
resultate = collection.query(
    query_texts=["etwas Schnelles und Herzhaftes"],
    n_results=3,
    where={"vegan": True}
)
```

So liefert ChromaDB nur Rezepte, die sowohl semantisch passen als auch die exakte Bedingung `vegan = True` erfüllen.
