import requests
import pandas as pd

url= (
    "https://api.worldbank.org/v2/country/CMR/indicator/"
    "NY.GDP.MKTP.KD.ZG"
)

params = {
    "format": "json",
    "per_page": 100
}

response = requests.get(url, params=params, timeout=30)

response.raise_for_status()
data = response.json()
if len(data) < 2 or data[1] is None:
    print("Aucune observation disponible")
else:
    df = pd.DataFrame([
        {
            
            "annee": int(item["date"]),
            "croissance_pib": item["value"] 
        }
        for item in data[1]
        if item["value"] is not None
    ])
    
    df = df.sort_values("annee").reset_index(drop=True)
    
    print("\nPremiere observations : ")
    print(df.head())
    
    print("\nDerniere observations : ")
    print(df.tail())
    
    print("\ninformations sur le jeu de donnee :")
    print(df.info())