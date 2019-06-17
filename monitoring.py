#!/usr/bin/python

import npyscreen as npy
import threading
import epics
import time

class Form(npy.Form):
    def __init__(self, **kws):
        npy.Form.__init__(self, **kws)
        self.busy = False

    def update(self):
        #synchronize gui updates between all monitored channels
        if self.busy == False:
            self.busy = True
        else:
            return
        time.sleep(0.1)
        self.DISPLAY()
        self.busy = False

class pv_monit:
    def __init__(self, frame, pvname):
        self.frame = frame
        self.line = self.frame.add(npy.TitleFixedText, name=pvname, begin_entry_at=30)
        self.line.aditable = False
        if("status" in pvname):
            self.pv = epics.PV(pvname, callback=self.on_update_status)
        else:
            self.pv = epics.PV(pvname, callback=self.on_update_value)

    def on_update_status(self, value=None, status=None, severity=None, **kws):
        if(value == 0):
            self.line.value = "{0}".format("Off")
        elif(value == 1):
            self.line.value = "{0}".format("On")
        elif(value == 3):
            self.line.value = "{0}".format("Ramping up")
        elif(value == 5):
            self.line.value = "{0}".format("Ramping down")
        else:
            self.line.value = "{0}".format("Trip")
        self.frame.update()

    def on_update_value(self, value=None, status=None, severity=None, **kws):
        self.line.value = "{0}".format(value)
        self.frame.update()

class gui(npy.NPSApp):
    def main(self):
        self.frame = Form(name="sTGC monitoring", lines=20, columns=70)
        ll = [i for i in open("/star/u/sysuser/users/lukas/STGC/stgc.list")]
        self.pvs = []
        for pvname in ll:
            self.pvs.append( pv_monit(self.frame, pvname.rstrip()) )

        npy.blank_terminal()
        self.frame.edit()

if __name__ == "__main__":
    gui = gui()
    gui.run()
