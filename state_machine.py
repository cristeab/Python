from datetime import datetime
from math import fabs

def get_time_ms():
    dt = datetime.now()
    return 1e3*dt.microsecond

#constants
ShakeAmplitudeThreshold = 3
ShakeOscillationCountParameter = 4
MaxShakePeriodMs = 800
GlobalTimeWindowMs = ShakeOscillationCountParameter*MaxShakePeriodMs
DeadTimeWindowMs = MaxShakePeriodMs

#generate input data
inData = []
temp = range(0, 10)
inData.append(temp)
inData.append(temp)
inData.append(temp)

#static variales for detectShake function
FlagThresholdCount = [0, 0, 0]
TimeStartWindowMs = [-1, -1, -1]
FlagPositive = [0, 0, 0] #1 - positive, -1 - negative
MachineState = 0 #0 - reset, 1 - wait, 2 - threshold reached, 3 - search
def detectShake(iX, iY, iZ):
    #output
    ShakeGestureFlag = 0
    ShakeAxis = 0
    #local variables
    CurFlagPositive = [0, 0, 0]
    if 0 == MachineState:
        #reset state machine
        FlagThresholdCount = [0, 0, 0]
        TimeStartWindowMs = [-1, -1, -1]
        MachineState = 3
    elif 1 == MachineState:
        #wait after detecting a shake
        if (-1 == TimeStartWindowMs[ShakeAxis-1]):
            TimeStartWindowMs[ShakeAxis-1] = get_time_ms()
        elif ((get_time_ms() - TimeStartWindowMs[ShakeAxis-1]) >= DeadTimeWindowMs):
            MachineState = 0
    elif 2 == MachineState:
        #threshold reached
        FlagThresholdCount[ShakeAxis-1] = FlagThresholdCount[ShakeAxis-1]+1
        MachineState = 3
        if (-1 == TimeStartWindowMs[ShakeAxis-1]):
            TimeStartWindowMs[ShakeAxis-1] = get_time_ms()
            FlagPositive[ShakeAxis-1] = CurFlagPositive[ShakeAxis-1]  
        else:            
            if CurFlagPositive[ShakeAxis-1] == FlagPositive[ShakeAxis-1] or ((get_time_ms()-TimeStartWindowMs[ShakeAxis-1]) >= GlobalTimeWindowMs):
                MachineState = 0
            elif FlagThresholdCount[ShakeAxis-1] >= ShakeOscillationCountParameter:
                ShakeGestureFlag = 1
                MachineState = 1
    elif 3 == MachineState:
        #search threshold
        if (fabs(iX) > ShakeAmplitudeThreshold):
            CurFlagPositive[0] = fabs(iX)/iX
            ShakeAxis = 1
            MachineState = 2
        elif (fabs(iY) > ShakeAmplitudeThreshold):
            CurFlagPositive[1] = fabs(iY)/iY
            ShakeAxis = 2
            MachineState = 2
        elif (fabs(iZ) > ShakeAmplitudeThreshold):
            CurFlagPositive[2] = fabs(iZ)/iZ
            ShakeAxis = 3
            MachineState = 2
    else:
        print "unknown state, reseting state machine"
        MachineState = 0
        
    return (ShakeGestureFlag, ShakeAxis)
            
        

