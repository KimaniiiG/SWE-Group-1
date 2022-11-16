from MotionDetection import email_alert

import PySimpleGUI as sg



sg.theme('HotDogStand')

layout = [


        [sg.Text("This is an alert System")],

        [sg.Text("Please enter your email to recive Alerts & Updates")],

        [sg.InputText()],

        [sg.Button("Submit")],

        [sg.Button("Arm Alarm System")]

        ]

window = sg.Window("My Firt Window", layout, size=(1400,600))

while True:
    event, values = window.read()
    if event == "Submit":
        break
    if event == "Arm Alarm System"

window.close()
