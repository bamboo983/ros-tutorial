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
            # Client send request timestamp
            request_time = rospy.get_time()
            get_time = rospy.ServiceProxy('get_time', GetTime)
            # Server send response timestamp
            server_response_time = get_time().time
            # Client receive response timestamp
            client_receive_response_time = rospy.get_time()
            # Duration of client request to response from server
            round_trip = client_receive_response_time - request_time
            # Duration of server response to client
            one_way = client_receive_response_time - server_response_time
            rospy.loginfo('Round trip: %f seconds' % round_trip)
            rospy.loginfo('One way: %f seconds' % one_way)
            duration.append(round_trip)

            if len(duration) == 360:
                plt.hist(duration)
                plt.title('Histogram of Duration of Client Request to Response (N = 360)')
                plt.xlabel('Duration (second)')
                plt.ylabel('Frequency')
                plt.show()
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        rate.sleep()

if __name__ == "__main__":
    get_time_client()
