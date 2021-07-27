# import
import tkinter as tk
from tkinter import Tk, Radiobutton, Label, Text, Button, messagebox
import socket

# class


class GUI:
    def __init__(self, listens, receive_buffer):
        self.socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listens = listens
        self.status = False
        self.receive_buffer = receive_buffer

        # window
        self.window = Tk()
        self.window.geometry('{}x{}'.format(
            self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.title('Demo GUI')

        # radiobutton
        self.character_radioValue = tk.StringVar()
        self.server_radiobutton = Radiobutton(
            self.window, text='server', variable=self.character_radioValue, value='server')
        self.client_radiobutton = Radiobutton(
            self.window, text='client', variable=self.character_radioValue, value='client')

        # label
        self.character_label = Label(self.window, text='character')
        self.ip_label = Label(self.window, text='ip')
        self.port_label = Label(self.window, text='port')
        self.status_label = Label(self.window, text='')
        self.send_label = Label(self.window, text='send')
        self.receive_label = Label(self.window, text='')

        # text
        self.ip_text = Text(self.window, height=2, width=15)
        self.port_text = Text(self.window, height=2, width=15)
        self.send_data_text = Text(self.window)

        # button
        self.connect = Button(
            self.window, text='check', command=self._connect_ip_port)
        self.send_button = Button(self.window, text='send', command=self._send)

    def _connect_ip_port(self):
        character = self.character_radioValue.get()
        ip = self.ip_text.get(1.0, tk.END+"-1c")
        port = self.port_text.get(1.0, tk.END+"-1c")
        if len(character) > 0 and len(ip) > 0 and len(port) > 0:
            print('{}:{}'.format(ip, port))
            if character == 'server':
                self.status_label['text'] = 'wating'
                self.socket_object.bind((ip, int(port)))
                self.socket_object.listen(self.listens)
                self.client, _ = self.socket_object.accept()
                self.client.send('hi, this is server.'.encode())
                self.client.setblocking(False)
            elif character == 'client':
                self.socket_object.connect((ip, int(port)))
                self.socket_object.setblocking(False)
            self.status = True
            self.status_label['text'] = 'connected'
            self._receive()
        else:
            messagebox.showwarning(
                title='Error!', message='please check character, ip and port!')

    def _send(self):
        send_data = self.send_data_text.get(1.0, tk.END+"-1c")
        send_data = send_data.encode()
        if self.character_radioValue.get() == 'server' and self.status:
            self.client.send(send_data)
        elif self.character_radioValue.get() == 'client' and self.status:
            self.socket_object.send(send_data)

    def _receive(self):
        received_data = ''
        if self.character_radioValue.get() == 'server' and self.status:
            try:
                received_data = self.client.recv(self.receive_buffer)
            except:
                pass
        elif self.character_radioValue.get() == 'client' and self.status:
            try:
                received_data = self.socket_object.recv(self.receive_buffer)
            except:
                pass
        if len(received_data) > 0:
            self.receive_label['text'] = 'your received data:\n{}'.format(
                received_data.decode())
        self.window.after(1000, self._receive)

    def run(self):
        # NW
        self.character_label.pack(anchor=tk.NW)
        self.server_radiobutton.pack(anchor=tk.NW)
        self.client_radiobutton.pack(anchor=tk.NW)
        self.ip_label.pack(anchor=tk.NW)
        self.ip_text.pack(anchor=tk.NW)
        self.port_label.pack(anchor=tk.NW)
        self.port_text.pack(anchor=tk.NW)
        self.connect.pack(anchor=tk.NW)
        self.status_label.pack(anchor=tk.NW)

        # N
        self.send_label.pack(anchor=tk.N)
        self.send_data_text.pack(anchor=tk.N)
        self.send_button.pack(anchor=tk.N)
        self.receive_label.pack(anchor=tk.N)

        # run
        self.window.mainloop()


if __name__ == '__main__':
    # parameters
    listens = 1
    receive_buffer = 100

    # GUI
    gui = GUI(listens=listens, receive_buffer=receive_buffer)
    gui.run()
