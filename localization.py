from model import get_setting
from os import path
import json

current_locale = get_setting("language")

EN_MONTHS = [
			"January",
			"February",
			"March",
			"April",
			"May",
			"June",
			"July",
			"August",
			"September",
			"October",
			"November",
			"December"
		]

base = {
		"localization_name": "English",
		"today": "Today",
		"calendar": "Calendar",
		"timetables": "Timetables",
		"new_event": "New task",
		"event_name": "name",
		"event_datetime": "date and time",
		"event_is_important": "is important",
		"event_tags": "tags", "new_tag": "new tag",
		"no_tags": "none",
		"create": "create",
		"months":EN_MONTHS,
		"months2":EN_MONTHS,
		"weekdays":[
			"Monday",
			"Tuesday",
			"Wednesday",
			"Thursday",
			"Friday",
			"Saturday",
			"Sunday"
		],
		"mb_event":"Event",
		"mb_new":"new",
		"mb_settings":"settings",
		"settings":"Settings",
		"lang":"Language",
		"custom_lang":"custom",
		"load_lang":"search"
}



try:
	if current_locale == "en_US":
		wordlist = base
	else:
		with open(path.join("localization",f"{current_locale}.json")) as file:
			wordlist = json.load(file)
except (FileNotFoundError,UnicodeError):
	wordlist = base

def word(key:str):
	try:
		return wordlist[key]
	except KeyError:
		try:
			return base[key]
		except KeyError:
			return key




