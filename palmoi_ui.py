import tkinter as tk
from tkinter import ttk

# Fake data for simulation
machine_locations = [
    [(1.3521, 103.8198), (1.3522, 103.8199), (1.3523, 103.8200), (1.3524, 103.8201)],
    [(1.3525, 103.8202), (1.3526, 103.8203), (1.3527, 103.8204), (1.3528, 103.8205)],
    [(1.3529, 103.8206), (1.3530, 103.8207), (1.3531, 103.8208), (1.3532, 103.8209)]
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated Palm Oil Harvesting Machine : Harvestmate")
        self.geometry("800x600")

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")

        # Initialize containers
        self.container = tk.Frame(self, bg="#a3c1ad")
        self.container.pack(fill="both", expand=True)

        # Show login page
        self.show_frame(LoginPage, self)  # Pass 'self' as the controller argument

    def show_frame(self, page, *args):
        frame = page(self.container, *args)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(bg="#a3c1ad")

        title_label = tk.Label(self, text="Automated Palm Oil Harvesting Machine : Harvestmate", font=("Times New Roman", 24, "bold"), bg="#a3c1ad")
        title_label.pack(pady=20)

        frame = tk.Frame(self, bg="white", padx=20, pady=20)
        frame.pack(pady=20)

        username_label = tk.Label(frame, text="Username:", font=("Times New Roman", 16))
        username_label.grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(frame, font=("Times New Roman", 16))
        self.username_entry.grid(row=0, column=1, pady=10)

        password_label = tk.Label(frame, text="Password:", font=("Times New Roman", 16))
        password_label.grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(frame, show="*", font=("Times New Roman", 16))
        self.password_entry.grid(row=1, column=1, pady=10)

        login_button = tk.Button(frame, text="Login", command=lambda: controller.show_frame(MachineSelectionPage, controller), font=("Times New Roman", 16), bg="#4CAF50", fg="white", padx=20, pady=10)
        login_button.grid(row=2, column=1, pady=10)

class MachineSelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(bg="#a3c1ad")
        self.place(relwidth=1.0, relheight=1.0)  # Set the frame to fill the entire window

        title_label = tk.Label(self, text="Machine Selection", font=("Times New Roman", 24, "bold"), bg="#a3c1ad")
        title_label.place(relx=0.5, rely=0.1, anchor="center")  # Center the title label

        machine_buttons_frame = tk.Frame(self, bg="#a3c1ad")
        machine_buttons_frame.place(relx=0.5, rely=0.4, anchor="center")  # Center the machine buttons frame

        machine_buttons = []
        for i in range(1, 4):
            machine_name = f"Harvestmate {i:02d}"
            button = tk.Button(machine_buttons_frame, text=machine_name, command=lambda m=i: controller.show_frame(HarvestingPage, controller, m-1), font=("Times New Roman", 18), bg="#4CAF50", fg="white", padx=20, pady=20)
            button.pack(pady=10)
            machine_buttons.append(button)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(LoginPage, controller), font=("Times New Roman", 16), bg="#f44336", fg="white", padx=20, pady=20)
        back_button.place(relx=0.5, rely=0.9, anchor="center")  # Center the back button

class HarvestingPage(tk.Frame):
    def __init__(self, parent, controller, machine_index):
        super().__init__(parent)
        self.machine_index = machine_index
        self.config(bg="#a3c1ad")  # Light gray background
        self.place(relwidth=1.0, relheight=1.0)  # Set the frame to fill the entire window

        title_label = tk.Label(self, text=f"Harvestmate {machine_index+1:02d}", font=("Times New Roman", 24, "bold"), bg="#a3c1ad")
        title_label.pack(pady=20)

        button_frame = tk.Frame(self, bg="#a3c1ad")
        button_frame.pack()

        start_harvest_button = tk.Button(button_frame, text="Start Harvest", command=self.activate_details_button, font=("Times New Roman", 18), bg="#4CAF50", fg="white", padx=20, pady=20)
        start_harvest_button.grid(row=0, column=0, padx=10)

        self.details_button = tk.Button(button_frame, text="Harvesting Details", state="disabled", command=lambda: controller.show_frame(HarvestmateDetailsPage, self, machine_index), font=("Times New Roman", 18), bg="#2196F3", fg="white", padx=20, pady=20)
        self.details_button.grid(row=0, column=1, padx=10)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MachineSelectionPage, controller), font=("Times New Roman", 16), bg="#f44336", fg="white", padx=20, pady=20)
        back_button.pack(pady=20)

    def activate_details_button(self):
        self.details_button.config(state="normal")

class HarvestmateDetailsPage(tk.Frame):
    def __init__(self, parent, controller, machine_index):
        super().__init__(parent)
        self.machine_index = machine_index
        self.config(bg="#a3c1ad")  # Light gray background
        self.place(relwidth=1.0, relheight=1.0)  # Set the frame to fill the entire window

        title_label = tk.Label(self, text=f"Harvestmate {machine_index+1:02d} Details", font=("Times New Roman", 24, "bold"), bg="#a3c1ad")
        title_label.pack(pady=20)

        # Create a frame for simulating Harvestmate details
        details_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        details_frame.pack(pady=20)

        # Add labels to display machine details
        location_label = tk.Label(details_frame, text="Current Location:", font=("Times New Roman", 16))
        location_label.grid(row=0, column=0, sticky="w")
        self.location_value = tk.Label(details_frame, text=f"{machine_locations[self.machine_index][0]}", font=("Times New Roman", 16))
        self.location_value.grid(row=0, column=1, sticky="w")

        status_label = tk.Label(details_frame, text="Status:", font=("Times New Roman", 16))
        status_label.grid(row=1, column=0, sticky="w")
        self.status_value = tk.Label(details_frame, text="Harvesting", font=("Times New Roman", 16))
        self.status_value.grid(row=1, column=1, sticky="w")

        # Add a button to simulate location updates
        update_location_button = tk.Button(details_frame, text="Update Location", command=self.update_location, font=("Times New Roman", 14), bg="#4CAF50", fg="white", padx=10, pady=5)
        update_location_button.grid(row=2, column=0, columnspan=2, pady=10)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(HarvestingPage, controller, machine_index), font=("Times New Roman", 16), bg="#f44336", fg="white", padx=20, pady=20)
        back_button.pack(pady=20)

    def update_location(self):
        # Simulate location update by cycling through the list of locations
        current_location_index = machine_locations[self.machine_index].index(eval(self.location_value.cget("text")))
        next_location_index = (current_location_index + 1) % len(machine_locations[self.machine_index])
        next_location = machine_locations[self.machine_index][next_location_index]
        self.location_value.config(text=str(next_location))

if __name__ == "__main__":
    app = App()
    app.mainloop()