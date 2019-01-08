#Client socket code
#Nihar Suryawanshi
#UTA id: 1001654583

import Tkinter
from socket import *
import time
import random
from threading import Thread
import datetime
import re
from decimal import Decimal
from simpleeval import simple_eval
import datetime

#Global Variables
top = Tkinter.Tk()
top.title("Client Handler")
serverName = 'localhost'
serverPort = 5660
ch01 = 1
final_result = '0'
init_str='1'
send_str=''

send_array=[]

no = random.randint(1,98)



#METHOD TO START CLIENT
def st():
	op_wind.insert(Tkinter.END,"Starting the client..")	
	t1 = Thread(target = start_client)
	t1.daemon = True
	t1.start()


#METHOD TO START THE CLIENT 01
def start_client01():
	#To restart the server
	global ch01
	ch01 = 1
	#http://www.eg.bucknell.edu/~cs363/2016-spring/lecture-notes/06-SocketProgramming.pptx
	clientSocket = socket(AF_INET, SOCK_STREAM)
	#connect the socket to welcoming socket
	clientSocket.connect((serverName,serverPort))	

	#starting new thread for processing input and output
	t3 = Thread(target = send_rec01,args=(clientSocket,))
	t3.deamon=True
	t3.start()


	t4= Thread(target = stop_client01,args=(clientSocket,))
	t4.deamon=True
	t4.start()





#METHOD TO SEND AND RECEIVE DATA TO AND FROM SERVER		
def send_rec01(clientSocket):
	close_fg = 0
	global send_str
	global init_str

	while ch01!=0:
		
		poll, serverAddress = clientSocket.recvfrom(8096)
		print poll

		if poll == 'P':
			op_wind.insert(Tkinter.END,"Poll from server")

			clientSocket.sendto(send_str,(serverName,serverPort))
			#printig on GUI
			op_wind.insert(Tkinter.END,"Data Sent to Server")

		elif check_decimal(poll):
			print "server value"+ poll		
			op_wind.insert(Tkinter.END,"Update Result from Server")
			op_wind.insert(Tkinter.END,poll)	
			
			send_str=''
			init_str=poll

			# del inp_array[:]
			# del send_array[:]
			# inp_array.append(poll)
			print "updated value:"	
			print init_str

		elif poll == 'exit':
			op_wind.insert(Tkinter.END,"SERVER SHUT.\nCLIENT SHUTTING DOWN")
			clientSocket.close()
			break

		else:
			print poll

	#print"Exit While"

	clientSocket.sendto("bye",(serverName,serverPort))
	op_wind.insert(Tkinter.END,"Client 01 Stopped..")
	clientSocket.close()

					

#METHOD TO STOP THE CLIENT
def stop_client01(clientSocket):
	global ch01
	null=0
	while ch01!=0:
		null=0
	#ch01=0
	
	print ch01
	clientSocket.sendto("bye",(serverName,serverPort))

#Method to stop the client
def stop_cli():
	global ch01
	ch01=0

#Method to calculate the client
def calculate():

	global no
	global send_str
	final_result = simple_eval(init_str)
	final_result=round(final_result,4)
	op_wind.insert(Tkinter.END,"Local Result: ")
	op_wind.insert(Tkinter.END,final_result)

	#Writing to persistent storage

	dat1 = datetime.datetime.utcnow()
	
	print dat1
	#https://www.guru99.com/reading-and-writing-files-in-python.html
	fin=open("cli"+str(no)+".txt","a+")
	fin.write(str(dat1)+" :"+send_str)

	fin.close()


#Method to get the inputs
def get_input():
	global user_inp
	global init_str
	global send_str
	

	pat1=re.compile(r"[/]{1}[0]{1}")

	inp_str = user_inp.get()

	if  not pat1.match(inp_str):

	
		user_inp.delete(0,Tkinter.END)
		op_wind.insert(Tkinter.END,inp_str)

		init_str=init_str+inp_str
		#send_str=inp_str

		t1=time.time()
		send_str = inp_str+"#"+str(t1)

		print send_str
		print init_str
	else:
		op_wind.insert(Tkinter.END,"Divide by zero detected.")
	
#method to check if decimal
def check_decimal(s):
	try:
		complex(s)
	except ValueError:
		return False

	return True


	


#Code For GUI
#Input text section 
user_inp = Tkinter.Entry(top, text="enter input")
user_inp.grid(rowspan=2,column=0)
#Enter Button
btn_enter = Tkinter.Button(top,width=5,text="Enter", command=get_input)
btn_enter.grid(row=0,column=1)
#Execute Button
btn_exec = Tkinter.Button(top,width=5,text="Execute", command= calculate)
btn_exec.grid(row=0,column=2)
#Connect Button
btn_connect = Tkinter.Button(top,text="Connect", width=5,command = start_client01)
btn_connect.grid(row = 1, column =1)
#Close Button
btn_close01 = Tkinter.Button(top,text="Stop",width=5, command = stop_cli)
btn_close01.grid(row = 1, column =2)
#Output Log
op_wind = Tkinter.Listbox(top,height=20, width=50)
op_wind.grid(row=2,columnspan=3)

top.mainloop()