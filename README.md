# Weather Data Real-Time ETL Pipeline

## Project Overview
This project implements a simple **ETL (Extract, Transform, Load) pipeline** that collects real-time weather data from an external API, processes it, and stores it in a PostgreSQL database.

The goal of this project is to demonstrate core **data engineering concepts** such as:
- API data ingestion
- Data transformation
- Database loading
- Basic pipeline automation

---

## Architecture

Weather API  
↓  
Python ETL Script  
↓  
Data Transformation  
↓  
PostgreSQL Database  

---

## Tech Stack

- Python
- Requests (API calls)
- PostgreSQL
- psycopg2 (PostgreSQL connector)
- Git
- GitHub

---

## Project Structure

```
weather-data-pipeline
│
├── weather_etl.py              # Main ETL pipeline script
├── raw_weather_data.json       # Raw API data
├── cleaned_weather_data.csv    # Processed data
├── README.md                   # Project documentation
└── .gitignore                  # Ignored files
```

---

## Features

- Extracts real-time weather data from **Open-Meteo API**
- Transforms JSON data into structured format
- Stores cleaned data into a **PostgreSQL database**
- Maintains historical weather records

---

## How the Pipeline Works

### 1️⃣ Extract
The pipeline fetches live weather data from the **Open-Meteo Weather API**.

### 2️⃣ Transform
The JSON response is processed and converted into structured data including:
- City
- Temperature
- Wind speed
- Wind direction
- Timestamp

### 3️⃣ Load
The transformed data is inserted into a **PostgreSQL database table** for storage and analysis.

---

## How to Run the Project

### 1. Clone the repository

```
git clone https://github.com/Sreya45/Weather-Data-Real-Time-ETL.git
```

### 2. Navigate to the project

```
cd Weather-Data-Real-Time-ETL
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the ETL pipeline

```
python weather_etl.py
```

---

## Example Output

After running the pipeline, the weather data will be stored in PostgreSQL like this:

| id | city | temperature | windspeed | winddirection | recorded_at |
|----|------|-------------|-----------|---------------|-------------|

---

## Future Improvements

- Add **data visualization dashboard**
- Automate pipeline scheduling
- Containerize the pipeline using **Docker**
- Use **Apache Airflow for orchestration**

---

## Author

Sreya Vijay  
