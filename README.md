# Consistency-Management-in-Distributed-Replicas
Sample Project for Consistency Management in Distributed replicas of data. 
The project is coded in Python. 
TCP sementics are used.

Working:
Given are n clients connected simultaneously to the server.
Every Client has a calculator. Each client can perform operations on calculator locally.
Server has option to poll the clients for latest operations.
Server polls the clients and all the local operation are uploaded to server accoding to time stamp.
Server calculates the final result and pushes the latest result to all the clients.
The latest copy of result gets uploaded to all the clients.

Features:
1) Server handles multiple requests simultaneously.
2) Real time client connections and disconnections are displayed.
3) Client disconnections are handled sucessfully without server crashing.
4) Persistent storage is maintained for keeping track of the operations performed locally.
