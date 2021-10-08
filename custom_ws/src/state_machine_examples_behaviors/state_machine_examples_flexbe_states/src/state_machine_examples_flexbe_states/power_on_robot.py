#!/usr/bin/env python
import rospy
from flexbe_core import EventState, Logger

class PowerOnRobot(EventState):
  '''
  Implements a state that powers up a robot.

  <= succeeded
  '''
  def __init__(self):
    super().__init__(self, outcomes=['succeeded'])
  
  def execute(self, userdata):
    Logger.loginfo('Powering ON robot...')
    rospy.sleep(2)
    return 'succeeded'