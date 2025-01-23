from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Route for the home page (weather input form)
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")

        # Check if city is provided
        if not city:
            error_message = "Please enter a city name."
            return render_template("index.html", weather_data=weather_data, error_message=error_message)

        api_key = os.getenv("weather_api_key")

        # Check if API key is set in the environment variables
        if not api_key:
            error_message = "Error! The API key is not found. Please set it in the environment variable."
            return render_template("index.html", weather_data=weather_data, error_message=error_message)

        # Prepare API request URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)

        # Handle API response
        if response.status_code != 200:
            error_message = f"Error! Failed to retrieve data for {city}. Response code: {response.status_code}"
        else:
            data = response.json()

            # Extracting data from the API response
            city_name = data["name"]
            country = data["sys"]["country"]
            weather_description = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]

            # Temperature and other details
            temp = data["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
            temp_min = data["main"]["temp_min"] - 273.15
            temp_max = data["main"]["temp_max"] - 273.15
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            visibility = data.get("visibility", 0) / 1000  # Convert to km if available
            wind_speed = data["wind"]["speed"]
            wind_deg = data["wind"]["deg"]

            # Assemble the weather data into a dictionary
            weather_data = {
                "city": city_name,
                "country": country,
                "description": weather_description,
                "icon": icon_code,
                "temperature": round(temp, 2),
                "temperature_min": round(temp_min, 2),
                "temperature_max": round(temp_max, 2),
                "humidity": humidity,
                "pressure": pressure,
                "visibility": visibility,
                "wind_speed": wind_speed,
                "wind_deg": wind_deg
            }

    return render_template("index.html", weather_data=weather_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
