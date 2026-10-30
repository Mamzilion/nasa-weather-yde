import pandas as pd
data = {
    "Produit":["Ordinateur", "Telephone", "Tablette", "Ordinateur", "Telephone"],
    "Ville": ["Yaounde", "Douala", "Bafoussam", "Douala", "Yaounde"],
    "Prix": [350000, 120000, 150000, 350000, 120000],
    "Quantite": [2, 5, 3, 1, 4]
}

df = pd.DataFrame(data)
df["Chiffre_Affaires"] = df["Prix"]*df["Quantite"]
print(df)