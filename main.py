#!/usr/local/epics/modules/pythonIoc/pythonIoc


#import basic softioc framework
from softioc import softioc, builder

#import the the application
from STGC import STGC

stgc = STGC('130.199.60.8')

#run the ioc
builder.LoadDatabase()
softioc.iocInit()

stgc.do_startthread()

#start the ioc shell
softioc.interactive_ioc(globals())
