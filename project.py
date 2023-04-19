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

print('Program started')
sim.simxFinish(-1)  # close all opened connections
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
robotname = './robozin'
targetname = './target'
if clientID != -1:
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID, 'Working...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)

    error, robot = sim.simxGetObjectHandle(clientID, robotname, sim.simx_opmode_oneshot_wait)
    [error, target] = sim.simxGetObjectHandle(clientID, targetname, sim.simx_opmode_oneshot_wait)
    [error, robotLeftMotor] = sim.simxGetObjectHandle(clientID, './leftMotor', sim.simx_opmode_oneshot_wait)
    [error, robotRightMotor] = sim.simxGetObjectHandle(clientID, './rightMotor', sim.simx_opmode_oneshot_wait)

    [error, positionrobot] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_streaming)
    [error, positiontarget] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_streaming)
    [error, orientationrobot] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_streaming)
    time.sleep(2)


    cont = 0
    target_reached = False
    while cont < 100 and not target_reached:
        cont += 1

        [error, [xr, yr, zr]] = sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_buffer)
        [error, [xt, yt, zt]] = sim.simxGetObjectPosition(clientID, target, -1, sim.simx_opmode_buffer)
        [error, [alpha, beta, gamma]] = sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_buffer)

        sim.simxSetObjectOrientation(clientID, robot, -1, [0, 0, math.atan2(yt - yr, xt - xr)], sim.simx_opmode_oneshot_wait)
        sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, 0.5, sim.simx_opmode_oneshot_wait)
        sim.simxSetJointTargetVelocity(clientID, robotRightMotor, 0.5, sim.simx_opmode_oneshot_wait)

        if math.sqrt((xr - xt) ** 2 + (yr - yt) ** 2) < 0.1:
            sim.simxSetJointTargetVelocity(clientID, robotLeftMotor, 0, sim.simx_opmode_oneshot_wait)
            sim.simxSetJointTargetVelocity(clientID, robotRightMotor, 0, sim.simx_opmode_oneshot_wait)
            sim.simxAddStatusbarMessage(clientID, 'Target reached!', sim.simx_opmode_oneshot_wait)
            target_reached = True

        time.sleep(0.02)

        sim.simxAddStatusbarMessage(clientID, 'X: ' + str(xr) + ' | Y: ' + str(yr) + ' | Z: ' + str(zr), sim.simx_opmode_oneshot_wait)
        sim.simxAddStatusbarMessage(clientID, 'Alpha: ' + str(alpha) + ' | Beta: ' + str(beta) + ' | Gamma: ' + str(gamma), sim.simx_opmode_oneshot_wait)


    sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    sim.simxAddStatusbarMessage(clientID, 'Program paused..', sim.simx_opmode_blocking )
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')