#!/usr/bin/python
import ctypes

TestLib = ctypes.cdll.LoadLibrary('/star/u/sysuser/users/lukas/CAENHVWrapper-5.82/lib/x64/libcaenhvwrapper.so.5.82')
handle = ctypes.c_int(0)
result = TestLib.CAENHV_InitSystem(0,0,"130.199.60.8","admin","admin",ctypes.byref(handle)) #TOF
# result = TestLib.CAENHV_InitSystem(2,0,"130.199.60.172","admin","admin",ctypes.byref(handle)) # MTD
# print "a = ",hex(result)
# print "b = ",handle.value

###########################################################################################
# FUNGUJE
#pole = (5,7)
#bdlist = (ctypes.c_ushort*2)(*pole)
#a = (ctypes.c_float*2)(0.0,1.0)
#result1 = TestLib.CAENHV_GetBdParam(handle.value,2,bdlist,"Temp",ctypes.byref(a))
#print hex(result1)
#print "d = ",a[3]
#print "e = ",a[3]

###########################################################################################
#FUNGUJE
# chlist = (ctypes.c_ushort*2)(0,1)
# meno = ( (ctypes.c_char*10)*2 )()
# result3 = TestLib.CAENHV_GetChName(handle.value,bdlist[0],2,chlist,ctypes.byref(meno))
# print hex(result3)
# print meno[0][:]
# print meno[1][:]

###########################################################################################                                                        # FUNGUJE                                                                                                              
pole = (0,1,2,3,4,5)
chlist = (ctypes.c_ushort*6)(*pole)
a = (ctypes.c_float*6)(0.0,1.0,2.0,3.0,4.0,5.0)
result1 = TestLib.CAENHV_GetChParam(handle.value,5,"VMon",6,chlist,ctypes.byref(a))
print hex(result1)
print "0 = ",a[0]
print "1 = ",a[1]
print "2 = ",a[2]
print "3 = ",a[3]
print "4 = ",a[4]
print "5 = ",a[5]



