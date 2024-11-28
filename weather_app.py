import tkinter as tk
from PIL import Image, ImageTk
import requests
from datetime import datetime
from io import BytesIO
import traceback

class GlassFrame(tk.Frame):
    def __init__(self, parent, alpha=0.2, corner_radius=10, **kwargs):
        bg_color = kwargs.pop('bg', '#ffffff')
        kwargs['bg'] = self._adjust_color(bg_color, alpha)
        super().__init__(parent, **kwargs)
        
    def _adjust_color(self, color, alpha):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = int(r + (255 - r) * alpha)
        g = int(g + (255 - g) * alpha)
        b = int(b + (255 - b) * alpha)
        return f'#{r:02x}{g:02x}{b:02x}'

class ModernButton(tk.Button):
    def __init__(self, *args, **kwargs):
        self.hover_bg = kwargs.pop('hover_background', '#2563eb')
        self.normal_bg = kwargs.get('bg', '#3b82f6')
        super().__init__(*args, **kwargs)
        self.config(
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.config(bg=self.normal_bg)

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("900x700")
        
        # Modern dark theme colors
        self.bg_color = "#0f172a"  # Dark blue background
        self.card_bg = "#1e293b"   # Slightly lighter blue for cards
        self.accent_color = "#3b82f6"  # Bright blue
        self.text_color = "#f1f5f9"    # Light grey text
        self.secondary_text = "#94a3b8"  # Muted text
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        self.root.option_add("*Font", "Helvetica 10")
        
        self.api_key = "01000328394b93954c2042cd3b4c0503"
        self.weather_icons = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with reduced padding
        main_container = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=15)
        main_container.pack(fill="both", expand=True)
        
        # Header section with minimal height
        header = GlassFrame(main_container, alpha=0.1, bg=self.card_bg, padx=15, pady=10)
        header.pack(fill="x", pady=(0, 10))
        
        # Compact title and search section
        title = tk.Label(
            header,
            text="Weather Dashboard",
            font=("Helvetica", 20, "bold"),
            bg=header['bg'],
            fg=self.text_color
        )
        title.pack(pady=(0, 8))
        
        # Search container with minimal height
        search_frame = tk.Frame(header, bg=header['bg'])
        search_frame.pack(fill="x")
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Helvetica", 12),
            bg=self.card_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            width=40
        )
        self.search_entry.pack(side="left", padx=(0, 10), ipady=6)
        self.search_entry.bind("<Return>", lambda e: self.fetch_weather())
        
        search_button = ModernButton(
            search_frame,
            text="Search",
            font=("Helvetica", 11, "bold"),
            bg=self.accent_color,
            fg=self.text_color,
            command=self.fetch_weather
        )
        search_button.pack(side="left")
        
        # Current weather section with reduced height
        current_weather = GlassFrame(
            main_container,
            alpha=0.15,
            bg=self.card_bg,
            padx=20,
            pady=15
        )
        current_weather.pack(fill="x", padx=0, pady=(0, 10))
        
        # Current weather info in horizontal layout
        current_info = tk.Frame(current_weather, bg=current_weather['bg'])
        current_info.pack(fill="x", expand=True)
        
        # Left side - Location and description
        left_info = tk.Frame(current_info, bg=current_weather['bg'])
        left_info.pack(side="left", padx=20)
        
        self.location_label = tk.Label(
            left_info,
            text="",
            font=("Helvetica", 18, "bold"),
            bg=current_weather['bg'],
            fg=self.text_color
        )
        self.location_label.pack(anchor="w")
        
        self.desc_label = tk.Label(
            left_info,
            text="",
            font=("Helvetica", 14),
            bg=current_weather['bg'],
            fg=self.text_color
        )
        self.desc_label.pack(anchor="w", pady=(5, 0))
        
        # Center - Temperature and icon
        center_info = tk.Frame(current_info, bg=current_weather['bg'])
        center_info.pack(side="left", expand=True)
        
        temp_icon_frame = tk.Frame(center_info, bg=current_weather['bg'])
        temp_icon_frame.pack()
        
        self.weather_icon_label = tk.Label(
            temp_icon_frame,
            bg=current_weather['bg']
        )
        self.weather_icon_label.pack(side="left", padx=10)
        
        self.temp_label = tk.Label(
            temp_icon_frame,
            text="",
            font=("Helvetica", 32, "bold"),
            bg=current_weather['bg'],
            fg=self.accent_color
        )
        self.temp_label.pack(side="left")
        
        # Right side - Humidity and wind
        right_info = tk.Frame(current_info, bg=current_weather['bg'])
        right_info.pack(side="right", padx=20)
        
        self.humidity_label = tk.Label(
            right_info,
            text="",
            font=("Helvetica", 12),
            bg=current_weather['bg'],
            fg=self.secondary_text
        )
        self.humidity_label.pack(anchor="e")
        
        self.wind_label = tk.Label(
            right_info,
            text="",
            font=("Helvetica", 12),
            bg=current_weather['bg'],
            fg=self.secondary_text
        )
        self.wind_label.pack(anchor="e", pady=(5, 0))
        
        # Forecast section
        forecast_label = tk.Label(
            main_container,
            text="5-Day Forecast",
            font=("Helvetica", 20, "bold"),
            bg=main_container['bg'],
            fg=self.text_color
        )
        forecast_label.pack(pady=(10, 15), padx=20, anchor="w")
        
        # Forecast container
        self.forecast_frame = tk.Frame(main_container, bg=main_container['bg'])
        self.forecast_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Create forecast cards
        self.forecast_days = []
        for _ in range(5):
            card_container = tk.Frame(self.forecast_frame, bg=self.forecast_frame['bg'], padx=8)
            card_container.pack(side="left", expand=True, fill="both")
            
            day_frame = GlassFrame(
                card_container,
                alpha=0.15,
                bg=self.card_bg,
                padx=20,
                pady=25
            )
            day_frame.pack(expand=True, fill="both")
            
            date_label = tk.Label(
                day_frame,
                text="",
                font=("Helvetica", 16, "bold"),
                bg=day_frame['bg'],
                fg=self.text_color
            )
            date_label.pack(pady=(0, 10))
            
            icon_label = tk.Label(day_frame, bg=day_frame['bg'])
            icon_label.pack(pady=15)
            
            temp_label = tk.Label(
                day_frame,
                text="",
                font=("Helvetica", 24, "bold"),
                bg=day_frame['bg'],
                fg=self.accent_color
            )
            temp_label.pack(pady=(5, 10))
            
            desc_label = tk.Label(
                day_frame,
                text="",
                font=("Helvetica", 13),
                bg=day_frame['bg'],
                fg=self.secondary_text,
                wraplength=130
            )
            desc_label.pack(pady=(0, 5))
            
            self.forecast_days.append({
                "frame": day_frame,
                "date_label": date_label,
                "icon_label": icon_label,
                "temp_label": temp_label,
                "desc_label": desc_label
            })
    
    def fetch_weather(self):
        city = self.search_entry.get()
        if not city:
            return
            
        try:
            # Get current weather
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(current_url)
            current_data = response.json()
            
            if response.status_code == 200:
                # Get forecast data
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric"
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()
                
                if forecast_response.status_code == 200:
                    self.update_current_weather(current_data)
                    self.update_forecast(forecast_data)
        except Exception as e:
            print(f"Error fetching weather: {str(e)}")
    
    def update_current_weather(self, data):
        try:
            city = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            icon_code = data["weather"][0]["icon"]
            
            # Update labels
            self.location_label.config(text=f"{city}, {country}")
            self.temp_label.config(text=f"{temp:.1f}°C")
            self.desc_label.config(text=desc)
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.wind_label.config(text=f"Wind: {wind_speed} m/s")
            
            # Update weather icon
            if icon_code not in self.weather_icons:
                icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
                response = requests.get(icon_url)
                img = Image.open(BytesIO(response.content))
                photo = ImageTk.PhotoImage(img)
                self.weather_icons[icon_code] = photo
            
            self.weather_icon_label.config(image=self.weather_icons[icon_code])
            
        except Exception as e:
            print(f"Error updating current weather: {str(e)}")
    
    def update_forecast(self, data):
        try:
            # Get unique dates from the forecast data
            forecasts = {}
            current_date = datetime.now().date()
            
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                
                # Skip current date and only take next 5 days
                if date <= current_date:
                    continue
                    
                if date not in forecasts and len(forecasts) < 5:
                    forecasts[date] = {
                        'temp': item['main']['temp'],
                        'icon': item['weather'][0]['icon'],
                        'description': item['weather'][0]['description'],
                        'date': date
                    }
            
            # Sort forecasts by date
            sorted_forecasts = sorted(forecasts.items(), key=lambda x: x[0])
            
            # Update forecast cards
            for i, (date, forecast) in enumerate(sorted_forecasts):
                if i < len(self.forecast_days):
                    day_frame = self.forecast_days[i]
                    
                    # Get day name
                    day_name = date.strftime('%A')
                    
                    # Update labels with forecast data
                    day_frame['date_label'].config(
                        text=f"{day_name}\n{date.strftime('%b %d')}"
                    )
                    
                    # Load and display weather icon
                    icon_code = forecast['icon']
                    if icon_code not in self.weather_icons:
                        icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
                        response = requests.get(icon_url)
                        img = Image.open(BytesIO(response.content))
                        photo = ImageTk.PhotoImage(img)
                        self.weather_icons[icon_code] = photo
                    
                    day_frame['icon_label'].config(image=self.weather_icons[icon_code])
                    day_frame['temp_label'].config(text=f"{forecast['temp']:.1f}°C")
                    day_frame['desc_label'].config(text=forecast['description'].capitalize())
            
            # Clear any unused forecast cards
            for i in range(len(sorted_forecasts), len(self.forecast_days)):
                day_frame = self.forecast_days[i]
                day_frame['date_label'].config(text="")
                day_frame['icon_label'].config(image="")
                day_frame['temp_label'].config(text="")
                day_frame['desc_label'].config(text="")
                
        except Exception as e:
            print(f"Error updating forecast: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()
