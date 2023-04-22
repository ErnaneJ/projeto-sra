# coding=utf-8
# Insert in a script in Coppelia
# simRemoteApi.start(19999)
try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import math
import time

print ('Program started!')

sim.simxFinish(-1) # just in case, close all opened connections
clientID = sim.simxStart('127.0.0.1',19999,True,True,5000,5)

robotName = 'lumibot'

if clientID != -1:
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print ('Connected to remote API server!')
    sim.simxAddStatusbarMessage(clientID, "It's Working...", sim.simx_opmode_oneshot_wait)
    
    time.sleep(0.02)

    error, robot = sim.simxGetObjectHandle(clientID, robotName, sim.simx_opmode_oneshot_wait)
    [error, robotLeftMotor] = sim.simxGetObjectHandle(clientID, robotName +'_leftMotor',sim.simx_opmode_oneshot_wait)
    [error, robotRightMotor] = sim.simxGetObjectHandle(clientID, robotName + '_rightMotor', sim.simx_opmode_oneshot_wait)

    time.sleep(2)

    count = 0
    while(count < 250):
        count+=1

        [error, [xr,yr,zr]] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_buffer)
        [error, [alpha, beta, gamma]] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_buffer)

        vRef = 1.0
        sim.simxAddStatusbarMessage(clientID, 'The x position is '+str(xr) + ' and the y position is '+str(yr), sim.simx_opmode_oneshot_wait)

        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID, robotRightMotor, vRef, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, vRef, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    sim.simxAddStatusbarMessage(clientID, 'Program is paused', sim.simx_opmode_blocking )
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')