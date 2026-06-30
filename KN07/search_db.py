import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_collection(name="recipes")

suchanfrage = "Etwas Leichtes und Erfrischendes für heisse Tage"
print(f"Suche nach Rezepten für: '{suchanfrage}'...")

# KORREKTUR: Semantische Suche mit query() statt get()
# query() wandelt die Suchanfrage in einen Vektor um und vergleicht
# diesen per Distanzmass mit den gespeicherten Embeddings aller Rezepte.
resultate = collection.query(
    query_texts=[suchanfrage],
    n_results=2
)

print("Gefundene Rezepte:", resultate["documents"])
