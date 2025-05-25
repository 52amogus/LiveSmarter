from datetime import date,time as dtime
#from localization import word

SIDEBAR_BUTTON_STYLE = """
font-size:15px;
color:white;
font-weight:500;
border-radius:6;
"""

SIDEBAR_BUTTON_STYLE_SELECTED = """
font:15px;
font-weight:700;
color:white;
background-color:#3B9AFF;
border-radius:6;
"""

TITLE_STYLE = """
font-size:54px;
font-weight:900;

"""

SUBTITLE_STYLE = """
font-size:24px;
font-weight:600;
"""

def format_component(component:int):
	return f"{component if component > 9 else f"0{component}"}"


def format_time(time:dtime):
	return f"{time.hour}:{format_component(time.minute)}"

ADD_BUTTON_STYLE = """
padding:14;
background-color:#3B9AFF;
color:white;
font-size:30px;
font-weight:600;
border-radius:10;
"""

LIST_ROW_STYLE = """
background-color:#3B9AFF;
border-radius:10;
font-size:20px;
font-weight:600;
color:white;
"""

IMPORTANT_ROW_STYLE = """
background-color:#FF4C4C;
border-radius:10;
font-size:20px;
font-weight:900;
color:white;
"""

LIST_LAYER2_STYLE = """
background-color:#8BC3FF;
border-radius:10;
font-size:20px;
font-weight:600;
padding-left:10;
color:white;
"""

MAIN_BUTTON_STYLE = """
background-color:#3B9AFF;
color:white;
font-size:15px;
font-weight:900;
border-radius:10;
"""


MONTHS = {
	"RUSSIAN":
		["Январь",
		 "Февраль",
		 "Март",
		 "Апрель",
		 "Май",
		 "Июнь",
		 "Июль",
		 "Август",
		 "Сентябрь",
		 "Октябрь",
		 "Ноябрь",
		 "Декабрь"],
	"RUSSIAN-2":[
		"Января",
		"Февраля",
		"Марта",
		"Апреля",
		"Мая",
		"Июня",
		"Июля",
		"Августа",
		"Сентября",
		"Октября",
		"Ноября",
		"Декабря",
	],
	"DEFAULT":None
}

WEEKDAYS = {
	"RUSSIAN":[
		"Понедельник",
		"Вторник",
		"Среда",
		"Четверг",
		"Пятница",
		"Суббота",
		"Воскресенье",
	]
}