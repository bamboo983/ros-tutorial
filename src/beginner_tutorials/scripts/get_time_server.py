#!/usr/bin/env python

from beginner_tutorials.srv import *
import rospy

def handle_get_time(req):
    time = rospy.get_time()
    rospy.loginfo('Reply current time: %f' % time)
    return GetTimeResponse(time)

def get_time_server():
    rospy.init_node('get_time_server', anonymous=True)
    rospy.Service('get_time', GetTime, handle_get_time)
    rospy.loginfo('Ready to get time.')
    rospy.spin()

if __name__ == "__main__":
    get_time_server()
