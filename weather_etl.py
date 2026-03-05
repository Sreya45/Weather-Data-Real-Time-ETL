import requests
import json
import csv
import psycopg2

CITY = "Calicut"
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=11.2588&longitude=75.7804&current_weather=true"


def extract_weather_data():
    print("Extracting weather data from API...")
    response = requests.get(API_URL)
    data = response.json()

    with open("raw_weather_data.json", "w") as file:
        json.dump(data, file, indent=4)

    return data


def transform_weather_data(data):
    print("Transforming weather data...")

    current = data["current_weather"]

    transformed_data = {
        "city": CITY,
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "winddirection": current["winddirection"],
        "time": current["time"]
    }

    with open("cleaned_weather_data.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=transformed_data.keys())
        writer.writeheader()
        writer.writerow(transformed_data)

    return transformed_data


def load_weather_data(data):
    print("Loading data into PostgreSQL...")

    connection = psycopg2.connect(
        database="weather_pipeline_db",
        user="sreyavijay",
        host="localhost",
        port="5432"
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO weather_data (city, temperature, windspeed, winddirection, recorded_at)
    VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(insert_query, (
        data["city"],
        data["temperature"],
        data["windspeed"],
        data["winddirection"],
        data["time"]
    ))

    connection.commit()
    cursor.close()
    connection.close()

    print("Data successfully inserted into database!")


if __name__ == "__main__":
    raw_data = extract_weather_data()
    cleaned_data = transform_weather_data(raw_data)
    load_weather_data(cleaned_data)