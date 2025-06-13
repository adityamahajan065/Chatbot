import wikipedia
import datetime
import random
import webbrowser
import platform
import os
import requests
from textblob import TextBlob

class WikiBot:
    def __init__(self, name="SmartBot"):
        self.name = name
        self.serpapi_key = "YOUR_SERPAPI_KEY"  # Replace with your actual SerpAPI key
        self.weather_api_key = "c02f628f0feaf1227fe1e64b17dbc36c"  # Replace with your OpenWeatherMap API key
        self.greetings = [
            "Hello! I’m SmartBot. Ask me anything!",
            "Hi there! Ready to learn something new?",
            "Hey! I'm your assistant. What can I do for you today?"
        ]

    def help(self):
        return (
            "🤖 SmartBot Help:\n"
            "- Ask about any topic to get info from Wikipedia.\n"
            "- Ask weather in format: 'weather in [city]'\n"
            "- 'time': Show current time.\n"
            "- 'date': Show current date.\n"
            "- 'open [website]': Open a site (e.g., youtube).\n"
            "- 'search [query]': Open Google search.\n"
            "- 'os': Show system info.\n"
            "- 'exit': End the chat.\n"
        )

    def get_summary(self, query):
        try:
            return wikipedia.summary(query, sentences=3)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"'{query}' is too broad. Try one of these: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return self.google_fallback(query)
        except Exception:
            return self.google_fallback(query)

    def google_fallback(self, query):
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "engine": "google",
                "num": 1
            }
            res = requests.get(url, params=params)
            data = res.json()

            answer_box = data.get("answer_box")
            if answer_box:
                return answer_box.get("answer") or answer_box.get("snippet") or answer_box.get("content", "")

            results = data.get("organic_results", [])
            if results and "snippet" in results[0]:
                return results[0]["snippet"]

            return "Sorry, I couldn't find an answer on Google either."
        except Exception as e:
            return f"Google search failed: {str(e)}"

    def get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": self.weather_api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            data = response.json()

            if data["cod"] != 200:
                return f"Weather not found for '{city}'."

            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]

            return (
                f"🌤 Weather in {city.capitalize()}:\n"
                f"- {weather}\n"
                f"- Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                f"- Humidity: {humidity}%"
            )
        except Exception as e:
            return f"Failed to fetch weather: {str(e)}"

    def get_time(self):
        now = datetime.datetime.now()
        return f"🕒 Current time: {now.strftime('%H:%M:%S')}"

    def get_date(self):
        today = datetime.date.today()
        return f"📅 Today's date: {today.strftime('%Y-%m-%d')}"

    def open_website(self, site):
        urls = {
            'youtube': 'https://www.youtube.com',
            'google': 'https://www.google.com',
            'github': 'https://www.github.com'
        }
        site = site.lower()
        if site in urls:
            webbrowser.open(urls[site])
            return f"🔗 Opening {site}..."
        else:
            return f"I don't have a shortcut for '{site}'."

    def search_google(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"🔍 Searching Google for '{query}'..."

    def os_info(self):
        info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor()
        }
        return "🖥 OS Info:\n" + "\n".join([f"{k}: {v}" for k, v in info.items()])

    def handle_input(self, user_input):
        user_input = user_input.strip().lower()
        known_greetings = ["hello", "hi", "hey"]

        if user_input in known_greetings:
            return random.choice(self.greetings)
        elif user_input == "exit":
            return "👋 Goodbye!"
        elif user_input == "help":
            return self.help()
        elif user_input == "time":
            return self.get_time()
        elif user_input == "date":
            return self.get_date()
        elif user_input == "os":
            return self.os_info()
        elif user_input.startswith("open "):
            site = user_input[5:].strip()
            return self.open_website(site)
        elif user_input.startswith("search "):
            query = user_input[7:].strip()
            return self.search_google(query)
        elif user_input.startswith("weather in "):
            city = user_input.replace("weather in ", "").strip()
            return self.get_weather(city)
        elif user_input == "":
            return "⚠️ Please type something."
        else:
            corrected_input = str(TextBlob(user_input).correct())
            return self.get_summary(corrected_input)
