from model import get_setting
from os import path
import json

current_locale = get_setting("language")

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
		"create": "create"
}

try:
	with open(path.join("localization",f"{current_locale}.json")) as file:
		wordlist = json.load(file)
except FileNotFoundError:
	wordlist = base

def word(key:str):
	try:
		return wordlist[key]
	except KeyError:
		return key




