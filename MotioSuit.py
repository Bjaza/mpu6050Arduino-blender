import bge
import math
from math import *
import mathutils
import time

import sys
#sys.path.append("/usr/lib/python3/dist-packages")
import serial
import glob

port=''.join(glob.glob("/dev/ttyACM*"))
#port=''.join(glob.glob("/dev/ttyUSB*"))
#port=''.join(glob.glob("/dev/rfcomm"))  
ser = serial.Serial(port,9600)
print("connected to: " + ser.portstr)

#Connect the suit first and after a ~second launch the script


# Get the whole bge scene
scene = bge.logic.getCurrentScene()
# Helper vars for convenience
source = scene.objects
# Get the whole Armature
main_arm = source.get('Armature')
ob = bge.logic.getCurrentController().owner


def updateAngles():
	ser.write("a".encode('UTF-8'))
	s=ser.readline()[:-3].decode('UTF-8') #delete ";\r\n"
	angles=[x.split(',') for x in s.split(';')]
	for i in range(len(angles)):
		angles[i] = [float(x) for x in angles[i]]


	trunk = mathutils.Quaternion((angles[0][0],angles[0][1],angles[0][2],angles[0][3]))
	correction = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
	trunk_out = correction*trunk   

	ob.channels['trunk'].rotation_quaternion = mathutils.Vector([angles[0][0],angles[0][1],angles[0][2],angles[0][3]])

	ob.channels['trunk'].rotation_quaternion = trunk_out


	ob.update()
	time.sleep(0.001)

