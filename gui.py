# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import time
import serial
import threading
import csv
from datetime import datetime
from playsound import playsound
from Adafruit_IO import *

aio = Client('bab3797df29840b2ab431190b2b12c54')

###########################################################################
## Class mainframe
###########################################################################

iniciar = False;
status = False;
##ser = serial.Serial('COM10', 9600)
ser = serial.Serial('/dev/ttyACM0',9600)
data1 = 0
data2 = 0
setpoint = 0
albaja = 0
alalta = 0
csvdata = {}
listadata = [];

def reading():
    if ser.is_open == False:
        ser.open()

    global data1, data2

    while True:
            original_data = str(ser.readline())
            data = original_data.split(",")
            data1 = int(data[0][2:])
            data2 = int(data[1][:-5])
            if status:
                csvdata[data1] = data2
                listadata.append(data2)
def monitor():
        global data1,data2,setpoint,albaja,alalta,status
        alarma_baja = False
        alarma_alta = False

        while True:

            if (data1 >= setpoint):
                termino = True
            else:
                termino = False

            if (data2 <= albaja):
                alarma_baja = True
            else:
                alarma_baja = False

            if (data2 >= alalta):
                alarma_alta = True
            else:
                alarma_alta = False

            if status:
                if alarma_alta | alarma_baja:
                    playsound("smb_pause.wav")
                    time.sleep(4)
                if data1 >= setpoint:
                    playsound("smb_stage_clear.wav")
                    time.sleep(20)

def ioadafruit():

    while True:
        if len(listadata)>0 :
            try:
                aio.send('Diametro', listadata.pop() )
            except ValueError:
                print(ValueError)
        time.sleep(2)

reading_thread = threading.Thread(target=reading)
monitor_thread = threading.Thread(target=monitor)
export_thread = threading.Thread(target=ioadafruit)

class mainframe(wx.Frame):

    def __init__(self, parent):
        global setpoint,albaja,alalta

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Extrusora de Filamento - Qactus", pos=wx.DefaultPosition,
                          size=wx.Size(460, 290), style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE | wx.TAB_TRAVERSAL,
                          name=u"Extrusora de Filamento - Qactus")

        wx.CB_READONLY = False

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        gSizer4 = wx.GridSizer(2, 0, 0, 0)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_NONE)

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Iniciar", wx.DefaultPosition, wx.Size(150, 40), 0)
        bSizer9.Add(self.m_button2, 0, wx.ALL, 5)

        fgSizer1.Add(bSizer9, 10, 0, 5)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.Size(150, 40), 0)
        bSizer10.Add(self.m_button3, 0, wx.ALL, 5)

        fgSizer1.Add(bSizer10, 1, 0, 5)

        gSizer4.Add(fgSizer1, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer2 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_NONE)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.setPoint = wx.StaticText(self, wx.ID_ANY, u"Meta:", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.setPoint.Wrap(-1)
        bSizer5.Add(self.setPoint, 0, wx.ALL, 5)

        self.actual = wx.StaticText(self, wx.ID_ANY, u"Actual:", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.actual.Wrap(-1)
        bSizer5.Add(self.actual, 0, wx.ALL, 5)

        self.alarma_Bajo = wx.StaticText(self, wx.ID_ANY, u"Alarma baja:", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.alarma_Bajo.Wrap(-1)
        bSizer5.Add(self.alarma_Bajo, 0, wx.ALL, 5)

        self.alarma_Alta = wx.StaticText(self, wx.ID_ANY, u"Alarma alta:", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.alarma_Alta.Wrap(-1)
        bSizer5.Add(self.alarma_Alta, 0, wx.ALL, 5)

        self.diametro = wx.StaticText(self, wx.ID_ANY, u"Diametro actual:", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.diametro.Wrap(-1)
        bSizer5.Add(self.diametro, 0, wx.ALL, 5)

        fgSizer2.Add(bSizer5, 1, 0, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_slider1 = wx.Slider(self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.Size(250, 30), wx.SL_HORIZONTAL)
        bSizer6.Add(self.m_slider1, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.m_staticText10.Wrap(-1)
        bSizer6.Add(self.m_staticText10, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_slider2 = wx.Slider(self, wx.ID_ANY, 50, 0, 175, wx.DefaultPosition, wx.Size(250, 30), wx.SL_HORIZONTAL)
        bSizer6.Add(self.m_slider2, 0, wx.ALL, 5)

        self.m_slider3 = wx.Slider(self, wx.ID_ANY, 50, 175, 200, wx.DefaultPosition, wx.Size(250, 30), wx.SL_HORIZONTAL)
        bSizer6.Add(self.m_slider3, 0, wx.ALL, 5)

        self.mm2 = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(-1, 30), 0)
        self.mm2.Wrap(-1)
        bSizer6.Add(self.mm2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        fgSizer2.Add(bSizer6, 1, 0, 5)

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.cms2 = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(40, 30), 0)
        self.cms2.Wrap(-1)
        bSizer11.Add(self.cms2, 0, wx.ALL, 5)

        self.cms = wx.StaticText(self, wx.ID_ANY, "m", wx.DefaultPosition, wx.Size(40, 30), 0)
        self.cms.Wrap(-1)
        bSizer11.Add(self.cms, 0, wx.ALL, 5)

        self.abaja = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(40, 30), 0)
        self.abaja.Wrap(-1)
        bSizer11.Add(self.abaja, 0, wx.ALL, 5)

        self.aalta = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(40, 30), 0)
        self.aalta.Wrap(-1)
        bSizer11.Add(self.aalta, 0, wx.ALL, 5)

        self.mm = wx.StaticText(self, wx.ID_ANY,"mm", wx.DefaultPosition, wx.Size(40, 30), 0)
        self.mm.Wrap(-1)
        bSizer11.Add(self.mm, 0, wx.ALL, 5)

        fgSizer2.Add(bSizer11, 1, wx.ALL, 5)

        gSizer4.Add(fgSizer2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(gSizer4)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_timer1 = wx.Timer()
        self.m_timer1.SetOwner(self, wx.ID_ANY)
        self.m_timer1.Start(250)

        # Valores Iniciales
        self.m_slider1.SetValue(100)
        setpoint = int(self.m_slider1.GetValue())
        self.cms2.SetLabel(str(setpoint))

        self.m_slider2.SetValue(160)
        albaja = int(self.m_slider2.GetValue())
        self.abaja.SetLabel(str(albaja))

        self.m_slider3.SetValue(190)
        alalta = int(self.m_slider3.GetValue())
        self.aalta.SetLabel(str(alalta))

        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.iniciar_click)
        self.m_button3.Bind(wx.EVT_BUTTON, self.guardar_click)
        self.m_slider1.Bind(wx.EVT_SCROLL, self.metasl_mover)
        self.m_slider2.Bind(wx.EVT_SCROLL, self.albaja_mover)
        self.m_slider3.Bind(wx.EVT_SCROLL, self.alalta_mover)
        self.Bind(wx.EVT_TIMER, self.timer, id=wx.ID_ANY)

    def __del__(self):
        pass

        # Virtual event handlers, overide them in your derived class

    def iniciar_click(self, event):
        global status;
        if status == False:
            status=True
            self.m_button2.SetLabel("Detener")
            csvdata.clear()
        else:
            status=False
            self.m_button2.SetLabel("Iniciar")

    def guardar_click(self, event):
        with open(datetime.now().strftime('export/%Y-%m-%d-%H-%M')+'.csv','w') as f:
            w = csv.writer(f)
            w.writerows(csvdata.items())

    def metasl_mover(self, event):
        global setpoint
        setpoint = int(self.m_slider1.GetValue())
        self.cms2.SetLabel(str(setpoint))

    def albaja_mover(self, event):
        global albaja
        albaja = int(self.m_slider2.GetValue())
        self.abaja.SetLabel(str(albaja))

    def alalta_mover(self, event):
        global alalta
        alalta = int(self.m_slider3.GetValue())
        self.aalta.SetLabel(str(alalta))

    def timer(self, event):
        self.m_staticText10.SetLabel(str(data1))
        self.mm2.SetLabel(str(data2))

def Main():
    app = wx.App(False)
    frame = mainframe(None)
    frame.Show(True)
    reading_thread.start()
    monitor_thread.start()
    export_thread.start()
    app.MainLoop()


if __name__ == '__main__':
    Main()

