'''----------------------------------------IMPORTS----------------------------------------'''
import webbrowser
import tkinter as tk
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import struct
import serial
import time
# SHOW THE PATH OF FILE 
# WE NEED IT FOR THE PATHES
ASSETS_PATH = Path(__file__).resolve().parent / "assets"


#connect python to arduino with the maximum baudrate
ser = serial.Serial('COM15', 115200, timeout=.1)

'''----------------------------------------METHODS----------------------------------------'''
#SHOW VALUES WHEN WE CLICK 
flag = False
def btn_clicked():
    global flag
    print("KP :",float(kp.get()))   
    print("KI :",ki.get())
    print("KD :",kd.get())
    #print( type(kp.get()))
    value = int( float(kp.get()) * 10) 

    ser.write(struct.pack('>B', value ) ) #interpret bytes as packed binary data( conversions between python and c struct)
    flag = True


# Redirect YOU TO THE LINK
def know_more_clicked():
    instructions = ("https://www.facebook.com/")
    webbrowser.open_new_tab(instructions)

'''----------------------------------------MONITORING----------------------------------------'''
index = count()
c = 0
x = []
y = []
def animate(i):
    global c
    global flag

    if ( flag == True):
        while ( ser.in_waiting == 0 ):
            pass
        data = str(ser.readline())
        #print(data)
        new_data = data.split("'")  #split string
        print(new_data)
        if ( new_data[1][:-4] ):  
               #eleminate lest 4 elements
            data_plt = float(new_data[1][:-4])   # convert it to float
            x.append(next(index))
            y.append(data_plt)
            plt.cla()    #make it one colour
            plt.plot(x,y)
            plt.xlim(0+c -4  ,10 +c -4)   
            plt.ylim(0,5.0)    # set limits
            c=c+1  
            
'''------------------------------------APP COLOR------------------------------------'''
color="#b13af6"


'''------------------------------------FRAME CREATION------------------------------------'''
window = tk.Tk()
window.title("Ras Insat")
window.geometry("862x519")
window.configure(bg=color)




'''------------------------------------CANVA CREATION------------------------------------'''
canvas = tk.Canvas(window, bg=color, height=519, width=862)
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 862,  519, fill="#FFFFFF")


'''------------------------------------FORM PART ------------------------------------'''
#LITTLE TITLE
canvas.create_text(650.0, 100.0, text="Put Your Parameters", fill="#000000",font=("Arial-BoldMT",20))

#KP 
canvas.create_text(502.0, 156.0, text="KP", fill="#515486",font=("Arial-BoldMT",13))
kp = tk.Entry(bd=0, bg=color)
kp.place(x=490, y=167, width=321.0, height=50)

#KI
canvas.create_text(500.0, 234.5, text="KI", fill="#515486",font=("Arial-BoldMT", 13))
ki = tk.Entry(bd=0, bg=color)
ki.place(x=490, y=248, width=321.0, height=50)

#KD
canvas.create_text(502.0, 315.5, text="KD",fill="#515486", font=("Arial-BoldMT", 13))
kd = tk.Entry(bd=0, bg=color)
kd.place(x=490, y=329, width=321, height=50)

#Generate Button
generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0, cursor="hand2",
    command=btn_clicked)
generate_btn.place(x=557, y=401, width=180, height=55)


'''------------------------------------PAGE PART------------------------------------'''
#title
title = tk.Label(text="Welcome to RAS INSAT", bg=color,fg="white", font=("Arial-BoldMT",20))
title.place(x=27.0, y=20.0)

#Logo 
logo_image= tk.PhotoImage(file=ASSETS_PATH / "logo.png")
logo = tk.Label(image=logo_image, borderwidth=0, highlightthickness=0,background=color)
logo.place(x=10, y=80, width=390, height=190)

#INFO
info_text = tk.Label(
    text="This is our costomized app \n"
    "which will generate kp, ki and\n"
    "kd value.",
    bg=color, fg="white", justify="left",
    font=("Georgia",16))
info_text.place(x=27.0, y=300)


#HREF
know_more = tk.Button(text="Click here for instructions",bg=color, fg="white", cursor="hand2",command=know_more_clicked)
know_more.place(x=27, y=400)



#CREATION APP
window.resizable(False, False)
ani = FuncAnimation(plt.gcf(),animate, interval = 1) 
plt.show()
window.mainloop()
