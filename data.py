from datetime import date

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
background-color:#95C8FF;
border-radius:6;
"""

TITLE_STYLE = """
font-size:54px;
font-weight:900;
color:#3B9AFF;
"""

SUBTITLE_STYLE = """
font-size:24px;
font-weight:600;
"""

def format_component(component:int):
	return f"{component if component > 9 else f"0{component}"}"

def format_date(date1:date):
	return f"{date1.day} {MONTHS["RUSSIAN-2"][date1.month-1]} {date1.year}г."

ADD_BUTTON_STYLE = """
padding:14;
background-color:#3B9AFF;
color:white;
font-size:30px;
font-weight:900;
border-radius:10;
"""

MAIN_BUTTON_STYLE = """
background-color:#3B9AFF;
color:white;
font-size:25px;
font-weight:900;
border-radius:10;
"""