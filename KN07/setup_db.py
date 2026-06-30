import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="recipes")

documents = [
    "Spaghetti Carbonara mit knusprigem Speck, Ei und Parmesan.",
    "Frischer Sommer-Salat mit Wassermelone, Feta-Käse und Minze.",
    "Herzhaftes Rindsgulasch, langsam geschmort mit Paprika und Zwiebeln.",
    "Veganes Curry mit Kichererbsen, Kokosmilch und frischem Koriander."
]
ids = ["rec_1", "rec_2", "rec_3", "rec_4"]

collection.add(documents=documents, ids=ids)

print("Rezepte wurden erfolgreich vektorisiert und gespeichert!")
