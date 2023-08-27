import tkinter as tk
from tkinter import PhotoImage
import requests
from PIL import Image, ImageTk

#TODO: GLOBAL VARIABLES
access_token = ''
email_entry = ''


#TODO: Main menu functions
def login():

    global access_token
    # Get the username and password from the entry fields
    username = username_entry.get()
    password = password_entry.get()

    # URL for the POST request
    url = "http://127.0.0.1:8000/auth/login/"  # Replace with your actual URL
    data = {"username": username, "password": password}

    # Send the POST request
    response = requests.post(url, data=data)

    # Process the response
    if response.status_code == 200:
        response_data = response.json()
        response_message = response_data['Message']
        response_token = response_data['tokens']['access']
        login_status_label.config(text=response_message, fg="green")
        access_token = response_token
        window_after_login(str(username))
    else:
        response = response.json()['Message']
        login_status_label.config(text=response, fg="red")


# TODO: Login menu
def window_after_login(username):
    window = tk.Toplevel(root)
    window.title('Welcome to your Gym Experience')
    window.state('zoomed')

    # Functions
    def manage_exercises():
        global access_token
        window_manage_exercises = tk.Toplevel(root)
        window_manage_exercises.title('Permit an action with your exercises!')
        window_manage_exercises.state('zoomed')

    def manage_trainings():
        global access_token
        window_manage_exercises = tk.Toplevel(root)
        window_manage_exercises.title('Permit an action with your trainings!')
        window_manage_exercises.state('zoomed')

    image_path = "uIXvkD.jpg"
    exercises_image = Image.open(image_path)
    exercises_photo = ImageTk.PhotoImage(exercises_image)

    # Set the background image of the window
    background_label = tk.Label(window, image=exercises_photo)
    background_label.image = exercises_photo
    background_label.place(relwidth=1, relheight=1)  # Cover the whole window

    # Layout
    welcome_label = tk.Label(window, text=f"Welcome, {username}!", font=("Segoe UI Light", 45, "bold"), fg='orange')
    welcome_label.place(relx=0.50, rely=0.05, anchor=tk.CENTER)

    manage_exercises_button = tk.Button(window, text="Manage your exercises", font=('Segoe UI Light', 30), fg='#5DADE2',
                                        command=manage_exercises, relief=tk.SUNKEN, anchor='center')
    manage_exercises_button.place(relx=0.25, rely=0.95, relwidth=0.5, anchor=tk.CENTER)

    manage_trainings_button = tk.Button(window, text="Manage your trainings", font=('Segoe UI Light', 30), fg='#5DADE2',
                                        command=manage_trainings, relief=tk.SUNKEN, anchor='center')
    manage_trainings_button.place(relx=0.75, rely=0.95, relwidth=0.5, anchor=tk.CENTER)


#TODO: Register window
def register_window():
    window = tk.Toplevel(root)
    window.title("Register and try the GymXP app!")
    window.config(background='orange')
    window.state('zoomed')

    # Functions
    def register():

        # Entries
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        # URL for the POST request
        url = "http://127.0.0.1:8000/auth/signup/"  # Replace with your actual URL
        data = {"username": username, "password": password, "email": email}

        # Send the POST request
        response = requests.post(url, data=data)

        # Process the response
        if response.status_code == 200:
            response_data = response.json()
            response_message = response_data['Message']
            register_status_label.config(text=response_message, fg="green")
        else:
            response_message = response.json()['Message']
            register_status_label.config(text=response_message, fg="red")

    # Configure rows and columns of the root grid
    for i in range(3):
        window.columnconfigure(i, weight=1)
    for j in range(3):
        window.rowconfigure(j, weight=1)

    # Fill the form sign
    welcome_label = tk.Label(window, text="Fill the form and enjoy the app!", font=("Segoe UI Light", 45, "bold"), fg='white', bg='orange')
    welcome_label.place(relx=0.50, rely=0.05, anchor=tk.CENTER)

    #Register frame
    register_form = tk.Frame(window, bg='orange')
    register_form.grid(row=1, column=1)

    #Entries
    username_label = tk.Label(register_form, text="Username:", font=('Segoe UI Light', 15), fg='#000000', bg="#FFFFFF")
    username_label.grid(row=0, column=0, sticky="nsew")

    username_entry = tk.Entry(register_form, bg="#FFFFFF")
    username_entry.grid(row=0, column=1, sticky="nsew")

    email_label = tk.Label(register_form, text="Email:", font=('Segoe UI Light', 15), fg='#000000', bg="#FFFFFF")
    email_label.grid(row=1, column=0, sticky="nsew")

    email_entry = tk.Entry(register_form, bg="#FFFFFF")
    email_entry.grid(row=1, column=1, sticky="nsew")

    password_label = tk.Label(register_form, text="Password:", font=('Segoe UI Light', 15), fg='#000000', bg="#FFFFFF")
    password_label.grid(row=2, column=0, sticky="nsew")

    password_entry = tk.Entry(register_form, show="*", bg="#FFFFFF")
    password_entry.grid(row=2, column=1, sticky="nsew")

    register_button = tk.Button(register_form, text="Register", font=('Segoe UI Light', 15), command=register, fg='#5DADE2', bg="#FFFFFF", relief=tk.RAISED)
    register_button.grid(row=3, column=0, columnspan=2, sticky="nsew")

    register_status_label = tk.Label(register_form, fg="black", bg="#FFFFFF")
    register_status_label.grid(row=10, columnspan=2)


#TODO: Startup App

root = tk.Tk(className="GymXP")
root.configure(bg='white')
root.state('zoomed')

# Rows anc columns (3x3)
for i in range(3):
    root.columnconfigure(i, weight=1)
for j in range(3):
    root.rowconfigure(j, weight=1)

title = tk.Label(root, bg="#FFFFFF", text="Welcome to GymXP!", font=("Arial Bold", 30), fg='#5DADE2')
title.grid(row=0, column=0, columnspan=3, sticky="nsew")


# Login frame
frame_login = tk.Frame(root, bg='#FFFFFF')
frame_login.grid(row=1, column=1, sticky="nsew", columnspan=3)

# Grid for the login frame (2x1)
for i in range(2):
    frame_login.columnconfigure(i, weight=1)
for j in range(1):
    frame_login.rowconfigure(j, weight=1)

frame_login_image = tk.Frame(frame_login, bg='#FFFFFF', width=280, height=180)
frame_login_image.grid(row=0, column=0, sticky="nsew")
image = PhotoImage(file="physical-education-icon-22.jpg")
image_label = tk.Label(frame_login_image, image=image, bg='#FFFFFF', anchor='center')
image_label.grid(row=0, column=0, sticky="nsew")

frame_login_form = tk.Frame(frame_login, bg='#FFFFFF', width=280, height=180)
frame_login_form.grid(row=0, column=1, sticky="nsew")

# Entries
username_label = tk.Label(frame_login_form, text="Username:", font=('Segoe UI Light', 15), fg='#000000', bg="#FFFFFF")
username_label.grid(row=0, column=0, sticky="nsew")

username_entry = tk.Entry(frame_login_form, bg="#FFFFFF")
username_entry.grid(row=0, column=1, sticky="nsew")

password_label = tk.Label(frame_login_form, text="Password:", font=('Segoe UI Light', 15), fg='#000000', bg="#FFFFFF")
password_label.grid(row=1, column=0, sticky="nsew")

password_entry = tk.Entry(frame_login_form, show="*", bg="#FFFFFF")
password_entry.grid(row=1, column=1, sticky="nsew")

login_button = tk.Button(frame_login_form, text="Login", font=('Segoe UI Light', 15), fg='#5DADE2', command=login, bg="#FFFFFF", relief=tk.RAISED)
login_button.grid(row=2, column=0, columnspan=2, sticky="nsew")

register_label = tk.Label(frame_login_form, text="Don't have an account? Click the Register button!", bg="#FFFFFF")
register_label.grid(row=3, column=0, columnspan=2)

register_button = tk.Button(frame_login_form, text="Register", font=('Segoe UI Light', 15), fg='#5DADE2', command=register_window, bg="#FFFFFF", relief=tk.RAISED)
register_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

login_status_label = tk.Label(frame_login_form, text="Login successful", fg="black", bg="#FFFFFF")
login_status_label.grid(row=10, columnspan=2)

root.mainloop()

