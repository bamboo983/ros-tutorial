#!/usr/bin/env python

## Simple talker demo that listens to std_msgs/Float64 published 
## to the 'current_time' topic

import rospy
from std_msgs.msg import Float64
import matplotlib.pyplot as plt

duration = []

def callback(data):
    global duration
    diff_time = rospy.get_time() - data.data
    duration.append(diff_time)
    rospy.loginfo('Message duration: %f seconds' % diff_time)

    if len(duration) == 360:
        plt.hist(duration)
        plt.title('Histogram of Duration of Message from Publisher to Subscriber (N = 360)')
        plt.xlabel('Duration (second)')
        plt.ylabel('Frequency')
        plt.show()

def listener():

    rospy.init_node('time_subscriber', anonymous=True)
    rospy.Subscriber('current_time', Float64, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
if __name__ == '__main__':
    listener()
