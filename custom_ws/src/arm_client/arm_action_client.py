#!/usr/bin/env python3
import rospy
import actionlib
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal

class MoveJointNode:
  def __init__(self):
    rospy.init_node("joint_position_tester")
    rospy.loginfo("Starting MoveJointNode as joint_position_tester.")
    self.client = actionlib.SimpleActionClient(
      'arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction
      )
    self.client.wait_for_server()
    self.goal = FollowJointTrajectoryGoal()
    self.goal.trajectory.joint_names = [
      'arm_base_joint', 'shoulder_joint', 'bottom_wrist_joint', 'elbow_joint',
      'top_wrist_joint'
    ]

  def move_joint(self, angles):
    point = JointTrajectoryPoint()
    point.positions = angles
    point.time_from_start = rospy.Duration(3)
    self.goal.trajectory.points.append(point)
    self.client.send_goal_and_wait(self.goal)


if __name__ == "__main__":
  joint_position_tester = MoveJointNode()
  joint_position_tester.move_joint([0.5]*5)
  rospy.spin()
  