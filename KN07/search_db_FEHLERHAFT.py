import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_collection(name="recipes")

suchanfrage = "Etwas Leichtes und Erfrischendes für heisse Tage"
print(f"Suche nach Rezepten für: '{suchanfrage}'...")

# FEHLERHAFTER KI-CODE: Sucht nach exaktem Metadaten-Match (wie SQL)
resultate = collection.get(
    where={"text": suchanfrage}
)

print("Gefundene Rezepte:", resultate["documents"])
