import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import io
import requests
from weather_api import get_weather, get_location

# Function to display weather data
def display_weather(city=None, lat=None, lon=None):
    try:
        weather_data = get_weather(city, lat, lon)
        
        if 'error' in weather_data:
            messagebox.showerror("Error", weather_data['error']['message'])
            return
        
        condition = weather_data['current']['condition']
        condition_text = condition['text']
        temp_c = weather_data['current']['temp_c']
        temp_f = weather_data['current']['temp_f']
        humidity = weather_data['current']['humidity']
        wind_kph = weather_data['current']['wind_kph']
        wind_mph = weather_data['current']['wind_mph']
        icon_url = f"http:{condition['icon']}"
        
        # Update labels
        weather_condition.config(text=condition_text)
        update_temperature(temp_c, temp_f)
        humidity_label.config(text=f"Humidity: {humidity} %")
        wind_label.config(text=f"Wind Speed: {wind_kph} kph / {wind_mph} mph")
        
        # Update weather icon
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        weather_icon_label.config(image=icon_photo)
        weather_icon_label.image = icon_photo

        # Display weather alerts if any
        if 'alerts' in weather_data and weather_data['alerts']['alert']:
            alert = weather_data['alerts']['alert'][0]
            alert_text = f"Alert: {alert['headline']}\n{alert['desc']}\nInstructions: {alert['instruction']}"
            alert_label.config(text=alert_text)
        else:
            alert_label.config(text="No weather alerts.")

        # Display air quality data
        if 'air_quality' in weather_data['current']:
            air_quality_data = weather_data['current']['air_quality']
            display_air_quality_chart(air_quality_data)
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to display air quality chart
def display_air_quality_chart(air_quality_data):
    pollutants = ['co', 'o3', 'no2', 'so2', 'pm2_5', 'pm10']
    values = [air_quality_data[pollutant] for pollutant in pollutants]
    plt.figure(figsize=(8, 4))
    plt.bar(pollutants, values, color='skyblue')
    plt.title('Air Quality Data')
    plt.xlabel('Pollutants')
    plt.ylabel('Concentration (μg/m³)')

    # Embed the chart in Tkinter
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=50, y=600, width=700, height=300)

# Function to update temperature label based on selected unit
def update_temperature(temp_c, temp_f):
    if unit_var.get() == 'Celsius':
        temperature_label.config(text=f"Temperature: {temp_c} °C")
    else:
        temperature_label.config(text=f"Temperature: {temp_f} °F")

# Function to get weather for the user's current location
def get_weather_for_current_location():
    try:
        location = get_location()
        loc_data = location['loc'].split(',')
        lat, lon = loc_data[0], loc_data[1]
        display_weather(lat=lat, lon=lon)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to get location: {e}")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("800x800")  # Set the window size

# Create and place widgets
tk.Label(root, text="Enter city:").grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

get_weather_button = tk.Button(root, text="Get Weather", command=lambda: display_weather(city=city_entry.get()))
get_weather_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

current_location_button = tk.Button(root, text="Get Weather for Current Location", command=get_weather_for_current_location)
current_location_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

unit_var = tk.StringVar(value="Celsius")
unit_menu = tk.OptionMenu(root, unit_var, "Celsius", "Fahrenheit", command=lambda _: update_temperature(None, None))
unit_menu.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

weather_condition = tk.Label(root, text="")
weather_condition.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

weather_icon_label = tk.Label(root, image=None)
weather_icon_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

temperature_label = tk.Label(root, text="")
temperature_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

humidity_label = tk.Label(root, text="")
humidity_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

wind_label = tk.Label(root, text="")
wind_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

alert_label = tk.Label(root, text="", wraplength=400, justify="left")
alert_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Start the main loop
root.mainloop()
