#!/usr/bin/env python
import rospy
from flexbe_core import EventState , Logger
# from std_msgs.msg import String

class CheckCall(EventState):
  '''
  Implements a state that checks for customer call (if the button is pressed).
  If the button state is high, state is set to succeeded, else aborted.

  >#  button_state   str   If pressed returns pressed, else not_pressed
  <=  customer_called
  <=  no_call
  '''
  def __init__(self):
    super().__init__(self,
                     input_keys=['button_state'],
                     outcomes=['customer_called', 'no_call'])
  
  def execute(self, userdata):
    rospy.sleep(2)
    if self._button_state == 'pressed':
      return 'customer_called'
    else:
      return 'no_call'

  def on_enter(self, userdata):
    self._button_state = str(userdata.button_state.data)
    Logger.loginfo('Button state: {}'.format(self._button_state))