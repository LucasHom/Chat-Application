import tkinter as tk
import socket
import threading
from tkinter import messagebox

window = tk.Tk()
window.title("Client")
window.resizable(0, 0)

username = ""
topFrame = tk.Frame(window)
nameLabel = tk.Label(topFrame, text="Name:").pack(side=tk.LEFT)

entry_name = tk.Entry(topFrame)
entry_name.pack(side=tk.LEFT)

button_start = tk.Button(topFrame, text="Connect", command=lambda: connect())
button_start.pack(side=tk.LEFT)

topFrame.pack(side=tk.TOP)


displayFrame = tk.Frame(window)
lineLabel = tk.Label(displayFrame, text="********************").pack()

scroll_bar = tk.Scrollbar(displayFrame)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_display = tk.Text(displayFrame, height=20, width=55)
text_display.pack(side=tk.LEFT, fill=tk.Y, padx = (5, 0))
text_display.tag_config("tag_your_message", foreground="blue")
scroll_bar.config(command=text_display.yview)
text_display.config(yscroll=scroll_bar.set, background="#f4f6f7", highlightbackground="grey", state=tk.DISABLED)

displayFrame.pack(side=tk.TOP)

bottomFrame = tk.Frame(window)
text_message = tk.Text(bottomFrame, height=2, width=55)
text_message.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
text_message.config(highlightbackground="grey", state=tk.DISABLED)
text_message.bind("Return", (lambda event: get_chat_message(text_message.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)

def connect():
    global username, client
    if len(entry_name.get()) < 1:
        tk.messagebox.showerror(title="Invalid Name", message="You must enter your first name!")
    else:
        username = entry_name.get()
        connect_to_server(username)


#Network client
client = None
host_adress = "0.0.0.0"
host_port = 8080

def connect_to_server(username):
    global client, host_adress, host_port
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host_adress, host_port))
        client.send(username.encode())

        entry_name.config(state=tk.DISABLED)
        button_start.config(state=tk.DISABLED)
        text_message.config(state=tk.NORMAL)

        #Start a thread to keep receiving messages from the server
        #Do not block the main thread
        threading._start_new_thread(receive_message_from_server, (client, "m"))

    except Exception as e:
        messagebox.showerror(title="Error", message="Cannot connect to host " + host_adress + " at port " + str(host_port) + "\n Please try again later")


def receive_message_from_server(socket, m):
    while True:
        from_server = socket.recv(4096).decode()
        if not from_server:
            break
        #Display message from the server onto the chat window
        text = text_display.get("1.0", tk.END).strip()
        text_display.config(state=tk.NORMAL)
        if len(text) < 1:
            text_display.insert(tk.END, from_server)
        else:
            text_display.insert(tk.END, "\n\n" + from_server)

        text_display.config(state=tk.DISABLED)
        text_display.see(tk.END)

    socket.close()
    window.destroy()

def get_chat_message(message):
    message = message.replace("\n", "")
    text = text_display.get("1.0", tk.END).strip()
    text_display.config(state=tk.NORMAL)
    if len(text) < 1:
        text_display.insert(tk.END, "You: " + message, "Tag your message")
    else:
        text_display.insert(tk.END, "\n\n" + "You: " + message, "Tag your message")
    text_display.config(state=tk.DISABLED)
    send_message_to_server(message)
    text_display.see(tk.END)
    text_message.delete("1.0", tk.END)

def send_message_to_server(message):
    client_message = str(message)
    client.send(client_message.encode())
    if message == "exit":
        client.close()
        window.destroy()
    print("Sending message")

window.mainloop()