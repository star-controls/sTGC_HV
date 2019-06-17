#!/usr/bin/python
import ctypes

Lib = ctypes.cdll.LoadLibrary('/star/u/sysuser/users/lukas/CAENHVWrapper-5.82/lib/x64/libcaenhvwrapper.so.5.82')
handle = ctypes.c_int(0)
result = Lib.CAENHV_InitSystem(0,0,"130.199.60.8","admin","admin",ctypes.byref(handle))

bdlist = (ctypes.c_ushort*2)(7,9)
a = (ctypes.c_float*2)(0.0, 0.0)
result0 = Lib.CAENHV_GetBdParam(handle.value, 2, bdlist, "Temp", ctypes.byref(a))
print a[0], a[1]


chlist = (ctypes.c_ushort*2)(0,1)
b = (ctypes.c_float*2)(0.0,0.0)
result1 = Lib.CAENHV_GetChParam(handle.value, bdlist[0], "VMon", 2, chlist, ctypes.byref(b))
print b[0], b[1]

chlist1 = (ctypes.c_ushort*2)(0,1)
c = (ctypes.c_float*2)(0.0,0.0)
result1 = Lib.CAENHV_GetChParam(handle.value, bdlist[1], "VMon", 2, chlist1, ctypes.byref(c))
print c[0], c[1]
