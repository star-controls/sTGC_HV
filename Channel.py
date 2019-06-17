from softioc import builder, softioc
import ctypes

class Channel():
    def __init__(self, bdlist, channel, lib, handle):
        self.bdlist = bdlist
        self.channel = channel
        self.lib = lib
        self.handle = handle
        # Process Variables
        base_PV = "{0}:{1}:".format(self.bdlist, self.channel)
        self.readVol = builder.aIn(base_PV+"vmon", LOPR = 0, HOPR = 2000, EGU = "V")
        self.readCur = builder.aIn(base_PV+"imon", LOPR=0, HOPR=3, PREC=2, HIHI=2, HIGH=1.5, HHSV="MAJOR", HSV="MINOR", EGU = "muA")
        self.readStatus = builder.longIn(base_PV+"status")
        self.setOn = builder.boolOut(base_PV+'setOn', on_update=self.setOn, HIGH=1)
        self.setOff = builder.boolOut(base_PV+'setOff', on_update=self.setOff, HIGH=1)
        self.setVol = builder.aOut(base_PV+'setVol', LOPR=0, HOPR=2000, EGU="V", initial_value=self.getFloatParameter("V0Set"), on_update=self.setV0Set)
        self.setMaxVol = builder.aOut(base_PV+'setMaxVol', LOPR=0, HOPR=2000, EGU="V", initial_value=self.getFloatParameter("SVMax"), on_update=self.setSVMax)
        self.setRampUp = builder.aOut(base_PV+'setRampUp', LOPR=0, HOPR=50, EGU="V/s", initial_value=self.getFloatParameter("RUp"), on_update=self.setRUp)
        self.setRampDown = builder.aOut(base_PV+'setRampDown', LOPR=0, HOPR=50, EGU="V/s", initial_value=self.getFloatParameter("RDWn"), on_update=self.setRDWn)
        self.setTripI = builder.aOut(base_PV+'setTripI', LOPR=0, HOPR=90, PREC=2, EGU="muA", initial_value=self.getFloatParameter("I0Set"), on_update=self.setI0Set) 
        self.setTripTime = builder.aOut(base_PV+'setTripTime', LOPR=0, HOPR=90, PREC=1, EGU="s", initial_value=self.getFloatParameter("Trip"), on_update=self.setTrip)
        
    def update(self):
        self.readVol.set(self.getFloatParameter("VMon"))
        self.readCur.set(self.getFloatParameter("IMon"))
        self.readStatus.set(self.getStatus())

    def getFloatParameter(self, parName):
        chlist = (ctypes.c_ushort*1)(self.channel)
        FloatValues = (ctypes.c_float*1)(0.0)
        result = self.lib.CAENHV_GetChParam(self.handle.value, self.bdlist, parName, 1, chlist, ctypes.byref(FloatValues))        
        return FloatValues[0]

    def getStatus(self):
        chlist = (ctypes.c_ushort*1)(self.channel)
        StatusValues = (ctypes.c_uint*1)(0)
        result = self.lib.CAENHV_GetChParam(self.handle.value, self.bdlist, "Status", 1, chlist, ctypes.byref(StatusValues))
        a = int(StatusValues[0])
        return a

    def setOn(self, val):
        if(val==0):return
	chlist = (ctypes.c_ushort*1)(self.channel)
        BoolValues = (ctypes.c_bool*1)(1)
        result = self.lib.CAENHV_SetChParam(self.handle.value, self.bdlist, "Pw", 1, chlist, ctypes.byref(BoolValues))

    def setOff(self, val):
        if(val==0):return
        chlist = (ctypes.c_ushort*1)(self.channel)
        BoolValues = (ctypes.c_bool*1)(0)
        result = self.lib.CAENHV_SetChParam(self.handle.value, self.bdlist, "Pw", 1, chlist, ctypes.byref(BoolValues))

    def setFloatParameter(self, val, parName):
        chlist = (ctypes.c_ushort*1)(self.channel)
        FloatValues = (ctypes.c_float*1)(val)
        result = self.lib.CAENHV_SetChParam(self.handle.value, self.bdlist, parName, 1, chlist, ctypes.byref(FloatValues))
        #print result
    
    def setV0Set(self, val):
        self.setFloatParameter(val,"V0Set")
    def setI0Set(self, val):
        self.setFloatParameter(val, "I0Set")
    def setSVMax(self, val):
        self.setFloatParameter(val,"SVMax")    
    def setRUp(self, val):
        self.setFloatParameter(val,"RUp")    
    def setRDWn(self, val):
        self.setFloatParameter(val,"RDWn")
    def setTrip(self, val):
        self.setFloatParameter(val,"Trip")
