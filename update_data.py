from datetime import datetime, timedelta
import json
import pandas as pd
import requests

LATITUDE = 3.8480
LONGITUDE = 11.5021


def fetch_nasa_data():
  print("🔄 Extraction des données NASA POWER (Daily & Hourly)...")

  # 1. Données DAILY (depuis 2010)
  url_daily = "https://power.larc.nasa.gov/api/temporal/daily/point"
  params_daily = {
      "parameters": "ALLSKY_SFC_SW_DWN,T2M,T2M_MAX,T2M_MIN",
      "community": "RE",
      "longitude": LONGITUDE,
      "latitude": LATITUDE,
      "start": "20100101",
      "end": datetime.now().strftime("%Y%m%d"),
      "format": "JSON",
  }

  res_daily = requests.get(url_daily, params=params_daily)
  daily_timeseries = []

  if res_daily.status_code == 200:
    params_d = res_daily.json()["properties"]["parameter"]
    df_d = pd.DataFrame(params_d)
    df_d.index = pd.to_datetime(df_d.index, format="%Y%m%d")
    df_d.reset_index(inplace=True)
    df_d.rename(columns={"index": "Date"}, inplace=True)
    df_d["Date"] = df_d["Date"].dt.strftime("%Y-%m-%d")
    df_d = df_d[df_d["ALLSKY_SFC_SW_DWN"] >= 0]
    daily_timeseries = df_d.to_dict(orient="records")

  # 2. Données HOURLY (On prend les 14 derniers jours pour éviter les retards de l'API NASA)
  end_hourly = datetime.now() - timedelta(
      days=3
  )  # Décalage de sécurité NASA
  start_hourly = end_hourly - timedelta(days=10)

  url_hourly = "https://power.larc.nasa.gov/api/temporal/hourly/point"
  params_hourly = {
      "parameters": "ALLSKY_SFC_SW_DWN,T2M",
      "community": "RE",
      "longitude": LONGITUDE,
      "latitude": LATITUDE,
      "start": start_hourly.strftime("%Y%m%d"),
      "end": end_hourly.strftime("%Y%m%d"),
      "format": "JSON",
  }

  res_hourly = requests.get(url_hourly, params=params_hourly)
  hourly_timeseries = []

  if res_hourly.status_code == 200:
    data_h = res_hourly.json()
    params_h = data_h["properties"]["parameter"]
    df_h = pd.DataFrame(params_h)

    df_h.reset_index(inplace=True)
    df_h.rename(columns={df_h.columns[0]: "Timestamp"}, inplace=True)

    df_h["Datetime"] = pd.to_datetime(
        df_h["Timestamp"].astype(str), format="%Y%m%d%H", errors="coerce"
    )
    df_h = df_h.dropna(subset=["Datetime"])
    df_h["Datetime"] = df_h["Datetime"].dt.strftime("%Y-%m-%d %H:00")

    df_h = df_h[df_h["ALLSKY_SFC_SW_DWN"] >= 0]
    df_h = df_h[["Datetime", "ALLSKY_SFC_SW_DWN", "T2M"]]

    hourly_timeseries = df_h.to_dict(orient="records")

  # Structure globale du JSON
  summary = {
      "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
      "location": "Yaoundé, Cameroun",
      "coordinates": {"lat": LATITUDE, "lon": LONGITUDE},
      "daily_timeseries": daily_timeseries,
      "hourly_timeseries": hourly_timeseries,
  }

  output_path = "public/weather_data.json"
  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

  print(
      f"✅ Données générées avec succès ! ({len(daily_timeseries)} jours,"
      f" {len(hourly_timeseries)} heures)"
  )


if __name__ == "__main__":
  fetch_nasa_data()