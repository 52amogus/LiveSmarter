import json
import socket
from datetime import date,time
from typing import Optional, override
from model import Event


class ServerConfig:
	address = '5.129.201.198'
	port = 8080
	addr = (address,port)

class Session:
	def __init__(self,address:tuple[str,int],account_uuid,token):
		self.client = Client(socket.AF_INET,socket.SOCK_STREAM)
		self.client.connect(address)

		self.id = self.client.app_login(account_uuid,token)



	def get_active_dates(self,year,month):
		msg = {
			"type":"get_active_dates",
			"session_id":self.id,
			"contents":{"year": year,
			 "month": month}
		}
		result = self.client.request(msg,"action",is_result=True)
		return result

	#@staticmethod
	def end(self):
		self.client.request("!DISCONNECT","disconnect",is_result=False)
		print("[INFO] Session ended")

	def load_all(self,items_date:date):
		msg = {
			"type":"load_all",
			"session_id":self.id,
			"contents":{"date":items_date.isoformat()}
		}

		result = self.client.request(msg,"action",is_result=True)

		event_list:list[Event] = []

		for item in result:
			event_list.append(Event.decode(item[1],item[0]))

		return event_list


	def save_item(self,item:Event,item_date):
		msg = {
			"type":"save_item",
			"session_id":self.id,
			"contents":{
				"date":item_date.isoformat(),
				"item":item.save(),
				"itemid":item.id
			}
		}

		self.request(msg,"action",is_result=False)


class Client(socket):
	def request(self, msg, msgtype, *, is_result:bool) -> Optional:
		"""
		Send a request to the server and receive a response if there is one.
		:param msg:
		:param msgtype:
		:param is_result:
		:return:
		"""
		header = json.dumps(
			{"platform":"pc","length":len(json.dumps(msg)),"msg_type":msgtype,"is_result":is_result},ensure_ascii=False
		)
		header+="".join(" " for _ in range(96-len(header)))
		self.send(header.encode())
		self.send(json.dumps(msg).encode())

		if is_result:
			size = self.recv(5)
			result = self.recv(int(size.decode()))

			result = result.decode()

			result = json.loads(result)

			result_message = result["msg"]

			print(f"[INFO] result : {result_message} of type {result["type"]}")

			return result_message
		else:
			return None


	def login_user(self,user_login,user_password):
		msg = {
			"login":user_login,
			"password":user_password
		}
		result = self.request(msg,"userauth",is_result=True)
		return result

	def register_user(self,user_login,user_password):
		msg = {
			"login":user_login,
			"password":user_password
		}
		print("[INFO] user registered")
		self.request(msg,"register",is_result=False)


	def app_login(self,uuid1:str,token1:str):
		msg = {
			"uuid":uuid1,
			"token":token1
		}
		print("[INFO] app login complete")
		return self.request(msg,"appauth",is_result=True)


if __name__ == "__main__":
	pass