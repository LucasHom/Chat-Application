import tkinter as tk
import socket
import threading

window = tk.Tk()
window.title("Server")
window.resizable(0, 0)

#Add a top frame consisting of two button widgets
topFrame = tk.Frame(window)
button_start = tk.Button(topFrame, text="Connect", command=lambda: startServer())
button_start.pack(side=tk.LEFT)
button_stop = tk.Button(topFrame, text="Disconnect", command=lambda: stopServer(), state=tk.DISABLED)
button_stop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

#Middle Frames to display host and port info
middleFrame = tk.Frame(window)
hostLabel = tk.Label(middleFrame, text="Host: X.X.X.X")
hostLabel.pack(side=tk.LEFT)
portLabel = tk.Label(middleFrame, text="Port: XXXX")
portLabel.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

#Client frame represents the client area
clientFrame = tk.Frame(window)
clientListLabel = tk.Label(clientFrame, text="**********CLIENT LIST**********")
clientListLabel.pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
clientDisplayText = tk.Text(clientFrame, height=15, width=40)
clientDisplayText.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))

#Insert Demo Clients
for userNum in range(1, 9):
    clientDisplayText.insert(tk.END, f"user{userNum}\n")

scrollBar.config(command=clientDisplayText.yview)
clientDisplayText.config(yscrollcommand=scrollBar.set, background="#f4f6f7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

server = None
HOST_ADRESS = "0.0.0.0"
HOST_PORT = 8080
client_name = ""
clients = []
client_names = []


def startServer():
    global server, HOST_ADRESS, HOST_PORT, client_name, clients, client_names
    button_start.config(state=tk.DISABLED)
    button_stop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST_ADRESS, HOST_PORT))
    server.listen(5)

    threading._start_new_thread(accept_clients, (server, ""))

    hostLabel["text"] = "host: " + HOST_ADRESS
    portLabel["text"] = "port: " + str(HOST_PORT)

def stopServer():
    global server

    button_start.config(state=tk.NORMAL)
    button_stop.config(state=tk.DISABLED)

def accept_clients(server, y):
    while True:
        client,adress = server.accept()
        clients.append(client)

        #Use a thread in order to not clog the goey thread
        threading._start_new_thread(send_receive_client_message, (client, adress))

#Function to receive message from a current client and send to another client
def send_receive_client_message(client_connection, IPadress):
    global server, client_name, clients, clients_adress
    client_message = ""

    #Send a welcome message to clients
    client_name = client_connection.recv(4096)
    client_connection.send("Welcome " + str(client_name) + ".\n" + "Type 'EXIT' to quit")
    client_names.append|(client_name)

    #Helper function to show the clients name connecting or disconnecting
    update_client_names_display(client_names)
    while True:
        data = client_connection.recv(4096)
        if not data:
            break
        if data.upper() == "EXIT":
            break
        client_message = data

        index = get_client_index(clients, client_connection)
        sending_client_name = client_names[index]

        for c in clients:
            if c != client_connection:
                c.send(sending_client_name + "->" + client_message)

    #find the client index then remove from both client name list and connection list
    index = get_client_index(clients, client_connection)
    del client_names[index]
    del clients[index]
    server_message = "closing conection"
    client_connection.send(server_message.encode())
    client_connection.close()
    update_client_names_display(client_names)

def update_client_names_display(client_names_list):
    clientDisplayText.config(state=tk.NORMAL)
    clientDisplayText.delete("1.0", tk.END)
    for user in client_names_list:
        clientDisplayText.insert(tk.END, user+"\n")
    clientDisplayText.config(state=tk.DISABLED)

def get_client_index(client_list, current_client):
    #Helper function to return the index of the current client in the list of clients
    index = 0
    for client in client_list:
        if client[index] == current_client:
            break
        index += 1
    return index





















#Runs program
window.mainloop()