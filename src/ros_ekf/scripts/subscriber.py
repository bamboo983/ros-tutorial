#!/usr/bin/env python

## Simple talker demo that listens to std_msgs/Float64 published 
## to the 'current_time' topic

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Vector3
from tf.transformations import euler_from_quaternion

import csv
import matplotlib.pyplot as plt

ekf_x = []
ekf_y = []
ekf_z = []

def callback(data):
    global ekf_x
    global ekf_y
    global ekf_z

    orientation = data.pose.pose.orientation
    (roll, pitch, yaw) = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
    rospy.loginfo((roll, pitch, yaw))
    ekf_pub = rospy.Publisher('estimate', Vector3, queue_size=10)
    rate = rospy.Rate(5)
    vector = Vector3()
    vector.x = roll
    vector.y = pitch
    vector.z = yaw
    ekf_pub.publish(vector)

    ekf_x.append(roll)
    ekf_y.append(pitch)
    ekf_z.append(yaw)

    if len(ekf_z) == 200:
        plt.plot(len(ekf_x), ekf_x, 'r', len(ekf_y), ekf_y, 'g', len(ekf_z), ekf_z, 'b')
        plt.show()

def subscriber():

    rospy.init_node('subscriber', anonymous=True)
    rospy.Subscriber('robot_pose_ekf/odom_combined', PoseWithCovarianceStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
if __name__ == '__main__':
    subscriber()
