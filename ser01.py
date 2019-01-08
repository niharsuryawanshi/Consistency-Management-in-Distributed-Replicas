#Server socket code
#Nihar Suryawanshi
#UTA id: 1001654583

import Tkinter
from socket import *
from threading import Thread
import threading
import time
import datetime
import re
from Queue import Queue
from decimal import Decimal
import ast 
from simpleeval import simple_eval

top = Tkinter.Tk()
top.title("High Power Distributed Server")
ch_sr = 1
con_array=[]
array_inp=['1']
serverPort = 5660

defacto_dict={}

var1 = 0

init_str='1'
final_result='1'




global q
q = Queue()

#METHOD TO ACCEPT NEW INCOMMING CONNECTIONS
def accept_con():
	global con_array
	op_wind.insert(Tkinter.END,"Waiting for client..")
	while 1:
		#Listening to the incomming request
		connectionSocket, addr = serverSocket.accept()
		#storing connection socket in array of dictonaries
		#Dictionary
		con_dict = {addr:connectionSocket}
		#array
		con_array.append(con_dict)

		op_win02.insert(Tkinter.END,"Client "+str(addr)+" Connected.")
		#print con_dict
		#print con_array

		t2=Thread(target = listen_to_client, args = (connectionSocket,addr))
		t2.daemon = True
		t2.start()

		
		

		
#https://docs.python.org/3/library/queue.html
#Deque function is taken care here for each tread in queue.
def cord():

	global con_array
	global var1
	global init_str
	global defacto_dict

	#print"starting Queue while"
	time.sleep(3)
	while not q.empty():
		time.sleep(3)
		#print"release set 1 for appending"
		e = q.get()
		e.set()

	#sorting inputs according to timestamp
	time.sleep(3)
	print "Dictionary view Final.."
	print defacto_dict
	#sort based on time stamp
	i=0
	for key in sorted(defacto_dict.keys()):
		#print"inside sorted"
		print key
		init_str=init_str+defacto_dict[key]
		print init_str
		i=i+1
	#print "final list in dict:"+str(i)
 
 	
 	#time.sleep(2)
 	print"Expression Final:"
 	print init_str

	var1=0

	time.sleep(0.5)

	print"calculating on server.."
	final_result = simple_eval(init_str)
	print final_result

	time.sleep(0.5)

	#sending final result to the client
	for con in con_array:
		for key, value in con.iteritems():
			value.send(str(final_result))

	#Storing the final result
	init_str=str(final_result)

	#deletig from dictionary
	#https://stackoverflow.com/questions/10446839/does-dictionarys-clear-method-delete-all-the-item-related-objects-from-memory
	defacto_dict.clear()

	#print "defacto_dict"
	print defacto_dict
	print "updated result "+init_str




#THIS METHOD PROCESSES THE REQUEST OF CONNECTED CLIENTS, SOCKET OBJECT AND ADDRESS ARE PARAMATERS.
#https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
def listen_to_client(connectionSocket, addr):
	lab01=0
	arr_pol='P'
	global array_inp
	global init_str
	global ch_sr
	global defacto_dict
	global final_result
	pat1= re.compile(r"[0-9+-/*]")
	
	connectionSocket.send(init_str)

	while ch_sr!=0:	
		global con_array
		#connectionSocket.send('HB')
		message = connectionSocket.recv(8096)
		print message

		if message =='bye':
			op_win02.insert(Tkinter.END,"Client "+str(addr)+" Disconnected.")
		 	connectionSocket.close()
		 	
		 	for con in con_array:
				for key, value in con.iteritems():
					if key==addr:
		 				con_array.remove(con)
		 	
		 	print "con array stat"
		 	print con_array
	 	 	lab01=1
	 	 	break

	 	#code for client poll
	 	elif var1==1:
			#message = connectionSocket.recv(2024)
			op_wind.insert(Tkinter.END,"Client Data:")
			op_wind.insert(Tkinter.END,addr)
			op_wind.insert(Tkinter.END,message)
		
		
			#print"set locked 1"
			event = threading.Event()
			q.put(event)
			event.wait()
			#print"set released 1"
			print "Copying to Defacto Dictionary"

			m1=message.split("#")

			#storing into dictionary
			defacto_dict.update({m1[1]:m1[0]})

			print "defacto dict:"
			print defacto_dict
		
			print "data Appended"

			connectionSocket.send('Wait Client server is computinging data')
			
		

#METHOD TO START THE SERVER
def start_server():
	#Starting new Thread to stop GUI Freeze
	op_wind.insert(Tkinter.END,"Starting the Server..")	
	t1 = Thread(target = accept_con)
	t1.daemon = True
	t1.start()
	
#METHOD TO STOP THE SERVER
def stop_server():
	global ch_sr
	print"stop server command"
	ch_sr=0



#creating new thread for incoming client to poll
def poll():
	global	con_array
	
	#to start poll
	global var1 
	var1=1;

	for con in con_array:
		for key, value in con.iteritems():
			value.send('P')

	time.sleep(5)
	t3=Thread(target = cord)
	t3.daemon=True
	t3.start()





#http://www.eg.bucknell.edu/~cs363/2016-spring/lecture-notes/06-SocketProgramming.pptx
#Code to define 
#creating a socket object ServerSocket
serverSocket = socket(AF_INET, SOCK_STREAM) 
#this method binds the socket object to address host name and port no
serverSocket.bind(('',serverPort))
serverSocket.listen(3) #maximum no of Queue connection is set to 5


#https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
#Code For GUI 
btn_start = Tkinter.Button(top,text="Start", command = start_server)
btn_start.grid(row=0, column=0)

btn_close = Tkinter.Button(top,text="Stop", command = stop_server)
btn_close.grid(row=0, column=1)

btn_poll = Tkinter.Button(text="Poll", command = poll)
btn_poll.grid(row=0, column=2)

Tlab1 = Tkinter.Label(top,text="Connection Status")
Tlab1.grid(row=1,columnspan=3)

op_win02 = Tkinter.Listbox(top,height=8,width=40)
op_win02.grid(row=2 ,columnspan=3)

Tlab2 = Tkinter.Label(top,text="Console")
Tlab2.grid(row=3,columnspan=3)

op_wind = Tkinter.Listbox(top,height=20, width=40)
op_wind.grid(row=4,columnspan=3)

top.mainloop()