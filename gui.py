import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import os, sys, subprocess
from tkinter import colorchooser
from tkinter import messagebox

def check_admin():
    try:
        # Check if the script is already running with admin privileges by executing a simple command
        subprocess.check_call(['pkexec', 'true'])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    if not check_admin():
        # Launch the script with pkexec to acquire root privileges
        subprocess.call(['pkexec', 'python3', __file__])
        return
    else:
        selected_color = [0, 255, 0]
        path = "/sys/devices/platform/asus-nb-wmi/leds/asus::kbd_backlight/kbd_rgb_mode"

        def on_button_click():
            m = mode.get()
            s = speed.get()

            red = str(selected_color[0])
            green = str(selected_color[1])
            blue = str(selected_color[2])

            # Running the bash command that needs root privileges
            bash_command = f'echo "1 {m} {red} {green} {blue} {s}" | tee {path}'

            try:
                # Use pkexec to run the bash command with root privileges
                # This ensures that the authentication is done once via pkexec
                process = subprocess.Popen(
                    ['pkexec', 'bash', '-c', bash_command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    messagebox.showinfo("Success", f"Command executed successfully: {stdout.decode()}")
                else:
                    messagebox.showerror("Error", f"Error executing command: {stderr.decode()}")

            except Exception as e:
                messagebox.showerror("Exception", f"An error occurred: {str(e)}")

        def choose_color(): 
            # variable to store hexadecimal code of color
            color_code = colorchooser.askcolor(title="Choose color") 
            print(color_code)
            if color_code[0]:  # Check if a color was selected
                selected_color[0] = color_code[0][0]
                selected_color[1] = color_code[0][1]
                selected_color[2] = color_code[0][2]
                
                label3.config(text="Chosen color is: "+str(color_code[0]))

        # Create the main window
        win = tk.Tk()
        win.title("ASUS TUF BACKLIGHT CHANGER")
        win.geometry("1000x800")

        ### ADD MODE OF BACKLIGHT ###
        # Add a label
        label1 = tk.Label(win, text="Mode:", font=("Arial", 14))
        label1.pack(pady=20)

        ### Radio button ###
        mode = StringVar(win, "1") 

        options_mode = {
            "Static": "0", 
            "Breathing": "1", 
            "Color Cycle": "2"
        } 

        for (txt, val) in options_mode.items(): 
            Radiobutton(win, text=txt, variable=mode, value=val).pack(side=TOP, ipady=4) 

        ### ADD SPEED OF COLOR ###
        label2 = tk.Label(win, text="Speed:", font=("Arial", 14))
        label2.pack(pady=20)

        speed = StringVar(win, "1") 

        options_speed = {
            "Slow": "0", 
            "Medium": "1", 
            "Fast": "2"
        } 

        for (txt, val) in options_speed.items(): 
            Radiobutton(win, text=txt, variable=speed, value=val).pack(side=TOP, ipady=4) 

        ### CHOOSE COLOR ###
        color_codes = Button(win, text="Select color", command=choose_color)
        color_codes.pack(pady=20)
        
        #Add label
        label3 = tk.Label(win, text="Default color is (0,255,0) i.e. green", font=("Arial", 14))
        label3.pack(pady=20)
        
        ### SUBMIT CONFIG ###
        label4 = tk.Label(win, text="Submit button:", font=("Arial", 14))
        label4.pack(pady=20)

        button = Button(win, text="Submit", command=on_button_click)
        button.pack()

        # Start the Tkinter event loop
        win.mainloop()

if __name__ == "__main__":
    main()

