#!/usr/bin/env python

# This script is a simple ROS node that generates log messages at different severity levels.
# It will generate log messages at DEBUG, INFO, WARN, ERROR, and FATAL levels with increasing count.
#
# Usage:
# - Ensure that the ROS master (roscore) is running and logging is properly configured.
# - Run this script to start generating log messages: `rosrun PACKAGE_NAME test_client.py`


import rospy


def main():
    # Initialize the ROS node
    rospy.init_node('test_client', anonymous=True, log_level=rospy.DEBUG)

    count = 0
    rate = rospy.Rate(1)    # Log one set of messages per second

    # Keep generating log messages until the node is stopped
    while not rospy.is_shutdown():
        rospy.logdebug(f"Debug message: {count}")   # "log_level=rospy.DEBUG" must be set
        rospy.loginfo(f"Info message: {count}")
        rospy.logwarn(f"Warn message: {count}")
        rospy.logerr(f"Error message: {count}")
        rospy.logfatal(f"Fatal message: {count}")

        count += 1
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exiting...")
