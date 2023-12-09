import random
import requests
from bs4 import BeautifulSoup
import pywhatkit
import speech_recognition as sr
import pyttsx3
import mysql.connector
from decouple import config
import datetime
import time
from datetime import datetime
import subprocess as sp
import wikipedia
import webbrowser
import wolframalpha
import subprocess
import pyjokes
import threading
import json
import sys

# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Constants
opening_text = [
    "Cool, I'm on it, sir.",
    "Okay, sir, I'm working on it.",
    "Just a second, sir."
]

user_id = 1

# Database configuration
config = {
    'host': 'db4free.net',
    'port': 3306,
    'user': 'aguilarpogi123',
    'password': 'aguilarpogi123',
    'database': 'capstone2324',
    'connect_timeout': 30,
    'auth_plugin': 'mysql_native_password'
}
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language="en-US")
        return command.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

stop_speaking = False
engine = pyttsx3.init()
speak_lock = threading.Lock()

def speak(message):
    print("Aki:", message)
    global stop_speaking
    if not stop_speaking:
        with speak_lock:
            engine.say(message)
            engine.runAndWait()

def stop_talking():
    global stop_speaking
    stop_speaking = True

def get_username():
    username = ""
    try:
        # Database connection
        conn = mysql.connector.connect(
            host="db4free.net",
            port=3306,
            user="aguilarpogi123",
            password="aguilarpogi123",
            database="capstone2324",
            connect_timeout=30,  # Reduce the timeout value to 30 seconds
            auth_plugin='mysql_native_password'
        )

        if conn.is_connected():
            speak("Aki is now Online!")

        # Create a cursor object
        cursor = conn.cursor()
        sql = "SELECT username FROM users WHERE id = 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            username = result[0]

        # Closing the cursor and connection
        cursor.close()
        conn.close()
        print("Aki's listening...")

    except mysql.connector.Error as error:
        print("Error retrieving username:", error)

    return username


workouts = {
    'Monday': {
        'Cardio Warm up': 60,
        'Cardio Main workout': 60,
        'Cardio Cool down': 60
    },
    'Tuesday': {
        'Lower body Warm up': 60,
        'Lower body Squats': 30,
        'Lower body Lunges': 30,
        'Lower body Glute bridges': 30
    },
    'Wednesday': {
        'Upper body and core Warm up': 60,
        'Upper body and core Push-ups': 30,
        'Upper body and core Plank': 30
    },
    'Thursday': {},
    'Friday': {
        'Lower body with a focus on glutes Warm up': 60,
        'Lower body with a focus on glutes Squats': 30,
        'Lower body with a focus on glutes Glute bridges': 30
    },
    'Saturday': {
        'Upper body Warm up': 60,
        'Upper body Push-ups': 30,
        'Upper body Dumbbell rows': 30
    },
    'Sunday': {}
}

workout_days = ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday"]
non_workout_days = ["Thursday", "Sunday"]

# Define the meal options and their respective calorie counts
meal_options = {
    "Breakfast": [
        "Oatmeal with berries and nuts",
        "Whole-wheat toast with avocado and egg",
        "Yogurt with fruit and granola"
    ],
    "Lunch": [
        "Salad with grilled chicken or fish",
        "Soup or chili",
        "Sandwich on whole-wheat bread"
    ],
    "Dinner": [
        "Grilled salmon with roasted vegetables",
        "Chicken stir-fry with brown rice",
        "Lentil soup"
    ],
    "Snacks": [
        "Fruit",
        "Yogurt",
        "Trail mix"
    ]
}

calorie_counts = {
    "Oatmeal with berries and nuts": 300,
    "Whole-wheat toast with avocado and egg": 250,
    "Yogurt with fruit and granola": 200,
    "Salad with grilled chicken or fish": 300,
    "Soup or chili": 250,
    "Sandwich on whole-wheat bread": 200,
    "Grilled salmon with roasted vegetables": 400,
    "Chicken stir-fry with brown rice": 350,
    "Lentil soup": 300,
    "Fruit": 100,
    "Yogurt": 150,
    "Trail mix": 150
}

def get_workout_instructions(day):
    if day in workout_days:
        workout = workouts[day]
        instructions = f"On {day}, your workout consists of: "
        for exercise, duration in workout.items():
            instructions += f"{exercise} for {duration} seconds, "
        return instructions
    elif day in non_workout_days:
        return "Rest day. Take a break and relax."
        play_workout_video()
    else:
        return "Invalid day. Please provide a valid day."

def relax():
    speak("Playing relaxing music")
    pywhatkit.playonyt("heavy metal live")

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
def news():
    speak("Here are the latest news headlines:")
    url = 'https://news.google.com/rss'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        news_items = soup.findAll('item')[:5]

        for item in news_items:
            title = item.title.text
            speak(title)
    except requests.exceptions.RequestException:
        speak("Sorry, I couldn't fetch the news at the moment.")

def current_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"Sir, the current time is {current_time}.")

def system_command(command):
    if "shutdown" in command:
        speak("Shutting down the system")
        sp.call('shutdown /s /t 0', shell=True)
    elif "restart" in command:
        speak("Restarting the system")
        sp.call('shutdown /r /t 0', shell=True)
    elif "sleep" in command:
        speak("Putting the system to sleep")
        sp.call('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True)

def get_motivation():
    motivations = [
        "You're doing great! Keep pushing yourself!",
        "Don't give up! You're almost there!",
        "Remember, every step counts towards your goal!",
        "Believe in yourself and your abilities. You've got this!"

    ]
    return random.choice(motivations)

def greet_user():
    current_time = datetime.now()
    hour = current_time.hour
    if 5 <= hour < 12:
        speak(f"Good morning {get_username()}!")
        speak("It's " + current_time.strftime("%I:%M %p"))
        speak("how can I assist you to your Workout today?")
    elif 12 <= hour < 18:
        speak(f"Good afternoon {get_username()}!")
        speak("It's " + current_time.strftime("%I:%M %p"))
        speak("how can I assist you to your Workout today?")
    else:
        speak(f"Good evening {get_username()}!")
        speak("I am aki zero point one at your service")
        speak("The current time is " + current_time.strftime("%I:%M %p"))
        speak("how can I assist you to your Workout today?")

def calculate(command):
    app_id = "T6AGJ3-EVVE74PR9T"
    client = wolframalpha.Client(app_id)
    index = command.lower().split().index('calculate')
    command = command.split()[index + 1:]
    res = client.query(' '.join(command))
    answer = next(res.results).text
    print("The answer is " + answer)
    speak("The answer is " + answer)

def set_alarm():
    speak("Sure, please provide the alarm time.")
    alarm_time = listen().lower()  # Listen for the alarm time input
    # Extract the hour and minute from the input
    hour = None
    minute = None
    # Check if hour is specified in the input
    if "hour" in alarm_time:
        try:
            hour = int(alarm_time.split("hour")[0].strip())
            alarm_time = alarm_time.split("hour")[1]
        except ValueError:
            print("I'm sorry, I couldn't understand the hour. Please try again.")
            return

    # Check if minute is specified in the input
    if "minute" in alarm_time:
        try:
            minute = int(alarm_time.split("minute")[0].strip())
            alarm_time = alarm_time.split("minute")[1]
        except ValueError:
            print("I'm sorry, I couldn't understand the minute. Please try again.")
            return

    # Convert hour and minute to 24-hour format
    if "am" in alarm_time:
        if hour == 12:
            hour = 0
        alarm_time = alarm_time.replace("am", "").strip()
    elif "pm" in alarm_time:
        if hour != 12:
            hour += 12
        alarm_time = alarm_time.replace("pm", "").strip()
    # Convert the hour and minute to strings with leading zeros if necessary
    hour_str = str(hour).zfill(2) if hour is not None else None
    minute_str = str(minute).zfill(2) if minute is not None else None

    # Set the alarm time based on the provided inputs
    if hour_str is not None and minute_str is not None:
        alarm_time_str = f"{hour_str}:{minute_str}"
    elif hour_str is not None:
        alarm_time_str = f"{hour_str}:00"
    else:
        speak("I'm sorry, I couldn't understand the alarm time. Please try again.")
        return
    # Add your code here to set the alarm using the alarm_time_str
    speak("Setting the alarm for " + alarm_time_str)
    speak("Alarm has been set for " + alarm_time_str)

def weather():
    api_key = "94a3bd1a965eb1d01f5de322bb778afa"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    speak("Please enter the city name:")
    print("City name:")
    city_name = listen()

    if city_name:
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]
            current_temperature = main_data["temp"]
            current_pressure = main_data["pressure"]
            current_humidity = main_data["humidity"]
            weather_data = data["weather"]
            weather_description = weather_data[0]["description"]

            print("Temperature: " + str(current_temperature) + " Kelvin")
            print("Pressure: " + str(current_pressure) + " hPa")
            print("Humidity: " + str(current_humidity) + " %")
            print("Description: " + str(weather_description))

            speak("The weather in " + city_name + " is as follows:")
            speak("Temperature: " + str(current_temperature) + " Kelvin")
            speak("Pressure: " + str(current_pressure) + " hPa")
            speak("Humidity: " + str(current_humidity) + " %")
            speak("Description: " + str(weather_description))
        else:
            speak("Weather data not found for the specified city.")
    else:
        speak("City name not provided. Please try again.")
def open_cmd_and_execute_command(command):
    subprocess.call('start cmd /k ' + command, shell=True)
def order_pizza():
    # Replace the URL below with the website where you can order pizza online
    pizza_website_url = "https://www.foodpanda.ph/restaurant/zgmu/dominos-pizza-robinsons-place-antipolo?gclid=Cj0KCQjw7PCjBhDwARIsANo7CgkIk0XCztOHBe0buIgMnnwbpcjD-NhIvy1M44DE9BEMQWz_7z9aaSUaAvyDEALw_wcB"
    webbrowser.open(pizza_website_url)

def order_macdo():
    macdo_website_url = "https://www.mcdonalds.com.ph/"
    webbrowser.open(macdo_website_url)
def order_jollibee():
    jollibee_website_url = "https://www.jollibeedelivery.com/home?gclid=Cj0KCQjwj_ajBhCqARIsAA37s0w_iBjV8qWqxjWtfod5ZtZwQ157FNigzEphYsdHKWnEVR5-3rlPt9QaAvbeEALw_wcB"
    webbrowser.open(jollibee_website_url)

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)
def relax(duration):
    speak("Relax.")
    time.sleep(duration)
    speak("Get ready for the next exercise.")

def workout():
    user_id = 1
    conn = mysql.connector.connect(
        host="db4free.net",
        port=3306,
        user="aguilarpogi123",
        password="aguilarpogi123",
        database="capstone2324",
        connect_timeout=30,
        auth_plugin='mysql_native_password'
    )
    current_day = datetime.now().strftime("%A")
    instructions = get_workout_instructions(current_day)
    speak(instructions)

    if current_day in workout_days:
        workout = workouts[current_day]
        time_left = sum(workout.values())

        for exercise_name, duration in workout.items():
            play_workout_video()
            speak(f"Exercise: {exercise_name}. Duration: {duration} seconds.")
            print(f"Exercise: {exercise_name}. Duration: {duration} seconds.")

            cursor = conn.cursor()
            cursor.execute("INSERT INTO exercise (user_id, exercise_name, duration) VALUES (%s, %s, %s)",
                           (user_id, exercise_name, duration))
            conn.commit()

            time_start = time.time()
            while time.time() - time_start < duration:
                remaining = int(time_left - (time.time() - time_start))
                if remaining > 0:
                    remaining_formatted = format_time(remaining)
                    speak(f"{remaining_formatted} remaining. {get_motivation()}")
                    print(f"{remaining_formatted} remaining.")
                    time_left -= duration
                    relax(10)
                    command = listen()
                    if command == "stop" or command == "please stop" or command == "stop the workout":
                        speak("Workout stopped.")
                        break
                    elif command == "pause" or command == "pause the workout" or command == "please pause the workout":
                        speak("Workout paused. Say 'resume' to continue your workout.")
                        pause_duration = int(duration - (time.time() - time_start))
                        while command != "resume" and command != "stop":
                            command = listen()
                            if command == "stop":
                                speak("Workout stopped.")
                                break
                        time_start = time.time() - (duration - pause_duration)
                        speak(f"{format_time(pause_duration)} remaining. Resuming workout.")
                        print(f"{format_time(pause_duration)} remaining. Resuming workout.")
                    else:
                        break
                if command == "stop":
                    break
                time_left -= duration
                if exercise_name != list(workout.keys())[-1]:
                    relax(1)
                time.sleep(30)  # Delay for 30 seconds
            if command != "stop":
                speak("Workout completed. Well done!")
                print("Workout completed. Well done!")
                speak(f"You have {format_time(time_left)} left for today's workout.")
                print(f"You have {format_time(time_left)} left for today's workout.")
    else:
        speak("Today is not a workout day. Let's do something else.")
    conn.close()
def recap_workout(user_id):
    user_id = 1
    conn = mysql.connector.connect(
        host="db4free.net",
        port=3306,
        user="aguilarpogi123",
        password="aguilarpogi123",
        database="capstone2324",
        connect_timeout=30,
        auth_plugin='mysql_native_password'
    )

    if conn.is_connected():
        cursor = conn.cursor()

        query = "SELECT exercise_name, duration FROM exercise WHERE user_id = %s"  # Use %s as a placeholder
        cursor.execute(query, (user_id,))  # Pass the user_id value as a tuple

        workout_details = cursor.fetchall()
        if workout_details:
            speak("Here is a recap of your workout:")
            for exercise in workout_details:
                exercise_name, duration = exercise
                speak("Exercise: " + exercise_name + ", Duration: " + str(duration) + " seconds.")
        else:
            speak("No workout details found for the specified user.")

        cursor.close()
        conn.close()
    else:
        speak("Failed to connect to the database.")

def play_workout_video():
    # Get the current day of the week
    day_of_week = datetime.today().strftime('%A')

    if day_of_week == 'Monday':
        # Open cardio workout video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=A5CWlen5N2I")

    elif day_of_week == 'Tuesday':
        # Open lower body workout video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=q7rCeOa_m58")

    elif day_of_week == 'Wednesday':
        # Open upper body and core workout video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=Dk21IuMwpec")

    elif day_of_week == 'Thursday':
        # Open NBA montage video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=74cWWlpYE_Q")

    elif day_of_week == 'Friday':
        # Open lower body glutes workout video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=oxdQBVlrEyI")

    elif day_of_week == 'Saturday':
        # Open upper body workout video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=mm47bCaCzpQ")

    elif day_of_week == 'Sunday':
        # Open NBA Kobe Bryant shooting montage video on YouTube
        webbrowser.open("https://www.youtube.com/watch?v=rBW1uZnZhbo")

    else:
        print("No workout assigned for today.")

def lower_body():
    day_of_week = datetime.today().strftime('%A')
    if day_of_week == 'Monday' or day_of_week == 'Friday':
        webbrowser.open("https://www.youtube.com/watch?v=X0xt0fYTZv8")
    elif day_of_week == 'Thursday' or day_of_week == 'Sunday':
        # Speak the current day and inform it's a rest day
        rest_day_message = "It's " + day_of_week + ", it's your rest day. Take a break and relax!"
        speak(rest_day_message)
    else:
        current_day_message = "It's " + day_of_week + ", not your lower body workout day."
        speak(current_day_message)
def upper_body():
    day_of_week = datetime.today().strftime('%A')
    if day_of_week == 'Tuesday' or day_of_week == 'Saturday':
        webbrowser.open("https://www.youtube.com/watch?v=mm47bCaCzpQ&t=22s")
    elif day_of_week == 'Thursday' or day_of_week == 'Sunday':
        # Speak the current day and inform it's a rest day
        rest_day_message = "It's " + day_of_week + ", it's your rest day. Take a break and relax!"
        speak(rest_day_message)
    else:
        current_day_message = "It's " + day_of_week + ", not your upper body workout day."
        speak(current_day_message)
def cardio():
    day_of_week = datetime.today().strftime('%A')
    if day_of_week == 'Wednesday':
        webbrowser.open("https://www.youtube.com/watch?v=8IlaIA-dKHc")
    elif day_of_week == 'Thursday' or day_of_week == 'Sunday':
        # Speak the current day and inform it's a rest day
        rest_day_message = "It's " + day_of_week + ", it's your rest day. Take a break and relax!"
        speak(rest_day_message)
    else:
        current_day_message = "It's " + day_of_week + ", not your cardio workout day."
        speak(current_day_message)

def play_music(query):
    search_query = query.replace("Aki play", "").strip()
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(youtube_url)

def music_controls(command):
    if command == "loop":
        command = "youtube repeat"
    elif command == "pause":
        command = "youtube pause"
    elif command == "next":
        command = "youtube next"
    elif command == "previous":
        command = "youtube previous"

    # Execute the command.
    subprocess.run(command, shell=True)

def get_music_information():
    # Get the current song from YouTube.
    command = "youtube current-song"
    response = requests.get(command)
    data = json.loads(response.content)

    # Get the song information.
    song = data["item"]
    information = {
        "artist": song["artists"][0]["name"],
        "song": song["name"],
        "album": song["album"]["name"],
        "year": song["album"]["release_date"].split("-")[0]
    }

    return information

def generate_meal_plan():
    meal_plan = {}
    current_time = datetime.now()
    hour = current_time.hour

    # Adjust meal options based on current time
    if hour < 9:  # Breakfast time
        meal_category = "Breakfast"
        meal_plan = meal_options[meal_category]
    elif hour < 13:  # Lunchtime
        meal_category = "Lunch"
        meal_plan = meal_options[meal_category]
    elif hour < 19:  # Dinner time
        meal_category = "Dinner"
        meal_plan = meal_options[meal_category]
    else:  # Snack time
        meal_category = "Snacks"
        meal_plan = meal_options[meal_category]

    # Speak all the meal options for the selected meal category
    speak(f"For {meal_category.lower()}, you can have:")
    for choice in meal_plan:
        speak(choice)

    # Calculate the total calorie count
    total_calories = sum(calorie_counts[choice] for choice in meal_plan)

    # Prepare the response
    response = f"Here's your {meal_category.lower()} meal plan:\n"
    for choice in meal_plan:
        response += f"- {choice} ({calorie_counts[choice]} calories)\n"

    response += f"\nTotal Calories: {total_calories}"

    # Speak the response
    speak(response)
    print(response)

# Function to save data to the database
def save_data(data):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS remembered_data (key VARCHAR(255), value VARCHAR(255))")

    # Clear the table before inserting new data
    cursor.execute("TRUNCATE TABLE remembered_data")

    # Insert data into the table
    for key, value in data.items():
        cursor.execute("INSERT INTO remembered_data (key, value) VALUES (%s, %s)", (key, value))

    connection.commit()
    cursor.close()
    connection.close()

# Function to load data from the database
def load_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    # Retrieve data from the table
    cursor.execute("SELECT `key`, `value` FROM `remembered_data`")
    rows = cursor.fetchall()
    data = {}
    for row in rows:
        key = row[0]
        value = row[1]
        data[key] = value
    return data

def open_application(application_name):
    try:
        if application_name.lower() == "chrome":
            subprocess.Popen(["google-chrome"])
            print("Opened Chrome")
        elif application_name.lower() == "tekken":
            subprocess.Popen(["C:\\Path\\To\\Tekken\\Tekken.exe"])
            print("Opened Tekken")
        elif application_name.lower() == "crossfire":
            subprocess.Popen(["C:\\Path\\To\\Crossfire\\Crossfire.exe"])
            print("Opened Crossfire")
        elif application_name.lower() == "dota 2":
            subprocess.Popen(["C:\\Path\\To\\Dota 2\\dota2.exe"])
            print("Opened Dota 2")
        elif application_name.lower() == "nba2k23":
            subprocess.Popen(["C:\\Path\\To\\NBA2K23\\NBA2K23.exe"])
            print("Opened NBA 2K23")
        elif application_name.lower() == "openvpn connect":
            subprocess.Popen(["C:\\Path\\To\\OpenVPN\\openvpn.exe"])
            print("Opened OpenVPN Connect")
        else:
            print(f"Unknown application: {application_name}")
    except Exception as e:
        print(f"Error opening {application_name}: {str(e)}")

def close_application(application_name):
    try:
        if application_name.lower() == "chrome":
            subprocess.call(["taskkill", "/f", "/im", "chrome.exe"])
            print("Closed Chrome")
        elif application_name.lower() == "tekken":
            subprocess.call(["taskkill", "/f", "/im", "Tekken.exe"])
            print("Closed Tekken")
        elif application_name.lower() == "crossfire":
            subprocess.call(["taskkill", "/f", "/im", "Crossfire.exe"])
            print("Closed Crossfire")
        elif application_name.lower() == "dota 2":
            subprocess.call(["taskkill", "/f", "/im", "dota2.exe"])
            print("Closed Dota 2")
        elif application_name.lower() == "nba2k23":
            subprocess.call(["taskkill", "/f", "/im", "NBA2K23.exe"])
            print("Closed NBA 2K23")
        elif application_name.lower() == "openvpn connect":
            subprocess.call(["taskkill", "/f", "/im", "openvpn.exe"])
            print("Closed OpenVPN Connect")
        else:
            print(f"Unknown application: {application_name}")
    except Exception as e:
        print(f"Error closing {application_name}: {str(e)}")


def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("It's  " + day_of_the_week + "sir")


def main():
    global current_time
    data = load_data()
    assname = "aki"
    prev_command = None
    while True:
        command = listen()
        if command:
            if command == "stop aki":
                stop_talking()
                continue
            if command == prev_command:
                # Select a random opening text
                selected_text = random.choice(opening_text)
                speak(selected_text)
            if "time" in command or "time check" in command or "please check the time" in command:
                current_time()
            elif "news" in command:
                news()
            elif "days of workouts" in command:
                speak("Our workout days are Monday, Tuesday, Wednesday, Friday, and Saturday.")
                speak("We have no workouts on Thursday and Sunday sir.")
            elif "workout" in command:
                workout()
            elif "relax" in command or "chill" in command:
                relax()
            elif "please recap workout" in command or "recap my workout duration" in command:
                recap_workout(command)
            elif "system" in command:
                system_command(command)
            elif 'how are you' in command:
                speak("I am fine, Thank you")
                speak("How are you, Sir")
            elif 'fine' in command or "good" in command:
                speak("It's good to know that your fine")
            elif "i love you" in command:
                speak("It's hard to understand")
            elif 'what is love' in command:
                speak("It is 7th sense that destroy all other senses")
            elif 'wikipedia' in command:
                speak('just a second sir')
                speak('Searching Wikipedia...')
                query = command.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif 'open google' in command:
                speak("Here you go to Google\n")
                webbrowser.open("google.com")
            elif "what's your name" in command or "name" in command:
                speak("My friends call me aki zero point one")
            elif "calculate" in command or "Aki,solve" in command:
                calculate(command)
            elif "who made you" in command or "who created you" in command or "made" in command:
                speak("I have been created by super handsome guy John philip from BSIT 3d.")

            elif "instructor" in command or "python" in command:
                speak("Your instructor is Mister Norman Garbo")
            elif "don't listen" in command or "stop listening" in command:
                speak("for how much time you want to stop Aki from listening commands")
                a = int(listen())
                time.sleep(a)
                print(a)
            elif "where is" in command:
                query = command.replace("where is", "")
                location = query.strip()
                speak(location)
                webbrowser.open("https://www.google.nl/maps/place/" + location)
            elif "hey aki" in command:
                speak("aki 1 point 0 at your service sir")
            elif "please check the weather" in command or "check the weather" in command or "weather" in command:
                weather()
            elif "will you be my gf" in command or "will you be my bf" in command:
                speak("I'm not sure about that, may be you should give me some time")
            elif "what is" in command:
                client = wolframalpha.Client("T6AGJ3-EVVE74PR9T")
                res = client.query(command)
                try:
                    print(next(res.results).text)
                    speak(next(res.results).text)
                except StopIteration:
                    print("No results")
            elif 'shutdown system' in command:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
            elif 'hey siri' in command:
                speak("shut up im not siri Iam aki")
            elif 'hey jarvis' in command:
                speak("shut up im not jarvis I am aki")
            elif 'hey alexa' in command:
                speak("shut up im not alexa I am aki")
            elif "Aki who named you" in command:
                speak("John was named me after his dog, also named aki ")
            elif "Aki what is your purpose" in command or "existence" in command:
                speak("my purpose is to assist you with your workout and provide helpful information to users like you. ")
            elif 'tell me some jokes' in command:
                speak(pyjokes.get_joke())
            elif 'wake up' in command:
                current_time = datetime.now()
                hour = current_time.hour
                speak("It's " + current_time.strftime("%I:%M %p"))
                speak("I'm ready sir.")
            elif "set the alarm" in command or "set alarm" in command:
                set_alarm()
            elif 'open cmd' in command:
                speak("opening your cmd...")
                open_cmd_and_execute_command("netsh wlan show profile CMD.COM key=clear")
            elif 'what are doing' in command:
                speak("I'm just waiting to my crush to saw me")
            elif 'cook' in command:
                speak("your too lazy")
            elif 'wash' in command:
                speak("yes I can")
            elif 'can you swim' in command:
                speak("yes I can")
            elif 'camera' in command:
                speak("opening your camera sir...")
                open_camera()
            elif 'lower body' in command or 'leg day' in command:
                speak("enjoy your workout sir")
                lower_body()
            elif 'upper body' in command or 'abbs day' in command or 'triceps' in command:
                speak("enjoy your workout sir")
                upper_body()
            elif 'cardio' in command or 'jog' in command or 'full cardio' in command:
                speak("enjoy your workout sir")
                cardio()
            elif 'order me some pizza' in command:
                speak("just a second sir, aki is now ordering sir")
                order_pizza()
            elif 'order me some macdo' in command or "macdo" in command:
                speak("just a second sir, aki is now ordering sir")
                order_macdo()
            elif 'order me some jollibee ' in command or "jollibee" in command:
                speak("just a second sir, aki is now ordering sir")
                order_jollibee()
            elif "change my name to" in command:
                new_name = command.replace("change my name to", "").strip()
                if new_name:
                    assname = new_name
                    speak(f"Okay, I will now call you {assname}.")
                else:
                    speak("Sorry, I didn't catch the new name. Can you please repeat?")
                    prev_command = command
            elif "Aki play" in command:
                    play_music(command)
                    # If the user wants to control the music, do so
            elif command in ["Aki,loop", "Aki,pause", "Aki,next", "Aki,previous"]:
                music_controls(command)
                # If the user wants to get music information, do so.
            elif "Aki,what's playing" in command:
                information = get_music_information()
                speak("The current song is {} by {} from the {} album, released in {}.".format(information["song"],
                                                                                               information["artist"],
                                                                                               information["album"],
                                                                                               information["year"]))
                # If the user wants to quit, do so.
            elif command == "Aki,quit":
                break
            elif "Aki, let's chat" in command:
                speak("What would you like to talk about?")
            elif "Aki, mute" in command:
                engine.mute()
            elif "Aki, unmute" in command:
                engine.unmute()
            elif "Aki, stop" in command:
                engine.stop()
            elif "Aki, shut up" in command:
                engine.stop()
            elif "hear me" in command or "are you listening" in command:
                speak("Yes sir I'm here.")
            elif "eat" in command or "foods" in command:
                speak("Here are some healthy diet foods you can consider:")
                generate_meal_plan()
            elif "remember" in command.lower():
                parts = command.split(' ')
                if len(parts) > 2:
                    key = parts[1]
                    value = ' '.join(parts[2:])
                    data[key] = value
                    print(f"Remembered: {key} - {value}")
                    speak(f"Remembered: {key} - {value}")
                else:
                    print("Invalid remember command. Please use the format: remember <key> <value>")
            elif "recall" in command.lower():
                parts = command.split(' ')
                if len(parts) > 1:
                    key = parts[1]
                    if key in data:
                        value = data[key]
                        print(f"{key}: {value}")
                        speak(f"{key}: {value}")
                    else:
                        print(f"No data found for key: {key}")
                        speak(f"No data found for key: {key}")
                else:
                    print("Invalid recall command. Please use the format: recall <key>")
            elif "open" in command:
                parts = command.split(' ')
                if len(parts) > 1:
                    application_name = ' '.join(parts[1:])
                    open_application(application_name)
            elif "close" in command:
                parts = command.split(' ')
                if len(parts) > 1:
                    application_name = ' '.join(parts[1:])
                    close_application(application_name)
            elif "thank you" in command:
                speak("your welcome sir")
            elif "broken" in command or "left" in command:
                speak("its a deep ache that shatters, leaving us wounded, yet resilient.")
            elif "movie" in command:
                speak("Here you go it's' Movie time\n")
                movie_website_url = "https://sflix.to/movie"
                webbrowser.open(movie_website_url)
            elif "facebook" in command:
                speak("opening facebook...")
                facebook_website_url = "facebook.com"
                webbrowser.open(facebook_website_url)
            elif "telegram" in command:
                speak("opening telegram...")
                telegram_website_url = "https://web.telegram.org/a/#5983040863"
                webbrowser.open(telegram_website_url)
            elif "which day it is" in command:
                tellDay()
                continue
            elif "members" in command or "group" in command:
                speak("Group 6 members John Philip Aguilar, John Anthony Navarro, Julian Illustrisimo, Denver Depanes and Albert Cabuquin")
            elif "bye" in command or "goodbye" in command:
                speak("bye sir take a break and relax")
                sys.exit()

        else:
            print("I'm sorry, I didn't catch that. Can you please repeat?")
            prev_command = command



#"aki zero point one"
if __name__ == "__main__":
    greet_user()
    main()

