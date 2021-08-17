#!/usr/bin/env python3
import sys
import rospy
from std_msgs.msg import Int32, Bool
import actionlib
from battery_simulator.msg import (
  battery_simAction, battery_simGoal, battery_simResult 
)

class BatterySimClientNode:
  def __init__(self):
    rospy.init_node("BatterySimClient")
    rospy.loginfo("Starting BatterySimClientNode as BatterySimClient.")
    self.goal = battery_simGoal()
    self.client = actionlib.SimpleActionClient(
      'battery_simulator', battery_simAction
      )
    self.client.wait_for_server()
    rospy.loginfo('Client set up!')

  def battery_state(self, charge_condition):
    """
    We receive the charge state as an argument and send the goal to the server
    accordingly while charging or discharging

    Args:
        charge_condition (bool): 1 - charging, 0 - discharging
    """
    self.goal.charge_state = charge_condition
    rospy.loginfo('Sending goal: {}'.format(charge_condition))
    self.client.send_goal(self.goal)
    rospy.loginfo('Goal sent!')
  
  def wait_for_result(self):
    self.client.wait_for_result()
    return self.client.get_result()


if __name__ == "__main__":
  try:
    BatterySimClient = BatterySimClientNode()
    BatterySimClient.battery_state(bool(int(sys.argv[1])))
    rospy.loginfo('Waiting for result!')
    result = BatterySimClient.wait_for_result()
    print('Battery charge: {}'.format(result.battery_status))
  except rospy.ROSInterruptException:
    print('Program interrupted')