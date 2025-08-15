import requests
from datetime import date, timedelta

def weather_openmeteo(lat, lon):
    today = date.today()
    start = today - timedelta(days=30)

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max"
        f"&start_date={start}&end_date={today + timedelta(days=7)}"  # past 30 days + 7 days forecast
        f"&timezone=auto"
    )
    r = requests.get(url)
    data = r.json()

    if "daily" not in data:
        return f"Error from Open-Meteo API: {data}"

    daily = data["daily"]

    # Today's weather
    today_temp_max = daily["temperature_2m_max"][-8]  # today in the list
    today_temp_min = daily["temperature_2m_min"][-8]
    today_precip = daily["precipitation_sum"][-8]
    today_wind = daily["windspeed_10m_max"][-8]

    # Last 30 days rainfall
    last_30_rain = daily["precipitation_sum"][:30]
    last_30_sum = sum(last_30_rain)
    last_10_avg = sum(last_30_rain[-10:]) / 10

    # Forecast summary (next 7 days)
    forecast_lines = []
    for i in range(-7, 0):
        date_str = daily["time"][i]
        tmax = daily["temperature_2m_max"][i]
        tmin = daily["temperature_2m_min"][i]
        rain = daily["precipitation_sum"][i]
        wind = daily["windspeed_10m_max"][i]
        forecast_lines.append(f"{date_str}: {tmin}–{tmax}°C, {rain} mm rain, wind {wind} km/h")

    return (
        f"Weather Report for ({lat}, {lon}):\n"
        f"- Today's temp: {today_temp_min}–{today_temp_max}°C, Rain: {today_precip} mm, Wind: {today_wind} km/h\n"
        f"- Last 10 days avg rainfall: {last_10_avg:.2f} mm/day\n"
        f"- Last 1 month total rainfall: {last_30_sum:.2f} mm\n"
        f"- 7-day Forecast:\n" + "\n".join(forecast_lines)
    )