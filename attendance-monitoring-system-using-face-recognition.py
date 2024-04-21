import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import cv2
import csv
import os
import numpy as np
import face_recognition

# Function to capture attendance and update CSV file
def capture_attendance():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    f = open(current_date + '.csv', 'w+', newline='')
    lnwriter = csv.writer(f)

    video_capture = cv2.VideoCapture(0)
    present_students = []  # List to store names of present students

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
                if name in students:
                    students.remove(name)
                    present_students.append(name)  # Append name to present students list
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])
                    # Update GUI label with list of present students
                    student_label.config(text="Students Present: " + ", ".join(present_students))

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

    if present_students:
        messagebox.showinfo("Attendance Capture", "Attendance captured successfully!")
    else:
        messagebox.showinfo("Attendance Capture", "No students present!")

    # Start the animation after capturing attendance
    animate_label()

# Function to animate label
def animate_label():
    current_color = student_label.cget("background")
    new_color = "green" if current_color == "white" else "white"
    student_label.config(background=new_color)
    # Schedule the next animation after 500 milliseconds
    root.after(500, animate_label)

# Function to handle hover effect on buttons
def on_enter(e):
    capture_button.config(bg="lightblue")

def on_leave(e):
    capture_button.config(bg="SystemButtonFace")

# Load known face encodings and names
# Example faces (replace these with your own images)
obama_image = face_recognition.load_image_file("Official_portrait_of_Barack_Obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

surendar_image = face_recognition.load_image_file("surendar.jpg")
surendar_face_encoding = face_recognition.face_encodings(surendar_image)[0]

biden_image = face_recognition.load_image_file("Joe_Biden_presidential_portrait.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

sairam_image = face_recognition.load_image_file("sairam.jpg")
sairam_face_encoding = face_recognition.face_encodings(sairam_image)[0]

balaji_image = face_recognition.load_image_file("balaji.jpg")
balaji_face_encoding = face_recognition.face_encodings(balaji_image)[0]

known_face_encoding = [
    obama_face_encoding,
    biden_face_encoding,
    sairam_face_encoding,
    balaji_face_encoding,
    surendar_face_encoding
]

known_faces_names = [
    "obama",
    "biden",
    "sairam",
    "Balaji",
    "surrendar"
]

students = known_faces_names.copy()

# Create Tkinter GUI
root = tk.Tk()
root.title("Attendance Monitoring System")

label = tk.Label(root, text="Click below to capture attendance", font=("Arial", 16))
label.pack(pady=20)

# Capture Attendance button
capture_button = tk.Button(root, text="Capture Attendance", command=capture_attendance)
capture_button.pack(pady=10)
capture_button.bind("<Enter>", on_enter)  # Hover effect
capture_button.bind("<Leave>", on_leave)  # Hover effect

# Add a label to display the list of students present
student_label = tk.Label(root, text="Students Present: None", font=("Arial", 12), background="white")
student_label.pack(pady=10)

root.mainloop()
