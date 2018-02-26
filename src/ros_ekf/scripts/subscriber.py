#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Vector3
from tf.transformations import euler_from_quaternion

import csv
import numpy as np
from math import *

euler_x = [0]
euler_y = [0]
euler_z = [0]

def callback(data):
    global euler_x
    global euler_y
    global euler_z

    orientation = data.pose.pose.orientation
    (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
    euler_pub = rospy.Publisher('estimate', Vector3, queue_size=10)
    rate = rospy.Rate(20)

    # p, q, r vector
    euler = np.array([roll, pitch, yaw])

    # Euler angle update formula
    a01 = sin(radians(euler_x[-1])) * tan(radians(euler_y[-1]))
    a02 = cos(radians(euler_x[-1])) * tan(radians(euler_y[-1]))
    a11 = cos(radians(euler_x[-1]))
    a12 = -sin(radians(euler_x[-1]))
    a21 = sin(radians(euler_x[-1])) / cos(radians(euler_y[-1]))
    a22 = cos(radians(euler_x[-1])) / cos(radians(euler_y[-1]))

    update = np.array([[1, a01, a02],
                        [0, a11, a12],
                        [0, a21, a22]])

    euler_update = np.dot(update, euler) * 0.005
    # euler_update = np.dot(update, euler) * 0.001

    euler_x.append(euler_x[-1] + degrees(euler_update[0]))
    euler_y.append(euler_y[-1] + degrees(euler_update[1]))
    euler_z.append(euler_z[-1] + degrees(euler_update[2]))

    vector = Vector3()
    vector.x = euler_x[-1]
    vector.y = euler_y[-1]
    vector.z = euler_z[-1]
    euler_pub.publish(vector)
    rospy.loginfo((vector.x, vector.y, vector.z))

def subscriber():

    rospy.init_node('subscriber', anonymous=True)
    rospy.Subscriber('robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
if __name__ == '__main__':
    subscriber()
