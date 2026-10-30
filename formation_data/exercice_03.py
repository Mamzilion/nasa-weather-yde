from urllib.request import urlretrieve
from pathlib import Path

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

dossier = Path("datasets")
dossier.mkdir(exist_ok=True)

fichier = dossier / "iris.csv"

urlretrieve(url, fichier)

print("telechargement termine")
print("fichier enregistre ici: ", fichier.resolve())