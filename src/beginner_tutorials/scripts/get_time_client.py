#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *
import matplotlib.pyplot as plt

duration = []

def get_time_client():
    global duration
    rospy.init_node('get_time_client', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.wait_for_service('get_time')
        try:
            get_time = rospy.ServiceProxy('get_time', GetTime)
            resp = get_time()
            diff_time = rospy.get_time() - resp.time
            rospy.loginfo('Response duration: %f seconds' % diff_time)
            duration.append(diff_time)

            if len(duration) == 360:
                plt.hist(duration)
                plt.title('Histogram of Duration of Response from Server to Client (N = 360)')
                plt.xlabel('Duration (second)')
                plt.ylabel('Frequency')
                plt.show()
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        rate.sleep()

if __name__ == "__main__":
    get_time_client()
