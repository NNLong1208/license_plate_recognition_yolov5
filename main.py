import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from lisence_plate_recognition import *
from store import *
import time

def load_img():
    global img, image_data
    for img_display in frame.winfo_children():
        img_display.destroy()

    image_data = filedialog.askopenfilename(initialdir=r"C:\Users\nguye\Desktop\Detai", title="Choose an image",
                                       filetypes=(("all files", "*.*"), ("png files", "*.png")))
    basewidth = 400 # Processing image for dysplaying
    img = Image.open(image_data)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    file_name = image_data.split('/')
    panel = tk.Label(frame, text= str(file_name[len(file_name)-1]).upper()).pack()
    panel_image = tk.Label(frame, image=img).pack()

def classify():
    global img

    img = cv2.imread(image_data)
    time_start = time.time()
    label = model.predict(img)
    time_end = time.time()
    store_data(label)
    time_in, time_out = get_data(label)
    if time_in != None:
        time_in = time_in.strftime("%Y-%m-%d %H:%M:%S")
    if time_out != None:
        time_out = time_out.strftime("%Y-%m-%d %H:%M:%S")

    tk.Label(frame, text="Lisence plate").pack()
    result = tk.Label(frame, text= str(label) )#+  "\n Time in: {} \n Time out: {}".format(time_in, time_out))

    result.pack()
    result.config(font=('Helvatical bold',15))

model = lisence_plate_recognition()
root = tk.Tk()
root.title('Lisence plate recognition')
#root.iconbitmap('class.ico')
root.resizable(False, False)
tit = tk.Label(root, text="Nguyen Ngoc Long", padx=25, pady=6, font=("", 12)).pack()
canvas = tk.Canvas(root, height=500, width=500, bg='grey')
canvas.pack()
frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
chose_image = tk.Button(root, text='Choose Image',
                        padx=35, pady=10,
                        fg="white", bg="grey", command=load_img)
chose_image.pack(side=tk.LEFT)
class_image = tk.Button(root, text='Classify Image',
                        padx=35, pady=10,
                        fg="white", bg="grey", command=classify)
class_image.pack(side=tk.RIGHT)
root.mainloop()