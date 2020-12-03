import os
import rospy
import math as m
import sys 
import numpy as np
from gazebo_msgs.srv import GetModelState, GetModelStateRequest # Import the service message used by the service /gazebo/delete_model
from geometry_msgs.msg import Twist
import subprocess
check = 0
box_i = 0
box_x = []
box_y = []

def saveBoxVal(x,y):
    global box_x, box_y
    box_x.append(x)
    box_y.append(y)
    print ("Saving: "+ str(x) + " " + str(y))
    return


def checkBoxLocation(x,y):
    global box_x, box_y, check
    #ret False
    print ("Checking if we have this in the array: "+ str(x) + " " + str(y))
    for i in range(len(box_x)):
        if(box_x[i] == x and box_y[i] == y):
                print ("Found this in the array: "+ str(box_x[i]) + " " + str(box_y[i]) + str(len(box_x)))
                return False
        if i == len(box_x)-1:
            check = 0
    for i in range(len(box_x)):
        xx = box_x[i]
        yy = box_y[i]
        d = np.sqrt((xx-x)*(xx-x)+(yy-y)*(yy-y))
        print ("According to my calculations: " + str(d))
        if d <= 1:
            return True
    if x >= 6.4 or x <= -6.4 or y >= 6.4 or x <= -6.4:
        print ("We will be making another box")
        return True
    print ("We will not be making another box")
    return False

rospy.init_node('bounds_check',anonymous=True)
count = 0
name = 'box'


while True:
    #rospy.wait_for_message('/gazebo/get_model_state', GetModelState, timeout=None)
    rospy.sleep(0.5)
    loc = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
    a = GetModelStateRequest()
    a.model_name = "my_robot"
    #print loc(a)
    is_box_dropped = 0
    xpo = loc(a).pose.position.x
    ypo = loc(a).pose.position.y
    if xpo >= 5 or ypo >=5:
        b0 = "./drop_box.sh "
        b1 = name + str(box_i) + " "
        box_i = count
        if xpo >= 5:
            xpo = xpo + 1.4
            b2 = str(xpo) + " "
        else:
            b2 = b2 = str(xpo) + " "
        
        if ypo >= 5:
            ypo = ypo + 1.4
            b3 = str(ypo) + " "
        else:
            b3 = str(ypo) + " "
        
        b4 = "&"
        buff = b0+b1+b2+b3+b4
        xpo = round(xpo,1)
        ypo = round(ypo,1)



        if checkBoxLocation(xpo, ypo) == True and check == 0:
            check = 1
            
            print("We are at the boundary: "+ str(xpo) + " " + str(ypo))

            print (str(xpo) + " " + str(ypo))

            count +=1
            print(str(buff))
            os.system(buff)
            
            is_box_dropped = 1
            saveBoxVal(xpo,ypo)
            rospy.sleep(2)

    elif xpo <= -5 or ypo <= -5:
        b0 = "./drop_box.sh "
        b1 = name + str(box_i) + " "
        box_i = count
        if xpo <= -5:
            xpo = xpo - 1.4
            b2 = str(xpo) + " "
        else:
            b2 = b2 = str(xpo) + " "
        
        if ypo <= -5:
            ypo = ypo - 1.4
            b3 = str(ypo) + " "
        else:
            b3 = str(ypo) + " "
        
        b4 = "&"
        buff = b0+b1+b2+b3+b4
        xpo = round(xpo,1)
        ypo = round(ypo,1)
        

        if checkBoxLocation(xpo, ypo) == True and check == 0:
            check = 1
            print("We are at the boundary: "+ str(xpo) + " " + str(ypo))

            count +=1
            os.system(buff)
            
            is_box_dropped = 1
            saveBoxVal(xpo,ypo)
            rospy.sleep(2)