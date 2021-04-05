from tkinter import *
import time
import serial
from bitstring import Bits
import numpy
import matplotlib.pyplot as plt
import random
from scipy.fftpack import fft, fftshift
from scipy.signal import blackman
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#Init
global init_int
init_int = 1
#Relais
global relais_val
global relais_val_old
relais_val = 198
relais_val_old = 198
#ADC
global adc_val
global adc_val_old
adc_val = 26
adc_val_old = 26
#DAC
global amp
global dac_ampval
global dac_ampval_old
amp = 0.0
dac_ampval = 0
dac_ampval_old = 0
global dc_dbl
global dac_dcval
global dac_dcval_old
global DC_offset_arr
DC_offset_arr = [2**15+110,2**15+1400,2**15+2700,2**15+4020,2**15+5320,2**15+6640,2**15+7940,2**15+9240,2**15+10560,2**15+11860,2**15+13160,2**15+14480
,2**15+15780,2**15+17080,2**15+18380,2**15+19680,2**15+21000,2**15+22300,2**15+23620,2**15+24920,2**15+26240,2**15+27560,2**15+28888
,2**15+30191,2**15+31487,35,1348,2655,3970,5280,6590,7890,9200,10510,11810,13110,14410,15720,17040,18340,19640,20950,22250,23550,24860,26160
,27460,28780,30080,31400,32700]
dc_dbl = 0.0
dac_dcval = 0
dac_dcval_old = 0
global freq
global fsel
global dac_freqval
global dac_freqval_old
dac_freqval = 0
dac_freqval_old = 0
fsel = 1000
freq = 1
#Plot
global fig
global canvas
global ser
ser = serial.Serial('COM7',921600,timeout=0)
ser.flushInput()
ser.flushOutput()
time.sleep(0.5)
class App:
  def __init__(self, master):
    master.minsize(width=750, height=630)
    master.maxsize(width=1920, height=1200)
    frame = Frame(master)
    self.button = Button(master, text="QUIT", fg="red", command=frame.quit)
    self.button.place(x=710,y=605)
    self.label_relais = Label(text="Relais", font=("Helvetica", 14))
    self.label_relais.place(x=5,y=5)
    self.label_atten = Label(text="Attenuation")
    self.label_atten.place(x=5,y=30)
    self.atten = Radiobutton(master, text="1", variable=Atten, value=144).place(x=5,y=50)
    self.atten = Radiobutton(master, text="1/2", variable=Atten, value=48).place(x=5,y=70)
    self.atten = Radiobutton(master, text="1/3", variable=Atten, value=96).place(x=5,y=90)
    self.atten = Radiobutton(master, text="1/6", variable=Atten, value=192).place(x=5,y=110)
    self.label_offset = Label(text="Offset")
    self.label_offset.place(x=5,y=135)
    self.offset = Radiobutton(master, text="0 V", variable=Offset, value=6).place(x=5,y=155)
    self.offset = Radiobutton(master, text="2 V", variable=Offset, value=3).place(x=5,y=175)
    self.offset = Radiobutton(master, text="4 V", variable=Offset, value=9).place(x=5,y=195)
    self.label_adc = Label(text="ADC", font=("Helvetica", 14))
    self.label_adc.place(x=5,y=220)
    self.label_adc_chan = Label(text="Channel")
    self.label_adc_chan.place(x=5,y=245)
    self.adc_chan = Radiobutton(master, text="1", variable=Chan, value=1).place(x=5,y=265)
    self.adc_chan = Radiobutton(master, text="2", variable=Chan, value=2).place(x=5,y=285)
    self.adc_chan = Radiobutton(master, text="3", variable=Chan, value=3).place(x=5,y=305)
    self.adc_chan = Radiobutton(master, text="4", variable=Chan, value=4).place(x=5,y=325)
    self.label_adc_count = Label(text="Samplecount")
    self.label_adc_count.place(x=5,y=350)
    self.adc_count = Radiobutton(master, text="256", variable=Count, value=8).place(x=5,y=370)
    self.adc_count = Radiobutton(master, text="512", variable=Count, value=9).place(x=5,y=390)
    self.adc_count = Radiobutton(master, text="1024", variable=Count, value=10).place(x=5,y=410)
    self.adc_count = Radiobutton(master, text="2048", variable=Count, value=11).place(x=5,y=430)
    self.adc_count = Radiobutton(master, text="4096", variable=Count, value=12).place(x=5,y=450)
    self.adc_count = Radiobutton(master, text="8192", variable=Count, value=13).place(x=5,y=470)
    self.label_dac = Label(text="DAC", font=("Helvetica", 14))
    self.label_dac.place(x=5,y=495)
    self.label_dc = Label(text="DC Offset")
    self.label_dc.place(x=5,y=520)
    self.dac_dc = Scale(master, variable=DC, from_=-12.5, to=12.5, orient=HORIZONTAL,length=600, width=10,resolution=0.5).place(x=100,y=510)
    self.label_amp = Label(text="Amplitude Vpp")
    self.label_amp.place(x=5,y=550)
    self.dac_amp = Scale(master, variable=AMP, from_=0, to=25, orient=HORIZONTAL,length=600, width=10,resolution=0.1).place(x=100,y=540)
    self.label_freq = Label(text="Frequency")
    self.label_freq.place(x=5,y=580)
    self.dac_freq = Scale(master, variable=FREQ, from_=1, to=10, orient=HORIZONTAL,length=600, width=10,resolution=0.1).place(x=100,y=570)
    self.dac_f_select = Radiobutton(master, text="x 1 Hz", variable=FSel, value=1).place(x=100,y=605)
    self.dac_f_select = Radiobutton(master, text="x 10 Hz", variable=FSel, value=10).place(x=200,y=605)
    self.dac_f_select = Radiobutton(master, text="x 100 Hz", variable=FSel, value=100).place(x=300,y=605)
    self.dac_f_select = Radiobutton(master, text="x 1 kHz", variable=FSel, value=1000).place(x=400,y=605)
    self.dac_f_select = Radiobutton(master, text="x 10 kHz", variable=FSel, value=10000).place(x=500,y=605)
    self.dac_f_select = Radiobutton(master, text="x 100 kHz", variable=FSel, value=100000).place(x=600,y=605)
  def quit():
    root.destroy()
def task_config(): #Configure
  #Init
  global init_int
  if init_int == 1:
    Atten.set(192)
    Offset.set(6)
    Chan.set(1)
    Count.set(10)
    DC.set(0.0)
    AMP.set(0.0)
    init_int = 0
  #Relais
  global relais_val
  global relais_val_old
  atten_int = Atten.get()
  offset_int = Offset.get()
  relais_val = atten_int + offset_int
  if relais_val != relais_val_old:
    print("Setting Relais: " + str(relais_val))
    ser.write(bytearray([10])) # Chan 12
    ser.write(bytearray([relais_val]))
  relais_val_old = relais_val
  time.sleep(0.02)
  #ADC
  global adc_val
  global adc_val_old
  chan_int = Chan.get()
  count_int = Count.get()
  adc_val = chan_int*16+count_int
  if adc_val != adc_val_old:
    print("Setting ADC: " + str(adc_val))
    ser.write(bytearray([16])) # ADC
    ser.write(bytearray([adc_val]))
  adc_val_old = adc_val
  time.sleep(0.02)
  #DAC
  global amp
  global dac_ampval
  global dac_ampval_old
  amp = AMP.get()
  dac_ampval = int(amp*2603)
  if dac_ampval != dac_ampval_old:
    print("Setting DAC AMP: " + str(dac_ampval))
    ser.write(bytearray([4])) # AMP
    ser.write(bytearray([int(dac_ampval/256)]))
    ser.write(bytearray([int(dac_ampval%256)]))
  dac_ampval_old = dac_ampval
  time.sleep(0.02)
  global dc_dbl
  global dac_dcval
  global dac_dcval_old
  dc_dbl = DC.get()
  if dc_dbl == abs(dc_dbl):
    index = 25 + int(dc_dbl/0.5)
  else:
    index = 25 - int(abs(dc_dbl)/0.5)
  dac_dcval = DC_offset_arr[index]
  if dac_dcval != dac_dcval_old:
    print("Setting DAC DC: " + str(dac_dcval))
    ser.write(bytearray([2])) # AMP
    ser.write(bytearray([int(dac_dcval/256)]))
    ser.write(bytearray([int(dac_dcval%256)]))
  dac_dcval_old = dac_dcval
  time.sleep(0.02)
  global freq
  global fsel
  global dac_freqval
  global dac_freqval_old
  freq = FREQ.get()
  fsel = FSel.get()
  dac_freqval = int((freq*fsel)/(50*10**6/2**32))
  f_byte3, f_byte2, f_byte1, f_byte0 = (dac_freqval & 0xFFFFFFFF).to_bytes(4, 'big')
  if dac_freqval != dac_freqval_old:
    print("Setting DAC Freq: " + str(int(freq*fsel)) + " Step: " + str(dac_freqval))
    ser.write(bytearray([6])) # Freq
    ser.write(bytearray([f_byte3]))
    ser.write(bytearray([f_byte2]))
    ser.write(bytearray([f_byte1]))
    ser.write(bytearray([f_byte0]))
  dac_freqval_old = dac_freqval
  time.sleep(0.02)
  root.after(1000,task_config)
def task_plot(): #Plot
  chan_int = Chan.get()
  count_int = Count.get()
  N = 2**count_int
  N = 2**count_int
  F = 5.0 #in MHz ADC_Samplerate
  Nplot = 2**Count.get() # Zahl der zu plottenden Samples im oberen Plot
  FFT_xmin = 0 # Frequenzbereich im unteren Plot
  FFT_xmax = F/2
  ser.write(bytearray([16]))
  ser.write(bytearray([chan_int*16+count_int]))
  uart_data = bytearray()
  empty_bytearray = [0] * N*2
  start_time = time.time()
  elapsed_time = time.time() - start_time
  while (len(uart_data) < N*2) and (elapsed_time < 10):
    data = ser.read(1024)
    uart_data.extend(data)
    elapsed_time = time.time() - start_time
  if (len(uart_data)) < N*2:
    uart_data.extend(empty_bytearray)
  werte = []
  for x in range(0,N):
    werte.append((uart_data[x*2])*256+(uart_data[x*2+1]))
  timerange = numpy.linspace(0,Nplot*(1.0/F), Nplot)
  freq = numpy.linspace(-F/2, F/2, N)
  response = numpy.linspace(-F/2, F/2, N)
  fftmax=0
  empty_bytearray = [0] * N*2
  fig = plt.figure()
  ax1 = fig.add_subplot(211)
  ax2 = fig.add_subplot(212)
  ### Signal über Zeit ###
  ax1.clear()
  ax1.axis([0, Nplot, 0, 2**16-1])
  ax1.set_xlim(xmax = Nplot*(1.0/F), xmin = 0)
  ax1.set_title("ADC " + str(chan_int) +" Signal")
  ax1.set_ylabel("ADC Wert")
  ax1.xaxis.set_label_coords(1.05, -0.015)
  ax1.set_xlabel("t "+r'[$\mu$s]')
  ax1.plot(timerange,werte[0:Nplot])
  ### FFT ###
  A = fft(werte*blackman(N))
  response = 20 * numpy.log10(numpy.abs(fftshift(A / abs(A[1:N]).max())))
  fftmax=(numpy.argmax(response[int(N/2)+2:]))*((F/2)/(N/2))*1000
  ax2.clear()
  ax2.axis([-0.5, 0.5, -140, 0])
  ax2.set_xlim(xmax = FFT_xmax, xmin = FFT_xmin)
  ax2.set_title("FFT - Blackman")
  ax2.set_ylabel("Amplitude [dB]")
  ax2.set_xlabel("f [MHz]" + " max@" + str(int(fftmax)) + "kHz")
  ax2.plot(freq, response)
  canvas = FigureCanvasTkAgg(fig, master = root)
  canvas._tkcanvas.place(x=100,y=10)
  root.after(1000,task_plot)
root = Tk()
#Relais
Atten = IntVar()
Atten.set(192)
Offset = IntVar()
Offset.set(6)
#ADC
Chan = IntVar()
Chan.set(1)
Count = IntVar()
Count.set(10)
#DAC
DC = DoubleVar()
DC.set(0.0)
AMP = DoubleVar()
AMP.set(0.0)
FREQ = DoubleVar()
FREQ.set(1.0)
FSel = IntVar()
FSel.set(1000)
app = App(root)
root.after(100,task_config)
root.after(100,task_plot)
root.mainloop()
#ser.close()