#!/usr/bin/env python

from datetime import datetime
from math import *
from numpy import *
from pylab import *

def get_time_ms():
    dt = datetime.datetime.now()
    return 1e3*dt.microsecond

#constants
ShakeAmplitudeThreshold = 2
ShakeOscillationCountParameter = 4
MaxShakePeriodMs = 1e10 #800
GlobalTimeWindowMs = ShakeOscillationCountParameter*MaxShakePeriodMs
DeadTimeWindowMs = MaxShakePeriodMs

#generate input data
inData = []
dataLen = 45
amp = 3
freq = pi/3
time = range(0, dataLen)
inData = []
for n in time:
    inData.append(amp*sin(2*pi*freq*n))

def plot_data():
    stem(time, inData)
    plot([time[0], time[-1]], [ShakeAmplitudeThreshold, ShakeAmplitudeThreshold], 'k--')
    plot([time[0], time[-1]], [-ShakeAmplitudeThreshold, -ShakeAmplitudeThreshold], 'k--')
    show()

#static variales for detectShake function
FlagThresholdCount = [0, 0, 0]
TimeStartWindowMs = [-1, -1, -1]
FlagPositive = [0, 0, 0] #1 - positive, -1 - negative
PrevSample = [0, 0, 0]
MachineState = 0 #0 - reset, 1 - wait, 2 - threshold reached, 3 - search
ShakeAxis = 0
CurFlagPositive = [0, 0, 0]
def detectShake(iX, iY, iZ):
    global MachineState
    global FlagPositive
    global TimeStartWindowMs
    global FlagThresholdCount
    global PrevSample
    global ShakeAxis
    global CurFlagPositive
    #output
    ShakeGestureFlag = 0
    #state machine
    if (1 == MachineState):
        #wait after detecting a shake
        print "wait"
        if ((get_time_ms() - TimeStartWindowMs[ShakeAxis-1]) >= DeadTimeWindowMs):
            MachineState = 0
    if (3 == MachineState):
       #search for a threshold cross
        print "search"
        if (fabs(iX) >= ShakeAmplitudeThreshold) and (fabs(PrevSample[0]) < ShakeAmplitudeThreshold):
            CurFlagPositive[0] = fabs(iX)/iX
            ShakeAxis = 1
            MachineState = 2
            print PrevSample[0], iX
        elif (fabs(iY) >= ShakeAmplitudeThreshold) and (fabs(PrevSample[1]) < ShakeAmplitudeThreshold):
            CurFlagPositive[1] = fabs(iY)/iY
            ShakeAxis = 2
            MachineState = 2
            print PrevSample[1], iX
        elif (fabs(iZ) >= ShakeAmplitudeThreshold) and (fabs(PrevSample[2]) < ShakeAmplitudeThreshold):
            CurFlagPositive[2] = fabs(iZ)/iZ
            ShakeAxis = 3
            MachineState = 2
            print PrevSample[2], iX
        PrevSample[0] = iX
        PrevSample[1] = iY
        PrevSample[2] = iZ
    if (2 == MachineState):
        #threshold reached
        print "threshold cross", ShakeAxis-1
        FlagThresholdCount[ShakeAxis-1] = FlagThresholdCount[ShakeAxis-1]+1
        MachineState = 3
        if (-1 == TimeStartWindowMs[ShakeAxis-1]):
            print "start obs wnd"
            TimeStartWindowMs[ShakeAxis-1] = get_time_ms()
            FlagPositive[ShakeAxis-1] = CurFlagPositive[ShakeAxis-1]  
        else:
            cur_time = get_time_ms()
            if (CurFlagPositive[ShakeAxis-1] == FlagPositive[ShakeAxis-1]) or ((cur_time-TimeStartWindowMs[ShakeAxis-1]) >= GlobalTimeWindowMs):
                MachineState = 0
                if (CurFlagPositive[ShakeAxis-1] == FlagPositive[ShakeAxis-1]):
                    print "on same sign"
                elif ((cur_time-TimeStartWindowMs[ShakeAxis-1]) >= GlobalTimeWindowMs):
                    print "on time exceeded"
            elif (FlagThresholdCount[ShakeAxis-1] >= ShakeOscillationCountParameter):
                ShakeGestureFlag = 1
                TimeStartWindowMs[ShakeAxis-1] = get_time_ms()#prepare for the wait
                MachineState = 1
            else:
                FlagPositive[ShakeAxis-1] = CurFlagPositive[ShakeAxis-1]
    if (0 == MachineState):
        #reset state machine
        print "reset"
        FlagThresholdCount = [0, 0, 0]
        TimeStartWindowMs = [-1, -1, -1]
        MachineState = 3

    return (ShakeGestureFlag, ShakeAxis)

for i in time:
    (ShakeGestureFlag, ShakeAxis) = detectShake(inData[i], inData[i], inData[i])
    if 1 == ShakeGestureFlag:
        print "#", i, "Shake detected on axis", ShakeAxis

plot_data()
