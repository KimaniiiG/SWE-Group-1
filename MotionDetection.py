import threading
import winsound
from email.message import EmailMessage
import smtplib
import cv2
import imutils

def retrieve_input():
    global EmailAddress
    EmailAddress = EmailAddressBox.get()


print("Alarm System Started")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0


def email_alert(Subject, body, to):
		msg = EmailMessage()
		msg.set_content(body)
		msg['subject'] = Subject
		msg['to'] = to

		user = "DroneSurvilenceProject@gmail.com"
		msg['from'] = user
		password = "jduhshcgtkyvwplb"

		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(user, password)
		server.send_message(msg)

		server.quit()


def beep_alarm():

	global alarm
	for _ in range(5):
		if not alarm_mode:
			break
		print("ALARM SET OFF")
		email_alert("Motion Detection Warning", "Weird movement", "Kashinplays@gmail.com")
		winsound.Beep(2500,1000)
	alarm = False


while True:

	_, frame = cap.read()
	frame = imutils.resize(frame, width=500)

	if alarm_mode:
		frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

		difference = cv2.absdiff(frame_bw, start_frame)
		threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
		start_frame = frame_bw

		if threshold.sum() > 1000:
			alarm_counter += 1

		else:
			if alarm_counter > 0:
				alarm_counter -= 1

		cv2.imshow("Cam", threshold)
	else:
		cv2.imshow("Cam", frame)

	if alarm_counter > 20:
		if not alarm:
			alarm = True
			threading.Thread(target=beep_alarm).start()

	key_pressed = cv2.waitKey(30)

	if key_pressed == ord("t"):
		alarm_mode = not alarm_mode
		alarm_counter = 0

	if key_pressed == ord("q"):
		alarm_mode = False
		break

cap.release()
cv2.destroyAllWindows()
