import pyowm
global place

def check_weather(place):
	owm = pyowm.OWM('a5a9581344154c5c50433466c32affdd', language = "ru")
	observation = owm.weather_at_place(place)
	w = observation.get_weather()
	temp = w.get_temperature('celsius')["temp"]
	temp_max = w.get_temperature('celsius')['temp_max']
	temp_min = w.get_temperature('celsius')['temp_min']
	return "В городе " + place + " сейчас " + w.get_detailed_status() + ". Температура сейчас в районе " + str(temp) + " градусов по целсию." + " Температура может опуститься до " + str(temp_min)  + " градусов по целсию" + " и подняться до " + str(temp_max) + " градусов по целсию"