from datetime import time as dtime,date as ddate,timedelta,datetime
from functools import partial
from os import mkdir, environ, path, listdir, remove,rmdir
from typing import Any, Self, Callable,Optional
import platform
import json,time as ptime
from data import format_time
import threading,locale
from uuid import uuid1


CURRENT_FORMAT_VERSION = "1.2"


FORMATTERS:dict[str,Callable[[dict],dict]] = {}

DEFAULT_SETTINGS = {
	"language":locale.getlocale()[0]
}


class EventDecoderError(Exception):...

user_os = platform.platform()

if user_os[:5] == "macOS":
	from mac_notifications import client
	def remind_later(title:str,time:str):
		client.create_notification(
			title=f"{title}(повтор)",
			subtitle=time,delay=timedelta(minutes=5))

	def notificationListener(signal:threading.Event):
		today = ddate.today()
		upcoming = load_all(today)
		while not signal.is_set():
			for event in upcoming:
				current_time = datetime.now().time()
				if current_time >= event.time:
					notification_title = event.name
					notification_subtitle = format_time(event.time)
					client.create_notification(title=notification_title,
											   subtitle=notification_subtitle,
											   action_button_str="Напомнить через 5 мин.",
											   action_callback=partial(remind_later,notification_title,notification_subtitle))
					delete(today,event.id)
			upcoming = load_all(today)
			ptime.sleep(2)
		client.stop_listening_for_callbacks()


	app_path = f"{environ.get("HOME")}/Library/Application Support/live-smarter"

	dir_path = path.join(app_path, "db")

	timetables_path = path.join(dir_path, "timetables")
elif user_os[:7] == "Windows":
	app_path = f"{environ.get("APPDATA")}/live-smarter"
	dir_path = path.join(app_path, "db")
	timetables_path = path.join(dir_path, "timetables")


"""def UUID() -> str:
	ids = get_uuids()
	result = "".join([
		choice(ascii_letters+digits)
		for _ in repeat(None,40)
	])
	while result in ids:
		result = "".join([
			choice(ascii_letters+digits)
			for _ in repeat(None, 12)
		])
	with open(path.join(app_path,"local_uuids.txt"),"a") as file:
		file.write(f"\n{result}")
	return result"""

class Event:
	"""
	The class for managing calendar events
	"""
	def __init__(self,
				 name:str,
				 time:dtime,
				 isImportant:bool,
				 uuid:str = str(uuid1()),
				 completed:bool=False,
				 is_repeating_event:bool=None
				 ):
		"""
		Create an event
		"""
		if is_repeating_event is None:
			self.is_repeating_event = False
		else:
			self.is_repeating_event = is_repeating_event
		self.name = name
		self.time = time
		self.isImportant = isImportant
		self.completed = completed
		self.version = CURRENT_FORMAT_VERSION
		self.id = uuid

	def __hash__(self):
		return self.id

	@classmethod
	def decode(cls,data:dict[str,Any],uuid:str) -> Optional[Self]:
		event_version = data["version"]
		if event_version == CURRENT_FORMAT_VERSION:
			try:
				result = cls(data["name"],
							 dtime.fromisoformat(data["time"]),
							 data["isImportant"],
							 uuid,
							 data["completed"],
							 is_repeating_event=data.get("is_repeating_event")
							 )
				return result
			except KeyError as e:
				raise EventDecoderError(f"\nevent version is alright, but the contents are corrupted\n{e}!")
		else:
			if event_version in FORMATTERS:
				return cls.decode(FORMATTERS[event_version](data),str(uuid1()))
			else:
				raise EventDecoderError(f"\nCannot decode event of version {event_version}!")

	def save(self) -> dict:
		return {"name":self.name,
				"time":self.time.isoformat(),
				"version":self.version,"isImportant":self.isImportant,
				"completed":self.completed,
				}




def get_uuids() -> list[str]:
	with open(path.join(app_path,"local_uuids.txt")) as file:
		ids = file.readlines()
	return ids



def setup_directory():
	if not path.exists(dir_path):
		print("Setting up the directory!")
		mkdir(app_path)
		mkdir(dir_path)
		mkdir(timetables_path)
		with open(path.join(app_path, "settings.json"), "w") as settings_file:
			json.dump(DEFAULT_SETTINGS,settings_file)

def add_overrides_timetable(date:ddate,timetable_id:str,new:Event):
	date_path = create_date_path(date)
	local_timetable_path = path.join(dir_path,date_path, "overrides_timetables")
	try:
		mkdir(local_timetable_path)
	except FileExistsError:
		pass

	current_item_path = path.join(local_timetable_path,timetable_id)

	with open(current_item_path,"w") as file:
		json.dump(new.save(),file)


def get_overrides_timetable(date:ddate):
	date_path = create_date_path(date)
	local_timetable_path = path.join(dir_path,date_path, "overrides_timetables")
	print("L",local_timetable_path)
	if path.exists(local_timetable_path):
		all_items_ids = listdir(local_timetable_path)
		print("A",all_items_ids)

		all_items = []

		for timetable_id in all_items_ids:
			current_item_path = path.join(local_timetable_path, timetable_id)

			with open(current_item_path) as file:
				result = json.load(file)
				result["is_repeating_event"] = True
				all_items.append(Event.decode(result,timetable_id))

		return all_items
	print("B")
	return []

setup_directory()

def create_date_path(date:ddate):
	return path.join(str(date.year),str(date.month),str(date.day))

def delete(date:ddate,uuid:str):
	date_path = path.join(dir_path,create_date_path(date))
	event_path = path.join(date_path,uuid)
	remove(event_path)
	if len(listdir(date_path)) == 0:
		rmdir(date_path)
		month_path = path.join(dir_path,str(date.year),str(date.month))
		if len(listdir(month_path)) == 0:
			rmdir(month_path)
			year_path = path.join(dir_path,str(date.year))
			if len(listdir(year_path)) == 0:
				rmdir(year_path)


def load_all(date:ddate|int,timetable:bool=False) -> list[Event]:
	if not timetable:
		load_dir_path = create_date_path(date)
	else:
		load_dir_path = path.join(timetables_path,str(date))

	try:
		all_item_names = listdir(path.join(dir_path,load_dir_path))
	except FileNotFoundError:
		all_item_names = []
		pass
	all_items = []
	for name in all_item_names:
		try:
			print(name)
			with open(path.join(dir_path,load_dir_path,name)) as file:
				all_items.append(
					Event.decode(json.load(file),name)
				)
		except (FileNotFoundError,UnicodeError,IsADirectoryError) as e:
			print(f"Nothing planned, {e}")
	if not timetable:
		all_items+=get_timetable_for_date(date)
	return sorted(all_items,key=lambda x:x.time)


def save_item(date:ddate,item:Event):
	if not item.is_repeating_event:
		if not path.exists(p1:=path.join(dir_path,str(date.year))):
			mkdir(p1)
		if not path.exists(p2:=path.join(dir_path,p1,str(date.month))):
			mkdir(p2)
		if not path.exists(p3:=path.join(dir_path,p1,p2,str(date.day))):
			mkdir(p3)
		with open(path.join(p3,item.id),"w") as file:
			json.dump(item.save(),file)
	else:
		print("!")
		add_overrides_timetable(date,item.id,item)


def save_to_timetable(weekday:int,item:Event):
	folder_path = path.join(timetables_path,str(weekday))
	if not path.exists(folder_path):
		mkdir(folder_path)
	with open(path.join(folder_path,
						item.id),"w") as file:
		json.dump(item.save(),file)


def get_timetable(date:int):
	return load_all(date,timetable=True)


def id_map(item_list:list[Event]):
	return {i.id:i for i in item_list}

def set_repeating(i:Event):
	i.is_repeating_event = True

def get_timetable_for_date(date:ddate):
	timetable = id_map(get_timetable(date.weekday()+1))
	modifications = id_map(get_overrides_timetable(date))

	print(modifications)

	complete = []


	for item in timetable:
		if item in modifications:
			i = modifications[item]
			set_repeating(i)
			complete.append(i)
		else:
			i = timetable[item]
			set_repeating(i)
			complete.append(i)


	return complete

def get_active_dates(year:int,month:int):
	all_days:dict[str:int] = {}
	all_years = listdir(dir_path)
	if str(year) in all_years:
		all_months = listdir(path.join(dir_path,str(year)))
		if str(month) in all_months:
			all_days = {i:len(listdir(
				path.join(dir_path,str(year),str(month),str(i))
			)) for i in listdir(path.join(dir_path,str(year),str(month))) if i[0] != "."}
	keys = list(all_days.keys())
	keys.sort()
	results = {i: all_days[i] for i in keys}
	return results


with open(path.join(app_path,"settings.json")) as rfile:
	settings = json.load(rfile)

def get_setting(key:str):
	return settings[key]

def set_setting(key:str,value):
	settings[key] = value
	with open(path.join(app_path, "settings.json"),"w") as wfile:
		json.dump(settings,wfile)