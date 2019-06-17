import time
import threading
import numpy as np
import ctypes
from Channel import Channel
from softioc import builder, softioc
builder.SetDeviceName('sTGC')

class STGC():
    def __init__(self, ip):
        self.ip = ip
        self.boards = [3,7]
        self.channels = [0]
        self.lib = ctypes.cdll.LoadLibrary('/star/u/sysuser/users/lukas/CAENHVWrapper-5.82/lib/x64/libcaenhvwrapper.so.5.82')
        self.handle = ctypes.c_int(0)
        self.result0 = self.lib.CAENHV_InitSystem(0, 0, self.ip, "admin", "admin", ctypes.byref(self.handle))
        print "sTGC is using {0} boards".format(len(self.boards))
        #### Process Variables ####
        self.pv = []
        self.chanlist = []
        for i in range(0, len(self.boards)):
            base_PV = "{0}:Temp".format(self.boards[i])
            self.pv.append(builder.aIn(base_PV))
            for j in range(0, len(self.channels)):
                self.chanlist.append( Channel(self.boards[i], self.channels[j], self.lib, self.handle))

    def temperature(self):
        self.bdlist = (ctypes.c_ushort*len(self.boards))(*self.boards)
        zero_array = np.zeros(len(self.boards))
        self.temp = (ctypes.c_float*len(self.boards))(*zero_array)
        self.result1 = self.lib.CAENHV_GetBdParam(self.handle, len(self.boards), self.bdlist, "Temp", ctypes.byref(self.temp))
        return self.temp

    def do_runreading(self):
        while True:
            time.sleep(0.5)
            # Loop for temperature of boards
            for i in range(0, len(self.boards)):
                self.pv[i].set(self.temperature()[i])
            # Loop for channels
            for ch in self.chanlist:
                ch.update()
 
    def do_startthread(self):
        t = threading.Thread(target=self.do_runreading)
        t.daemon = True
        t.start()
