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

                # URL FOR THE GET REQUEST
                url = "http://127.0.0.1:8000/exercises/" + f"{username}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # SEND THE GET REQUEST
                response = requests.get(url, headers=headers)

                # PROCESS THE RESPONSE
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

            # LIST EXERCISES LISTBOX
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

                # URL FOR THE DELETE METHOD
                url = "http://127.0.0.1:8000/exercises/delete/" + f"{username}/" + f"{exercise}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # SEND THE DELETE REQUEST
                response = requests.delete(url, headers=headers)

                # PROCESS THE RESPONSE
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

            delete_exercise_name_label = tk.Label(frame, font=("Segue UI Light", 15, "bold"), bg='white',
                                                  text='Exercise name:')
            delete_exercise_name_label.grid(row=0, column=0, sticky='nsew')
            delete_exercise_name_entry = tk.Entry(frame, bg='white')
            delete_exercise_name_entry.grid(row=0, column=1, sticky='nsew')

            delete_exercise_button = tk.Button(frame, text="Delete the exercise",
                                               font=('Segue UI Light', 15),
                                               fg='white', command=delete_exercise_action,
                                               bg="orange", relief=tk.RAISED)
            delete_exercise_button.grid(row=1, column=0, columnspan=2, sticky='nsew')

            delete_exercise_response_label = tk.Label(frame, font=("Segue UI Light", 15, "bold"))
            delete_exercise_response_label.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # TODO: Retrieve/update menu
        def retrieve_update_exercise():

            def retrieve_update_exercise_action():
                global access_token
                global username
                old_exercise = old_name_entry.get()
                new_exercise = new_name_entry.get()
                new_exercise_type = new_type.get()
                if old_exercise and new_exercise:
                    # URL for the PATCH request
                    url = "http://127.0.0.1:8000/exercises/" + f"{username}/" + f"{old_exercise}/"
                    data = {"name": new_exercise}
                    headers = {"Authorization": f"Bearer {access_token}"}

                    # Send the PATCH request
                    response = requests.patch(url, data=data, headers=headers)

                    # Process the response
                    if response.status_code == 200:
                        response_data = response.json()
                        response_message = response_data['Message']
                        retrieve_update_exercise_response_label.configure(text=response_message, fg="green")
                    else:
                        response_data = response.json()
                        print_text = f"{response_data['detail']}"
                        retrieve_update_exercise_response_label.configure(text=print_text, fg="red")

                elif old_exercise and new_exercise and new_exercise_type:
                    # URL for the PATCH request
                    url = "http://127.0.0.1:8000/exercises/" + f"{username}/" + f"{old_exercise}/"
                    data = {"name": new_exercise, 'exercise_type': new_exercise_type}
                    headers = {"Authorization": f"Bearer {access_token}"}

                    # SEND THE PATCH REQUEST
                    response = requests.patch(url, data=data, headers=headers)

                    # PROCESS THE RESPONSE
                    if response.status_code == 200:
                        response_data = response.json()
                        response_message = response_data['Message']
                        retrieve_update_exercise_response_label.configure(text=response_message, fg="green")
                    else:
                        response_data = response.json()
                        print_text = f"{response_data['detail']}"
                        retrieve_update_exercise_response_label.configure(text=print_text, fg="red")

                elif old_exercise and (new_exercise_type != "Nothing"):
                    # URL FOR THE PATCH REQUEST
                    url = "http://127.0.0.1:8000/exercises/" + f"{username}/" + f"{old_exercise}/"
                    data = {'exercise_type': new_exercise_type}
                    headers = {"Authorization": f"Bearer {access_token}"}

                    # SEND THE PATCH REQUEST
                    response = requests.patch(url, data=data, headers=headers)

                    # PROCESS THE RESPONSE
                    if response.status_code == 200:
                        response_data = response.json()
                        response_message = response_data['Message']
                        retrieve_update_exercise_response_label.configure(text=response_message, fg="green")
                    else:
                        response_data = response.json()
                        print_text = ""
                        for key, value in response_data.items():
                            print_text += f"{key}: {str(value)}" + "\n"
                        retrieve_update_exercise_response_label.configure(text=print_text, fg="red")

                elif old_exercise and new_exercise_type == "Nothing":
                    # URL for the PATCH request
                    url = "http://127.0.0.1:8000/exercises/" + f"{username}/" + f"{old_exercise}/"
                    headers = {"Authorization": f"Bearer {access_token}"}

                    # Send the POST request
                    response = requests.patch(url, headers=headers)

                    # Process the response
                    if response.status_code == 200:
                        response_data = response.json()
                        response_message = response_data['Data']
                        text = {}
                        text['Exercise name'] = response_message['name']
                        text['Exercise type'] = response_message['exercise_type']
                        print_text = f"Exercise name: {text['Exercise name']}" + "\n" + f"Exercise type: {text['Exercise type']}"
                        retrieve_update_exercise_response_label.configure(text=print_text, fg="green")
                    else:
                        response_data = response.json()
                        print_text = ""
                        for key, value in response_data.items():
                            print_text += f"{key}: {str(value)}" + "\n"
                        retrieve_update_exercise_response_label.configure(text=print_text, fg="red")

            retrieve_update_exercise_window = new_window('Retrieve or update a specific exercise !', 'zoomed', 'orange')
            retrieve_update_exercise_label = tk.Label(retrieve_update_exercise_window,
                                                      text="Retrieve/Update a specific exercise:",
                                                      font=("Segue UI Light", 45, "bold"),
                                                      fg='white', bg='orange')
            retrieve_update_exercise_label.place(relx=0.50, rely=0.10, anchor=tk.CENTER)

            # CREATE RETRIEVE/UPDATE EXERCISES GRID (3X3)
            for u in range(3):
                retrieve_update_exercise_window.rowconfigure(u, weight=1)
                retrieve_update_exercise_window.columnconfigure(u, weight=1)

            frame = tk.Frame(retrieve_update_exercise_window, bg='orange')
            frame.grid(row=1, column=1, rowspan=2, sticky='nsew')

            for f in range(2):
                frame.columnconfigure(f, weight=1)

            old_name_label = tk.Label(frame, text='Old exercise name', font=("Segue UI Light", 15, "bold"))
            old_name_label.grid(row=0, column=0, sticky='nsew')

            old_name_entry = tk.Entry(frame, bg='white')
            old_name_entry.grid(row=0, column=1, sticky='nsew')

            new_name_label = tk.Label(frame, text='New exercise name', font=("Segue UI Light", 15, "bold"))
            new_name_label.grid(row=1, column=0, sticky='nsew')

            new_name_entry = tk.Entry(frame, bg='white')
            new_name_entry.grid(row=1, column=1, sticky='nsew')

            new_type_label = tk.Label(frame, text='New exercise type', font=("Segue UI Light", 15, "bold"))
            new_type_label.grid(row=2, column=0, sticky='nsew')

            new_types = ['Nothing', 'Technique', 'Cardio', 'Strength']
            new_type = tk.StringVar()
            new_exercise_type_menu = tk.OptionMenu(frame, new_type, *new_types)
            new_exercise_type_menu.grid(row=2, column=1, sticky='nsew')

            retrieve_update_button = tk.Button(frame, text="Retrieve/Update the exercise",
                                               font=('Segue UI Light', 15),
                                               fg='white', command=retrieve_update_exercise_action,
                                               bg="orange", relief=tk.RAISED)
            retrieve_update_button.grid(row=3, column=0, columnspan=2, sticky='nsew')

            retrieve_update_exercise_response_label = tk.Label(frame, font=("Segue UI Light", 15))
            retrieve_update_exercise_response_label.grid(row=4, column=0, columnspan=2, sticky='nsew')

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

    # TODO: MANAGE TRAININGS MENU
    def manage_trainings():
        global access_token
        window_manage_trainings = new_window('Permit an action with your trainings !', 'zoomed', 'orange')
        trainings_action_label = tk.Label(window_manage_trainings,
                                          text="What kind of action \n do you want to perform to your trainings?",
                                          font=("Segue UI Light", 45, "bold"),
                                          fg='white', bg='orange')
        trainings_action_label.place(relx=0.50, rely=0.1, anchor=tk.CENTER)

        # TODO: CREATE TRAINING MENU
        def create_training():
            global username
            create_training_window = new_window('Create your training !', 'zoomed', 'orange')
            create_training_label = tk.Label(create_training_window,
                                             text="Create your training !",
                                             font=("Segue UI Light", 45, "bold"),
                                             fg='white', bg='orange')
            create_training_label.place(relx=0.50, rely=0.1, anchor=tk.CENTER)

            def create_training_action():
                exercise = exercise_entry.get()
                quantity_type_ = quantity_type.get()
                quantity = quantity_entry.get()
                time_type_ = time_type.get()
                repetitions = repetitions_entry.get()
                global username
                global access_token

                if quantity_type_ == 'Sets':
                    # URL for the POST request
                    url = "http://127.0.0.1:8000/training/create/"
                    data = {"username": username, "exercise": exercise, 'quantity_type': quantity_type_,
                            "quantity": quantity, "repetitions": repetitions}
                    headers = {"Authorization": f"Bearer {access_token}"}

                    # Send the POST request
                    response = requests.post(url, data=data, headers=headers)

                    # Process the response
                    if response.status_code == 201:
                        response_data = response.json()
                        response_message = response_data['Message']
                        listbox.insert(tk.END, response_message)

                    else:
                        response_data = response.json()
                        response_message = response_data['Message']
                        listbox.insert(tk.END, response_message)


                elif quantity_type_ == 'Time':
                    # URL for the POST request
                    url = "http://127.0.0.1:8000/training/create/"
                    data = {"username": username, "exercise": exercise, 'quantity_type': quantity_type_,
                            "quantity": quantity, "time_type": time_type_}
                    headers = {"Authorization": f"Bearer {access_token}"}

                    # Send the POST request
                    response = requests.post(url, data=data, headers=headers)

                    # Process the response
                    if response.status_code == 201:
                        response_data = response.json()
                        response_message = response_data['Message']
                        listbox.insert(tk.END, response_message)
                    else:
                        response_data = response.json()
                        response_message = response_data['Message']
                        listbox.insert(tk.END, response_message)

            # CREATE TRAINING MENU GRID (3X3)
            for i in range(4):
                create_training_window.rowconfigure(i, weight=1)
                create_training_window.columnconfigure(i, weight=1)

            # CREATE TRAINING MENU LAYOUT
            create_form_frame = tk.Frame(create_training_window, bg='orange')
            create_form_frame.grid(row=2, column=1, rowspan=2, sticky='nsew')

            # CREATE TRAINING FORM GRID
            for m in range(7):
                create_form_frame.rowconfigure(m, weight=1)
            for n in range(2):
                create_form_frame.columnconfigure(n, weight=1)

            exercise_label = tk.Label(create_form_frame, text="Exercise name:",
                                      font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            exercise_label.grid(row=0, column=0, sticky='nsew')

            exercise_entry = tk.Entry(create_form_frame, bg='white')
            exercise_entry.grid(row=0, column=1, sticky='nsew')

            response_frame = tk.Frame(create_training_window, bg='white')
            response_frame.grid(row=2, column=2, rowspan=2, sticky='nsew')

            listbox = tk.Listbox(response_frame)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(response_frame, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

            def on_first_option_select(*args):
                selected_option = quantity_type.get()
                if selected_option == "Time":
                    time_type_menu["state"] = "normal"
                    time_type_menu.grid(row=3, column=1, sticky='nsew')
                    time_type_label.grid(row=3, column=0, sticky='nsew')
                    repetitions_label.grid_forget()
                    repetitions_entry.grid_forget()
                    create_button.grid(row=4, columnspan=2, column=0, sticky='nsew')
                else:
                    time_type_menu["state"] = "disabled"
                    time_type_label.grid_remove()
                    repetitions_label.grid(row=3, column=0, sticky='nsew')
                    repetitions_entry.grid(row=3, column=1, sticky='nsew')
                    create_button.grid(row=4, columnspan=2, column=0, sticky='nsew')

            for j in range(3):  # Adjusted the range here
                create_form_frame.rowconfigure(j, weight=1)
            for m in range(2):
                create_form_frame.columnconfigure(m, weight=1)

            quantity_type_label = tk.Label(create_form_frame, text="Quantity type:",
                                           font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            quantity_type_label.grid(row=1, column=0, sticky='nsew')

            quantity_type = tk.StringVar()
            quantity_type_menu = tk.OptionMenu(create_form_frame, quantity_type, "Sets", "Time")
            quantity_type_menu.grid(row=1, column=1, sticky='nsew')

            quantity_label = tk.Label(create_form_frame, text='Quantity',
                                      font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            quantity_label.grid(row=2, column=0, sticky='nsew')

            quantity_entry = tk.Entry(create_form_frame, bg='white')
            quantity_entry.grid(row=2, column=1, sticky='nsew')

            time_type = tk.StringVar()
            time_type_menu = tk.OptionMenu(create_form_frame, time_type, "Hours", "Minutes", "Seconds")
            time_type_menu["state"] = "disabled"

            time_type_label = tk.Label(create_form_frame, text='Time type',
                                       font=("Segue UI Light", 15, "bold"), fg='black', bg='white')

            create_button = tk.Button(create_form_frame, text="Create the training",
                                      font=('Segue UI Light', 30, 'bold'), command=create_training_action,
                                      fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)

            repetitions_label = tk.Label(create_form_frame, text='Number of repetitions per set',
                                         font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            repetitions_entry = tk.Entry(create_form_frame, bg='white')

            quantity_type.trace("w", on_first_option_select)

        def list_trainings():
            global access_token
            global username
            list_trainings_window = new_window('Get a long list of all your trainings !', 'zoomed', 'orange')
            list_trainings_label = tk.Label(list_trainings_window,
                                            text="Get a long list of all your trainings !",
                                            font=("Segue UI Light", 45, "bold"),
                                            fg='white', bg='orange')
            list_trainings_label.place(relx=0.50, rely=0.1, anchor=tk.CENTER)

            # TODO: LIST TRAININGS MENU
            def list_trainings_action():
                global username
                global access_token

                # URL for the GET request
                url = "http://127.0.0.1:8000/training/" + f"{username}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the GET request
                response = requests.get(url, headers=headers)

                # Process the response
                if response.status_code == 200:
                    response_data = response.json().get('Data', [])
                    response_message = response.json().get('Message', '')

                    for item in response_data:
                        for key, value in item.items():
                            if key == 'username':
                                pass
                            else:
                                if key=='id':
                                    listbox.insert(tk.END, f"Training {key}: {value}")
                                else:
                                    listbox.insert(tk.END, f"{value}")

                        listbox.insert(tk.END, "")

                    listbox.insert(tk.END, "")
                    listbox.insert(tk.END, response_message)
                else:
                    response_message = response.json().get('Message', '')
                    listbox.insert(tk.END, response_message)
                pass

            # LIST EXERCISES GRID (3x3)
            for i in range(3):
                list_trainings_window.columnconfigure(i, weight=1)
                list_trainings_window.rowconfigure(i, weight=1)

            # List exercises listbox
            list_trainings_frame = tk.Listbox(list_trainings_window, bg='orange')
            list_trainings_frame.grid(row=1, column=1, rowspan=1, sticky="nsew")
            list_button_frame = tk.Frame(list_trainings_window, bg='orange')
            list_button_frame.grid(row=2, column=1, rowspan=1, sticky="nsew")
            for g in range(3):
                list_button_frame.rowconfigure(g, weight=1)
            for k in range(1):
                list_button_frame.columnconfigure(k, weight=1)

            list_button = tk.Button(list_button_frame, text="List all your trainings!",
                                    font=('Segue UI Light', 15, 'bold'),
                                    fg='white', command=list_trainings_action,
                                    bg="orange", relief=tk.RAISED)
            list_button.grid(row=0, column=0, sticky='nsew')
            listbox = tk.Listbox(list_trainings_frame)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(list_trainings_frame, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

        # TODO: RETRIEVE TRAINING MENU

        def retrieve_training():

            retrieve_trainings_by_date_window = new_window('Retrieve all trainings in a specific day !', 'zoomed',
                                                           'orange')
            retrieve_trainings_by_date_label = tk.Label(retrieve_trainings_by_date_window,
                                                        text="Retrieve all trainings in a specific day!",
                                                        font=("Segue UI Light", 45, "bold"),
                                                        fg='white', bg='orange')
            retrieve_trainings_by_date_label.place(relx=0.50, rely=0.10, anchor=tk.CENTER)

            def retrieve_trainings_actions():
                global username
                global access_token
                date = date_entry.get()

                # URL for the PATCH request
                url = "http://127.0.0.1:8000/training/" + f"{username}/" + f"{date}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the POST request
                response = requests.get(url, headers=headers)

                # Process the response
                if response.status_code == 200:
                    response_data = response.json().get('Data', [])
                    response_message = response.json().get('Message', '')

                    for item in response_data:
                        for key, value in item.items():
                            if key == 'username':
                                pass
                            else:
                                listbox.insert(tk.END, f"{key}: {value}")
                        listbox.insert(tk.END, "")

                    listbox.insert(tk.END, "")
                    listbox.insert(tk.END, response_message)
                else:
                    response_message = response.json().get('Message', '')
                    listbox.insert(tk.END, response_message)

                pass

            # CREATE RETRIEVE TRAININGS FORM GRID (4X4)
            for u in range(4):
                retrieve_trainings_by_date_window.rowconfigure(u, weight=1)
                retrieve_trainings_by_date_window.columnconfigure(u, weight=1)

            frame_form = tk.Frame(retrieve_trainings_by_date_window, bg='orange')
            frame_form.grid(row=1, column=1, rowspan=2, sticky='nsew')

            for f in range(3):
                frame_form.rowconfigure(f, weight=1)
            for g in range(2):
                frame_form.columnconfigure(g, weight=1)

            date_label = tk.Label(frame_form, text='Date of trainings \n (YYYY-MM-DD format):',
                                  font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            date_label.grid(row=2, column=0, sticky="nsew")

            date_entry = tk.Entry(frame_form, bg="white")
            date_entry.grid(row=2, column=1, sticky="nsew")

            retrieve_trainings_button = tk.Button(frame_form, text="Retrieve",
                                                  font=('Segue UI Light', 30, 'bold'),
                                                  command=retrieve_trainings_actions,
                                                  fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)
            retrieve_trainings_button.grid(row=3, columnspan=2, column=0, sticky="nsew")

            # LISTBOX FRAME
            listbox_frame = tk.Frame(retrieve_trainings_by_date_window, bg='white')
            listbox_frame.grid(row=2, column=2, rowspan=2, sticky="nsew")

            for i in range(3):
                listbox_frame.rowconfigure(i, weight=1)

            listbox = tk.Listbox(listbox_frame)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(listbox_frame, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)

        # TODO: DELETE TRAININGS MENU
        def delete_training():
            delete_trainings_by_id_window = new_window('Delete a training by providing the training ID', 'zoomed',
                                                       'orange')
            delete_trainings_by_id_label = tk.Label(delete_trainings_by_id_window,
                                                    text="Delete a training by providing the training ID",
                                                    font=("Segue UI Light", 45, "bold"),
                                                    fg='white', bg='orange')
            delete_trainings_by_id_label.place(relx=0.50, rely=0.10, anchor=tk.CENTER)

            def delete_training_action():
                global username
                global access_token
                index = id_entry.get()

                # URL for the POST request
                url = "http://127.0.0.1:8000/training/delete/" + f"{username}/" + f"{index}/"
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the GET request
                response = requests.delete(url, headers=headers)

                # Process the response
                if response.status_code == 204:
                    response_message = "Exercise deleted successfully."
                    response_label.configure(text=response_message, fg='green')
                else:
                    try:
                        response_data = response.json()
                        response_message = response_data['Message']
                        response_label.configure(text=response_message, fg='red')
                    except:
                        response_label.configure(text="An error occurred.", fg='red')

            # CREATE DELETE TRAININGS FORM GRID (3X3)
            for u in range(3):
                delete_trainings_by_id_window.rowconfigure(u, weight=1)
                delete_trainings_by_id_window.columnconfigure(u, weight=1)

            frame_form = tk.Frame(delete_trainings_by_id_window, bg='orange')
            frame_form.grid(row=1, column=1, rowspan=2, sticky='nsew')

            # DELETE FRAME LAYOUT
            for r in range(3):
                frame_form.rowconfigure(r, weight=1)
            for p in range(2):
                frame_form.columnconfigure(p, weight=1)

            id_label = tk.Label(frame_form, text='Training ID', font=("Segue UI Light", 15, "bold"), fg='black',
                                bg='white')
            id_label.grid(row=0, column=0, sticky="nsew")

            id_entry = tk.Entry(frame_form, bg='white')
            id_entry.grid(row=0, column=1, sticky='nsew')

            delete_button = tk.Button(frame_form, text="Delete", font=('Segue UI Light', 30, 'bold'),
                                      command=delete_training_action, fg='white', bg="orange",
                                      relief=tk.RAISED, padx=5, pady=5)
            delete_button.grid(row=1, column=0, columnspan=2, sticky='nsew')

            response_label = tk.Label(frame_form, bg='white', font=("Segue UI Light", 15, "bold"))
            response_label.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # TODO: UPDATE TRAINING MENU

        def update_training():
            update_training_window = new_window('Update a specific exercise !', 'zoomed', 'orange')
            update_training_label = tk.Label(update_training_window,
                                             text="Update a specific training:",
                                             font=("Segue UI Light", 45, "bold"),
                                             fg='white', bg='orange')
            update_training_label.place(relx=0.50, rely=0.10, anchor=tk.CENTER)

            def update_training_action():
                global username
                global access_token
                index = id_entry.get()
                exercise_name = exercise_entry.get()
                quantity_type_ = quantity_type.get()
                quantity = quantity_entry.get()
                time = time_type.get()
                repetitions = repetitions_entry.get()

                dic = {"exercise": exercise_name, "quantity_type": quantity_type_,
                       "quantity": quantity, "time_type": time, "repetitions": repetitions}

                # URL for the PATCH request
                url = "http://127.0.0.1:8000/training/update/" + f"{username}/" + f"{index}/"
                data = {}
                for key, value in dic.items():
                    if key and value:
                        data[key]=value
                headers = {"Authorization": f"Bearer {access_token}"}

                # Send the PATCH request
                response = requests.patch(url, data=data, headers=headers)

                # Process the response
                if response.status_code == 200:
                    response_data = response.json()
                    response_message = response_data['Message']
                    response_label.configure(text=response_message, fg="green")
                else:
                    response_data = response.json()
                    response_message = response_data['Message']
                    response_label.configure(text=response_message, fg="red")

            # CREATE TRAINING MENU GRID (3X3)
            for i in range(3):
                update_training_window.rowconfigure(i, weight=1)
                update_training_window.columnconfigure(i, weight=1)

            # UPDATE TRAINING MENU LAYOUT
            update_form_frame = tk.Frame(update_training_window, bg='white')
            update_form_frame.grid(row=1, column=1, rowspan=2, sticky='nsew')

            # CREATE TRAINING FORM GRID
            for m in range(7):
                update_form_frame.rowconfigure(m, weight=1)
            for n in range(2):
                update_form_frame.columnconfigure(n, weight=1)

            id_label = tk.Label(update_form_frame, text="Training ID:",
                                font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            id_label.grid(row=0, column=0, sticky='nsew')

            id_entry = tk.Entry(update_form_frame, bg='white')
            id_entry.grid(row=0, column=1, sticky='nsew')

            exercise_label = tk.Label(update_form_frame, text="Exercise name:",
                                      font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            exercise_label.grid(row=1, column=0, sticky='nsew')

            exercise_entry = tk.Entry(update_form_frame, bg='white')
            exercise_entry.grid(row=1, column=1, sticky='nsew')

            response_label = tk.Label(update_form_frame, bg='white', font=("Segue UI Light", 15, "bold"))
            response_label.grid(row=6, column=0, columnspan=2, sticky='nsew')

            def on_first_option_select(*args):
                selected_option = quantity_type.get()
                if selected_option == "Time":
                    time_type_menu["state"] = "normal"
                    time_type_menu.grid(row=4, column=1, sticky='nsew')
                    time_type_label.grid(row=4, column=0, sticky='nsew')
                    repetitions_label.grid_forget()
                    repetitions_entry.grid_forget()
                    update_button.grid(row=5, columnspan=2, column=0, sticky='nsew')
                else:
                    time_type_menu["state"] = "disabled"
                    time_type_label.grid_remove()
                    repetitions_label.grid(row=4, column=0, sticky='nsew')
                    repetitions_entry.grid(row=4, column=1, sticky='nsew')
                    update_button.grid(row=5, columnspan=2, column=0, sticky='nsew')

            for j in range(3):
                update_form_frame.rowconfigure(j, weight=1)
            for m in range(2):
                update_form_frame.columnconfigure(m, weight=1)

            quantity_type_label = tk.Label(update_form_frame, text="Quantity type:",
                                           font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            quantity_type_label.grid(row=2, column=0, sticky='nsew')

            quantity_type = tk.StringVar()
            quantity_type_menu = tk.OptionMenu(update_form_frame, quantity_type, "Sets", "Time")
            quantity_type_menu.grid(row=2, column=1, sticky='nsew')

            quantity_label = tk.Label(update_form_frame, text='Quantity',
                                      font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            quantity_label.grid(row=3, column=0, sticky='nsew')

            quantity_entry = tk.Entry(update_form_frame, bg='white')
            quantity_entry.grid(row=3, column=1, sticky='nsew')

            time_type = tk.StringVar()
            time_type_menu = tk.OptionMenu(update_form_frame, time_type, "Hours", "Minutes", "Seconds")
            time_type_menu["state"] = "disabled"

            time_type_label = tk.Label(update_form_frame, text='Time type',
                                       font=("Segue UI Light", 15, "bold"), fg='black', bg='white')

            update_button = tk.Button(update_form_frame, text="Update the training",
                                      font=('Segue UI Light', 30, 'bold'), command=update_training_action,
                                      fg='white', bg="orange", relief=tk.RAISED, padx=5, pady=5)

            repetitions_label = tk.Label(update_form_frame, text='Number of repetitions per set',
                                         font=("Segue UI Light", 15, "bold"), fg='black', bg='white')
            repetitions_entry = tk.Entry(update_form_frame, bg='white')

            quantity_type.trace("w", on_first_option_select)

        # MANAGE TRAININGS MENU GRID
        for i in range(3):
            window_manage_trainings.rowconfigure(i, weight=1)
            window_manage_trainings.columnconfigure(i, weight=1)

        # MANAGE TRAININGS LABEL
        button_frame = tk.Frame(window_manage_trainings, bg='white')
        button_frame.grid(row=1, column=1, rowspan=2, sticky='nsew')

        for j in range(2):
            button_frame.columnconfigure(j, weight=1)
        for i in range(7):
            button_frame.rowconfigure(i, weight=1)

        # BUTTONS
        create_training_button = tk.Button(button_frame, text="Create a training",
                                           font=('Segue UI Light', 15),
                                           fg='white', command=create_training,
                                           bg="orange", relief=tk.RAISED)
        create_training_button.grid(row=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        list_trainings_button = tk.Button(button_frame, text="Get a list of your trainings",
                                          font=('Segue UI Light', 15),
                                          fg='white', command=list_trainings,
                                          bg="orange", relief=tk.RAISED)
        list_trainings_button.grid(row=2, columnspan=2, sticky="nsew", padx=10, pady=10)

        retrieve_training_button = tk.Button(button_frame, text="Retrieve a training by a date",
                                             font=('Segue UI Light', 15),
                                             fg='white', command=retrieve_training,
                                             bg="orange", relief=tk.RAISED)
        retrieve_training_button.grid(row=3, columnspan=2, sticky="nsew", padx=10, pady=10)

        delete_training_button = tk.Button(button_frame, text="Delete a training with an index",
                                           font=('Segue UI Light', 15),
                                           fg='white', command=delete_training,
                                           bg="orange", relief=tk.RAISED)
        delete_training_button.grid(row=4, columnspan=2, sticky="nsew", padx=10, pady=10)

        update_training_button = tk.Button(button_frame, text="Update a training with an index",
                                           font=('Segue UI Light', 15),
                                           fg='white', command=update_training,
                                           bg="orange", relief=tk.RAISED)
        update_training_button.grid(row=5, columnspan=2, sticky="nsew", padx=10, pady=10)

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

frame_login_form = tk.Frame(frame_login, bg='#FFFFFF', width=380, height=380)
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
login_status_label.grid(row=5, columnspan=2)

root.mainloop()
