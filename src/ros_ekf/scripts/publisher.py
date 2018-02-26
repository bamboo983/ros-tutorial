#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from tf.transformations import quaternion_from_euler

import csv

def publisher():
    odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)
    imu_pub = rospy.Publisher('imu_data', Imu, queue_size=10)
    rospy.init_node('publisher', anonymous=True)
    rate = rospy.Rate(20)

    # read gyro data and convert to quaternion
    quaternion = []
    angular_velocity = []
    with open('/home/bamboo/catkin_ws/src/ros_ekf/scripts/imu_synthetic/gyro.txt', 'rb') as f:
    # with open('/home/bamboo/catkin_ws/src/ros_ekf/scripts/imu_gladiator/gyro.txt', 'rb') as f:
        gyro_reader = csv.reader(f, delimiter=',')
        for gyro in gyro_reader:
            q = quaternion_from_euler(float(gyro[0]), float(gyro[1]), float(gyro[2]))
            quaternion.append(list(q))
            angular_velocity.append(list((float(gyro[0]), float(gyro[1]), float(gyro[2]))))

    # read linear acceleration data
    linear_acceleration = []
    with open('/home/bamboo/catkin_ws/src/ros_ekf/scripts/imu_synthetic/accel.txt', 'rb') as f:
    # with open('/home/bamboo/catkin_ws/src/ros_ekf/scripts/imu_gladiator/accel.txt', 'rb') as f:
        accel_reader = csv.reader(f, delimiter=',')
        for a in accel_reader:
            linear_acceleration.append(list((float(a[0]), float(a[1]), float(a[2]))))

    # read timestamp data
    timestamp = []
    with open('/home/bamboo/catkin_ws/src/ros_ekf/scripts/imu_synthetic/timestamp.txt', 'rb') as f:
    # with open('/home/bamboo/catkin_ws/src/ros_ekf/scripts/imu_gladiator/timestamp.txt', 'rb') as f:
        timestamp_reader = csv.reader(f, delimiter=',')
        for t in timestamp_reader:
            timestamp.append(list((float(t[0]), float(t[1]))))

    # for ii in range(len(timestamp)):
    ii = 0
    while True:

        # create Odometry
        odom = Odometry()

        # std_msgs/Header header
        odom.header.seq = ii
        odom.header.stamp = rospy.Time.from_sec(timestamp[ii][0])
        odom.header.frame_id = 'base_footprint'

        # string child_frame_id
        # odom.child_frame_id = '0'

        # geometry_msgs/PoseWithCovariance pose
        odom.pose.pose.position.x = 1
        odom.pose.pose.position.y = 0
        odom.pose.pose.position.z = 0

        odom.pose.pose.orientation.x = quaternion[ii][0]
        odom.pose.pose.orientation.y = quaternion[ii][1]
        odom.pose.pose.orientation.z = quaternion[ii][2]
        odom.pose.pose.orientation.w = quaternion[ii][3]

        odom.pose.covariance = [1, 0, 0, 0, 0, 0,
                                0, 1, 0, 0, 0, 0,
                                0, 0, 1, 0, 0, 0,
                                0, 0, 0, 1e4, 0, 0,
                                0, 0, 0, 0, 1e4, 0,
                                0, 0, 0, 0, 0, 1e4]

        # geometry_msgs/TwistWithCovariance twist
        # odom.twist.twist.linear.x = linear_acceleration[ii][0]
        # odom.twist.twist.linear.y = linear_acceleration[ii][1]
        # odom.twist.twist.linear.z = linear_acceleration[ii][2]

        # odom.twist.twist.angular.x = angular_velocity[ii][0]
        # odom.twist.twist.angular.y = angular_velocity[ii][1]
        # odom.twist.twist.angular.z = angular_velocity[ii][2]

        # odom.twist.covariance = [1, 0, 0, 0, 0, 0,
                                # 0, 1, 0, 0, 0, 0,
                                # 0, 0, 1, 0, 0, 0,
                                # 0, 0, 0, 1e4, 0, 0,
                                # 0, 0, 0, 0, 1e4, 0,
                                # 0, 0, 0, 0, 0, 1e4]

        # create Imu
        imu = Imu()

        # std_msgs/Header header
        imu.header.seq = ii
        imu.header.stamp = rospy.Time.from_sec(timestamp[ii][0])
        imu.header.frame_id = 'base_footprint'

        # geometry_msgs/Quaternion orientation
        imu.orientation.x = quaternion[ii][0]
        imu.orientation.y = quaternion[ii][1]
        imu.orientation.z = quaternion[ii][2]
        imu.orientation.w = quaternion[ii][3]
        imu.orientation_covariance = [1e-3, 0, 0,
                                        0, 1e-3, 0,
                                        0, 0, 1e-3]

        # geometry_msgs/Vector3 angular_velocity
        imu.angular_velocity.x = angular_velocity[ii][0]
        imu.angular_velocity.y = angular_velocity[ii][1]
        imu.angular_velocity.z = angular_velocity[ii][2]
        imu.angular_velocity_covariance = [1e-3, 0, 0,
                                            0, 1e-3, 0,
                                            0, 0, 1e-3]

        # geometry_msgs/Vector3 linear_acceleration
        imu.linear_acceleration.x = linear_acceleration[ii][0]
        imu.linear_acceleration.y = linear_acceleration[ii][1]
        imu.linear_acceleration.z = linear_acceleration[ii][2]
        imu.linear_acceleration_covariance = [1e-3, 0, 0,
                                                0, 1e-3, 0,
                                                0, 0, 1e-3]

        # publish the subscribed topics by robot_pose_ekf
        odom_pub.publish(odom)
        imu_pub.publish(imu)

        print odom
        print imu
        
        ii += 1
        if ii == len(timestamp):
            ii = 0
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
