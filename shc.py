import Tkinter as tk
import serial
import threading
from time import sleep


current = -273.15
desired = -273.15
newdesired = -273.15
abort = False
port = "/dev/ttyUSB0"
isset = False


def setter():
    global isset
    isset = True





root = tk.Tk()
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)
frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
frame3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
frame4.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
frame2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
textbox = tk.Text(root, height=2, width=30)
copyright = tk.Text(root, height=1, width=30)
entryTemp = tk.Entry(root, width=6)
cbox = tk.Text(root, height=1, width=2)
entryPort = tk.Entry(root, width=15)
setbutt = tk.Button(root, text="SET", command=setter)
root.title("V LO HeatBed")
textbox.pack(in_=frame1, side=tk.LEFT, fill=tk.BOTH, expand=True)
entryTemp.pack(in_=frame2, side=tk.LEFT)
cbox.pack(in_=frame2, side=tk.LEFT, expand=True)
entryPort.pack(in_=frame2, side=tk.LEFT)
entryTemp.insert(tk.END, str(desired))
entryPort.insert(tk.END, str(port))
setbutt.pack(in_=frame2, side=tk.LEFT)
copyright.pack(in_=frame3, side=tk.LEFT, fill=tk.BOTH, expand=True)
cbox.insert(tk.END, "C")
copyright.insert(tk.END, "Copyright by Jan Dziedzic 2017")


def aborter():
    global isset, newdesired, abort
    newdesired = -273.15
    entryTemp.delete(0, 'end')
    entryTemp.insert(tk.END, "-273.15")
    abort = True
    isset = True

abortbutt = tk.Button(root, text="ABORT", command=aborter, height=2, width=40)
abortbutt.pack(in_=frame4, side=tk.LEFT)


def serialstuff():
    global current, desired, newdesired, isset, port
    try:
        ser = serial.Serial(port)
    except:
        pass
    while True:
        try:
            ser.reset_input_buffer()
            whatread = ser.readline()
            whatread = whatread.rstrip("\r\n")
            currentS, desiredS = whatread.split(",")
            current = float(currentS)
            desired = float(desiredS)
        except:
            pass
        string2display = ("Current temp: " +
                          str(current) +
                          " C\nDesired temp: " +
                          str(desired) +
                          " C")
        if current == -273.15:
            string2display = "Can't connect\nWrong port?"
        textbox.delete(1.0, tk.END)
        textbox.insert(tk.END, string2display)
        if isset:
            try:
                newdesired = float(entryTemp.get())
                newport = entryPort.get()
            except:
                pass
            if newport != port:
                try:
                    ser.close()
                except:
                    pass
                try:
                    port = newport
                    ser = serial.Serial(port)
                    sleep(0.5)
                except:
                    pass
            if newdesired != desired:
                try:
                    ser.write((str(newdesired) + "\n").encode())
                    print ("Setting transmitted")
                except:
                    pass

            isset = False
        sleep(0.2)

serialThread = threading.Thread(target=serialstuff)
serialThread.daemon = True
serialThread.start()


def guistuff():
    root.mainloop()

guistuff()

