#!/usr/bin/env python

## Simple talker demo that published std_msgs/Float64 messages
## to the 'current_time' topic

import rospy
from std_msgs.msg import Float64

def talker():
    pub = rospy.Publisher('current_time', Float64, queue_size=10)
    rospy.init_node('time_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        time = rospy.get_time()
        pub.publish(time)
        rospy.loginfo('Publish current time: %f' % time)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
