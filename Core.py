import tkinter as tk
from tkinter import PhotoImage
import requests
from PIL import Image, ImageTk

#TODO: GLOBAL VARIABLES
access_token = ''


#TODO: MAIN MENU
def login():

    global access_token
    # Get the username and password from the entry fields
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    # Define the URL and data for the POST request
    url = "http://127.0.0.1:8000/auth/login/"  # Replace with your actual URL
    data = {"username": username, "password": password, "email": email}

    # Send the POST request
    response = requests.post(url, data=data)

    # Process the response
    if response.status_code == 200:
        response_data = response.json()
        response_message = response_data['Message']
        response_token = response_data['tokens']['access']
        login_status_label.config(text="Login successful: " + response_message, fg="green")
        access_token = response_token
        window_after_login(str(username), access_token)
    else:
        response = response.json()['Message']
        login_status_label.config(text=response, fg="red")


def register():
    pass


# APP
root = tk.Tk(className="GymXP")
root.configure(bg='white')

# Configure rows and columns of the root grid
for i in range(3):
    root.columnconfigure(i, weight=1)
for j in range(3):
    root.rowconfigure(j, weight=1)

title = tk.Label(root,
                 bg="#FFFFFF",
                 text="Welcome to GymXP!",
                 font=("Arial Bold", 30),
                 fg='#5DADE2')
title.grid(row=0,
           column=0,
           columnspan=3,
           sticky="nsew")


# LOGIN FRAME
frame_login = tk.Frame(root, bg='#FFFFFF')
frame_login.grid(row=1,
                 column=1,
                 sticky="nsew",
                 columnspan=3)

# MAKE 2x1 GRID FOR SIGN IN FORM
for i in range(2):
    frame_login.columnconfigure(i, weight=1)
for j in range(1):
    frame_login.rowconfigure(j, weight=1)

frame_login_image = tk.Frame(frame_login,
                             bg='#FFFFFF',
                             width=280,
                             height=180)
frame_login_image.grid(row=0,
                       column=0,
                       sticky="nsew")
image = PhotoImage(file="physical-education-icon-22.jpg")
image_label = tk.Label(frame_login_image,
                       image=image,
                       bg='#FFFFFF',
                       anchor='center')
image_label.grid(row=0,
                 column=0,
                 sticky="nsew")

frame_login_form = tk.Frame(frame_login,
                            bg='#FFFFFF',
                            width=280,
                            height=180)
frame_login_form.grid(row=0,
                      column=1,
                      sticky="nsew")

username_label = tk.Label(frame_login_form,
                          text="Username:",
                          font=('Segoe UI Light', 15),
                          fg='#000000',
                          bg="#FFFFFF")
username_label.grid(row=0,
                    column=0,
                    sticky="nsew")

username_entry = tk.Entry(frame_login_form,
                          bg="#FFFFFF")
username_entry.grid(row=0,
                    column=1,
                    sticky="nsew")

email_label = tk.Label(frame_login_form,
                       text="Email:",
                       font=('Segoe UI Light', 15),
                       fg='#000000',
                       bg="#FFFFFF")
email_label.grid(row=1,
                 column=0,
                 sticky="nsew")

email_entry = tk.Entry(frame_login_form,
                       bg="#FFFFFF")
email_entry.grid(row=1,
                 column=1,
                 sticky="nsew")

password_label = tk.Label(frame_login_form,
                          text="Password:",
                          font=('Segoe UI Light', 15),
                          fg='#000000',
                          bg="#FFFFFF")
password_label.grid(row=2,
                    column=0,
                    sticky="nsew")

password_entry = tk.Entry(frame_login_form,
                          show="*",
                          bg="#FFFFFF")
password_entry.grid(row=2,
                    column=1,
                    sticky="nsew")

login_button = tk.Button(frame_login_form,
                         text="Login",
                         font=('Segoe UI Light', 15),
                         fg='#5DADE2', command=login,
                         bg="#FFFFFF",
                         relief=tk.RAISED)
login_button.grid(row=3,
                  column=0,
                  columnspan=2,
                  sticky="nsew")

register_label = tk.Label(frame_login_form,
                          text="Don't have an account? Click the Register button!",
                          bg="#FFFFFF")
register_label.grid(row=4,
                    column=0,
                    columnspan=2)

register_button = tk.Button(frame_login_form,
                            text="Register",
                            font=('Segoe UI Light', 15),
                            fg='#5DADE2',
                            command=register,
                            bg="#FFFFFF",
                            relief=tk.RAISED)
register_button.grid(row=5,
                     column=0,
                     columnspan=2,
                     sticky="nsew")

login_status_label = tk.Label(frame_login_form,
                              text="Login successful",
                              fg="black",
                              bg="#FFFFFF")
login_status_label.grid(row=10,
                        columnspan=2)


#TODO: INSIDE MENU

def window_after_login(username, access_token):
    window = tk.Toplevel(root)
    window.title('Welcome to your Gym Experience')
    window.geometry("1920x1080")

    # Configure rows and columns of the window grid
    for m in range(2):
        window.columnconfigure(i, weight=1)
    for n in range(1):
        window.rowconfigure(j, weight=1)

    # CREATE NEW WIDGETS
    welcome_label = tk.Label(window,
                             text=f"Welcome, {username}!",
                             font=("Arial", 16))

    # Load and set the background image using PIL

    exercises_image = ImageTk.PhotoImage("uIXvkD.jpg")
    background_label = tk.Label(window, image=exercises_image, anchor='center')

    '''
    manage_exercises_button = tk.Button(window, text="Manage your exercises",
                                        font=('Segoe UI Light', 30),
                                        fg='#5DADE2',
                                        command=login,
                                        bg=window.cget('background'),
                                        relief=tk.RAISED, anchor='center')

    manage_exercises_button.grid(row=0,
                                 column=0,
                                 columnspan=1,
                                 sticky="nsew")

    manage_trainings_button = tk.Button(window,
                                        text="Manage your trainings",
                                        font=('Segoe UI Light', 30),
                                        fg='#5DADE2',
                                        command=login,
                                        bg=window.cget('background'),
                                        relief=tk.RAISED,
                                        anchor='center')

    manage_trainings_button.grid(row=0,
                                 column=1,
                                 columnspan=1,
                                 sticky="nsew")
                                 '''


root.mainloop()

