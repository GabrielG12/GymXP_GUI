import tkinter as tk
from tkinter import PhotoImage
import requests
from PIL import Image, ImageTk

# TODO: GLOBAL VARIABLES
access_token = ''
email_entry = ''
username = ''


# TODO: Main menu functions
def new_window(title, state, background):
    window = tk.Toplevel(root)
    window.title(title)
    window.configure(bg=str(background))
    window.state(state)
    return window


def login():
    global access_token
    global username
    username = username_entry.get()
    password = password_entry.get()

    # URL for the POST request
    url = "http://127.0.0.1:8000/auth/login/"
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

    # TODO: Manage exercises menu
    def manage_exercises():
        global access_token
        window_manage_exercises = tk.Toplevel(root)
        window_manage_exercises.title('Permit an action with your exercises!')
        window_manage_exercises.state('zoomed')
        window_manage_exercises.configure(bg='orange')

        # TODO: Create an exercise menu
        def create_exercise():
            create_exercise_window = new_window('Create your exercise !', 'zoomed', 'orange')

            def create_exercise_action():
                exercise = exercise_name.get()
                exercise_type = type.get()
                global username
                global access_token

                # URL for the POST request
                url = "http://127.0.0.1:8000/exercises/create/"
                data = {"username": username, "name": exercise, 'exercise_type': exercise_type}
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the POST request
                response = requests.post(url, data=data, headers=headers)

                # Process the response
                if response.status_code == 201:
                    response_data = response.json()
                    response_message = response_data['Message']
                    response_label.configure(text=response_message, fg="green")
                else:
                    response_data = response.json()
                    response_message = response_data['Message']
                    response_label.configure(text=response_message, fg="red")

            # CREATE EXERCISE LABEL
            create_exercise_label = tk.Label(create_exercise_window,
                                             text="Fill the form and create your exercise!",
                                             font=("Segue UI Light", 45, "bold"),
                                             fg='white', bg='orange')
            create_exercise_label.place(relx=0.50, rely=0.15, anchor=tk.CENTER)

            # CREATE EXERCISES GRID (3x3)
            for i in range(3):
                create_exercise_window.columnconfigure(i, weight=1)
                create_exercise_window.rowconfigure(i, weight=1)

            # CREATE EXERCISE FORM
            create_exercise_frame = tk.Frame(create_exercise_window, bg='orange')
            create_exercise_frame.grid(row=1, column=1, rowspan=2, sticky="nsew")
            for j in range(2):
                create_exercise_frame.columnconfigure(j, weight=1)

            exercise_name_label = tk.Label(create_exercise_frame, text="Exercise name:",
                                           font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            exercise_name_label.grid(row=0, column=0, sticky='nsew')
            exercise_name = tk.Entry(create_exercise_frame, bg='white')
            exercise_name.grid(row=0, column=1, sticky='nsew')

            exercise_type_label = tk.Label(create_exercise_frame, text="Exercise type:",
                                           font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            exercise_type_label.grid(row=1, column=0, sticky='nsew')
            types = ['Technique', 'Cardio', 'Strength']
            type = tk.StringVar()
            exercise_type_menu = tk.OptionMenu(create_exercise_frame, type, *types)
            exercise_type_menu.grid(row=1, column=1, sticky='nsew')

            create_button = tk.Button(create_exercise_frame, text="Create the exercise", font=('Segue UI Light', 15),
                                      fg='#5DADE2', command=create_exercise_action,
                                      bg="#FFFFFF", relief=tk.RAISED)
            create_button.grid(row=2, column=0, columnspan=2)

            response_label = tk.Label(create_exercise_frame, font=("Segue UI Light", 15, "bold"), bg='white')
            response_label.grid(row=3, column=0, columnspan=2)

        # TODO: List exercises menu
        def list_exercises():
            def list_exercises_action():
                global username

                # URL for the GET request
                url = "http://127.0.0.1:8000/exercises/" + f"{username}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the GET request
                response = requests.get(url, headers=headers)

                # Process the response
                if response.status_code == 200:
                    response = response.json()
                    response_data = response.get('Data', [])
                    response_message = response.get('Message', '')

                    if response_data:
                        for exercise in response_data:
                            listbox.insert(tk.END, exercise['name'])
                    else:
                        listbox.insert(tk.END, response_message)
                else:
                    response_data = response.json()
                    response_message = response_data.get('Message', '')
                    listbox.insert(tk.END, response_message)

            list_exercises_window = new_window('These are the exercises you have created :', 'zoomed', 'orange')
            list_exercises_window_label = tk.Label(list_exercises_window, bg='orange',
                                                   font=("Segue UI Light", 45, "bold"), fg='white',
                                                   text='These are the exercises you have created :')
            list_exercises_window_label.place(relx=0.50, rely=0.15, anchor=tk.CENTER)

            # CREATE EXERCISES GRID (3x3)
            for i in range(3):
                list_exercises_window.columnconfigure(i, weight=1)
                list_exercises_window.rowconfigure(i, weight=1)

            # List exercises listbox
            list_exercise_frame = tk.Listbox(list_exercises_window, bg='orange')
            list_exercise_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
            list_button_frame = tk.Frame(list_exercises_window, bg='orange')
            list_button_frame.grid(row=2, column=1, rowspan=1, sticky="nsew")
            for g in range(3):
                list_button_frame.rowconfigure(g, weight=1)
            for k in range(1):
                list_button_frame.columnconfigure(k, weight=1)
            list_button = tk.Button(list_button_frame, text="List all your exercises!",
                                    font=('Segue UI Light', 15, 'bold'),
                                    fg='white', command=list_exercises_action,
                                    bg="orange", relief=tk.RAISED)
            list_button.grid(row=0, column=0, sticky='nsew')
            listbox = tk.Listbox(list_exercise_frame)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(list_exercise_frame, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

        # TODO: Delete exercises menu
        def delete_exercise():

            def delete_exercise_action():
                exercise = delete_exercise_name_entry.get()
                global username
                global access_token

                # URL for the POST request
                url = "http://127.0.0.1:8000/exercises/delete/" + f"{username}/" + f"{exercise}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the GET request
                response = requests.delete(url, headers=headers)

                # Process the response
                if response.status_code == 204:
                    response = response.json()
                    response_message = response['Data']
                    delete_exercise_response_label.configure(text=response_message, fg='green')
                else:
                    response_data = response.json()
                    response_message = response_data['Message']
                    delete_exercise_response_label.configure(text=response_message, fg='red')

            delete_exercise_window = new_window('Delete a specific exercise !', 'zoomed', 'orange')
            delete_exercise_label = tk.Label(delete_exercise_window,
                                             text="Delete a specific exercise:",
                                             font=("Segue UI Light", 45, "bold"),
                                             fg='white', bg='orange')
            delete_exercise_label.place(relx=0.50, rely=0.10, anchor=tk.CENTER)

            # CREATE DELETE EXERCISES GRID (3X3)
            for z in range(3):
                delete_exercise_window.rowconfigure(z, weight=1)
                delete_exercise_window.columnconfigure(z, weight=1)

            # DELETE EXERCISES LAYOUT
            frame = tk.Frame(delete_exercise_window, bg='orange', width=100, height=100)
            frame.grid(row=1, column=1, rowspan=2, sticky='nsew')

            for m in range(2):
                frame.columnconfigure(m, weight=1)

            delete_exercise_name_label = tk.Label(frame, font=("Segue UI Light", 15, "bold"), bg='white', text='Exercise name:')
            delete_exercise_name_label.grid(row=0, column=0, sticky='nsew')
            delete_exercise_name_entry = tk.Entry(frame, bg='white')
            delete_exercise_name_entry.grid(row=0, column=1, sticky='nsew')

            delete_exercise_button = tk.Button(frame, text="Delete the exercise",
                                               font=('Segue UI Light', 15),
                                               fg='white', command=delete_exercise_action,
                                               bg="orange", relief=tk.RAISED)
            delete_exercise_button.grid(row=1, column=0, columnspan=2, sticky='nsew')

            delete_exercise_response_label = tk.Label(frame, font=("Segue UI Light", 15, "bold"))
            delete_exercise_response_label.grid(row=2, column=0,columnspan=2, sticky='nsew')

        # TODO: Retrieve/update menu
        def retrieve_update_exercise():
            retrieve_update_exercise_window = new_window('Retrieve or update a specific exercise !', 'zoomed', 'orange')

        # TODO: Manage exercises menu continued

        # EXERCISES ACTION LABEL
        exercises_action_label = tk.Label(window_manage_exercises,
                                          text="What kind of action \n do you want to perform to your exercises?",
                                          font=("Segue UI Light", 45, "bold"),
                                          fg='white', bg='orange')
        exercises_action_label.place(relx=0.50, rely=0.15, anchor=tk.CENTER)

        # CONFIG ROWS AND COLS
        for i in range(4):
            window_manage_exercises.columnconfigure(i, weight=1)
            window_manage_exercises.rowconfigure(i, weight=1)

        # MANAGE EXERCISES LAYOUT
        create_button = tk.Button(window_manage_exercises, text="Create an exercise",
                                  font=('Segue UI Light', 30, 'bold'), command=create_exercise,
                                  fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)
        create_button.grid(row=2, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        get_button = tk.Button(window_manage_exercises, text="Get a list of your exercises",
                               font=('Segue UI Light', 30, 'bold'), command=list_exercises,
                               fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)
        get_button.grid(row=3, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        delete_button = tk.Button(window_manage_exercises, text="Delete an exercise",
                                  font=('Segue UI Light', 30, 'bold'), command=delete_exercise,
                                  fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)
        delete_button.grid(row=2, column=2, rowspan=1, columnspan=3, sticky="nsew", padx=10, pady=10)

        retrieve_update_button = tk.Button(window_manage_exercises, text="Update/Retrieve an exercise",
                                           font=('Segue UI Light', 30, 'bold'), command=retrieve_update_exercise,
                                           fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)
        retrieve_update_button.grid(row=3, column=2, rowspan=1, columnspan=3, sticky="nsew", padx=10, pady=10)

    def manage_trainings():
        global access_token
        window_manage_exercises = tk.Toplevel(root)
        window_manage_exercises.title('Permit an action with your trainings!')
        window_manage_exercises.state('zoomed')

    # After login menu layout
    image_path = "uIXvkD.jpg"
    exercises_image = Image.open(image_path)
    exercises_photo = ImageTk.PhotoImage(exercises_image)

    # Set the background image of the window
    background_label = tk.Label(window, image=exercises_photo)
    background_label.image = exercises_photo
    background_label.place(relwidth=1, relheight=1)

    # Layout
    welcome_label = tk.Label(window, text=f"Welcome, {username}!", font=("Segue UI Light", 45, "bold"), fg='orange')
    welcome_label.place(relx=0.50, rely=0.05, anchor=tk.CENTER)

    manage_exercises_button = tk.Button(window, text="Manage your exercises", font=('Segue UI Light', 30), fg='#5DADE2',
                                        command=manage_exercises, relief=tk.SUNKEN, anchor='center')
    manage_exercises_button.place(relx=0.25, rely=0.95, relwidth=0.5, anchor=tk.CENTER)

    manage_trainings_button = tk.Button(window, text="Manage your trainings", font=('Segue UI Light', 30), fg='#5DADE2',
                                        command=manage_trainings, relief=tk.SUNKEN, anchor='center')
    manage_trainings_button.place(relx=0.75, rely=0.95, relwidth=0.5, anchor=tk.CENTER)


# TODO: Register window
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

    # FILL THE FORM SIGN
    welcome_label = tk.Label(window, text="Fill the form and enjoy the app!", font=("Segue UI Light", 45, "bold"),
                             fg='white', bg='orange')
    welcome_label.place(relx=0.50, rely=0.05, anchor=tk.CENTER)

    # REGISTER FRAME
    register_form = tk.Frame(window, bg='orange')
    register_form.grid(row=1, column=1)

    # ENTRIES
    username_label = tk.Label(register_form, text="Username:", font=('Segue UI Light', 15), fg='#000000', bg="#FFFFFF")
    username_label.grid(row=0, column=0, sticky="nsew")

    username_entry = tk.Entry(register_form, bg="#FFFFFF")
    username_entry.grid(row=0, column=1, sticky="nsew")

    email_label = tk.Label(register_form, text="Email:", font=('Segue UI Light', 15), fg='#000000', bg="#FFFFFF")
    email_label.grid(row=1, column=0, sticky="nsew")

    email_entry = tk.Entry(register_form, bg="#FFFFFF")
    email_entry.grid(row=1, column=1, sticky="nsew")

    password_label = tk.Label(register_form, text="Password:", font=('Segue UI Light', 15), fg='#000000', bg="#FFFFFF")
    password_label.grid(row=2, column=0, sticky="nsew")

    password_entry = tk.Entry(register_form, show="*", bg="#FFFFFF")
    password_entry.grid(row=2, column=1, sticky="nsew")

    register_button = tk.Button(register_form, text="Register", font=('Segue UI Light', 15), command=register,
                                fg='#5DADE2', bg="#FFFFFF", relief=tk.RAISED)
    register_button.grid(row=3, column=0, columnspan=2, sticky="nsew")

    register_status_label = tk.Label(register_form, fg="black", bg="#FFFFFF")
    register_status_label.grid(row=10, columnspan=2)


# TODO: Startup App

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
username_label = tk.Label(frame_login_form, text="Username:", font=('Segue UI Light', 15), fg='#000000', bg="#FFFFFF")
username_label.grid(row=0, column=0, sticky="nsew")

username_entry = tk.Entry(frame_login_form, bg="#FFFFFF")
username_entry.grid(row=0, column=1, sticky="nsew")

password_label = tk.Label(frame_login_form, text="Password:", font=('Segue UI Light', 15), fg='#000000', bg="#FFFFFF")
password_label.grid(row=1, column=0, sticky="nsew")

password_entry = tk.Entry(frame_login_form, show="*", bg="#FFFFFF")
password_entry.grid(row=1, column=1, sticky="nsew")

login_button = tk.Button(frame_login_form, text="Login", font=('Segue UI Light', 15), fg='#5DADE2', command=login,
                         bg="#FFFFFF", relief=tk.RAISED)
login_button.grid(row=2, column=0, columnspan=2, sticky="nsew")

register_label = tk.Label(frame_login_form, text="Don't have an account? Click the Register button!", bg="#FFFFFF")
register_label.grid(row=3, column=0, columnspan=2)

register_button = tk.Button(frame_login_form, text="Register", font=('Segue UI Light', 15), fg='#5DADE2',
                            command=register_window, bg="#FFFFFF", relief=tk.RAISED)
register_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

login_status_label = tk.Label(frame_login_form, fg="black", bg="#FFFFFF")
login_status_label.grid(row=10, columnspan=2)

root.mainloop()
