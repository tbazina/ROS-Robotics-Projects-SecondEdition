#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_navigation_states.move_base_state import MoveBaseState
from flexbe_states.publisher_string_state import PublisherStringState
from flexbe_states.subscriber_state import SubscriberState
from state_machine_examples_flexbe_states.check_call import CheckCall
from state_machine_examples_flexbe_states.power_on_robot import PowerOnRobot
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]
from geometry_msgs.msg import PoseStamped, Quaternion
from tf.transformations import quaternion_from_euler

# [/MANUAL_IMPORT]


'''
Created on Fri Aug 20 2021
@author: Tomislav Bazina
'''
class RestaurantrobotanalogySM(Behavior):
	'''
	Robot has to carry out the following tasks:
- Power on the robot
- Check for a customer call (listen to topic)
- Navigate to the table based on call
- Take the order from the customer
- Go to the delivery area or kitchen if the order has been confirmed or has failed
- Deliver food to the customer
- Return to the waiting space
	'''


	def __init__(self):
		super(RestaurantrobotanalogySM, self).__init__()
		self.name = 'Restaurant robot analogy'

		# parameters of this behavior
		self.add_parameter('button_state_topic', '/button_state')
		self.add_parameter('order_placement_topic', '/order_placement')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1033 y:590, x:483 y:640
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.table_location = self.AddPose2D(0, 0, 0, 'table')
		_state_machine.userdata.order = 'food, drinks'
		_state_machine.userdata.kitchen_location = self.AddPose2D(1, 1, 1, 'kitchen')
		_state_machine.userdata.delivery_area_location = self.AddPose2D(2, 2, 2, 'delivery_area')

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:48 y:74
			OperatableStateMachine.add('POWER_ON',
										PowerOnRobot(),
										transitions={'succeeded': 'WAIT_STATE'},
										autonomy={'succeeded': Autonomy.Off})

			# x:397 y:274
			OperatableStateMachine.add('CHECK_ORDER',
										SubscriberState(topic=self.order_placement_topic, blocking=True, clear=False),
										transitions={'received': 'GO_TO_DELIVERY_AREA', 'unavailable': 'GO_TO_KITCHEN'},
										autonomy={'received': Autonomy.Low, 'unavailable': Autonomy.Low},
										remapping={'message': 'recieved_order'})

			# x:1024 y:352
			OperatableStateMachine.add('GO_TO_DELIVERY_AREA',
										MoveBaseState(action_topic='/move_base_dummy_server'),
										transitions={'arrived': 'finished', 'failed': 'failed', 'preempted': 'WAIT_STATE'},
										autonomy={'arrived': Autonomy.Low, 'failed': Autonomy.Low, 'preempted': Autonomy.Low},
										remapping={'waypoint': 'delivery_area_location'})

			# x:631 y:224
			OperatableStateMachine.add('GO_TO_KITCHEN',
										MoveBaseState(action_topic='/move_base_dummy_server'),
										transitions={'arrived': 'SPEAK_OUT', 'failed': 'failed', 'preempted': 'WAIT_STATE'},
										autonomy={'arrived': Autonomy.Low, 'failed': Autonomy.Low, 'preempted': Autonomy.Low},
										remapping={'waypoint': 'kitchen_location'})

			# x:31 y:274
			OperatableStateMachine.add('GO_TO_TABLE',
										MoveBaseState(action_topic='/move_base_dummy_server'),
										transitions={'arrived': 'TAKE_ORDER', 'failed': 'failed', 'preempted': 'WAIT_STATE'},
										autonomy={'arrived': Autonomy.Low, 'failed': Autonomy.Low, 'preempted': Autonomy.Low},
										remapping={'waypoint': 'table_location'})

			# x:641 y:374
			OperatableStateMachine.add('SPEAK_OUT',
										PublisherStringState(topic=self.order_placement_topic),
										transitions={'done': 'GO_TO_DELIVERY_AREA'},
										autonomy={'done': Autonomy.Low},
										remapping={'value': 'order'})

			# x:241 y:274
			OperatableStateMachine.add('TAKE_ORDER',
										PublisherStringState(topic=self.order_placement_topic),
										transitions={'done': 'CHECK_ORDER'},
										autonomy={'done': Autonomy.Low},
										remapping={'value': 'order'})

			# x:801 y:74
			OperatableStateMachine.add('WAIT_STATE',
										SubscriberState(topic=self.button_state_topic, blocking=True, clear=False),
										transitions={'received': 'CHECK_CALL', 'unavailable': 'WAIT_STATE'},
										autonomy={'received': Autonomy.Low, 'unavailable': Autonomy.Low},
										remapping={'message': 'button_state'})

			# x:48 y:174
			OperatableStateMachine.add('CHECK_CALL',
										CheckCall(),
										transitions={'customer_called': 'GO_TO_TABLE', 'no_call': 'WAIT_STATE'},
										autonomy={'customer_called': Autonomy.Low, 'no_call': Autonomy.Low},
										remapping={'button_state': 'button_state'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	def AddPose2D(self, x, y, theta, frame_id='none'):
		p = PoseStamped()
		p.pose.position.x = x
		p.pose.position.y = y
		p.pose.position.z = 0.
		quaternions = quaternion_from_euler(0, 0, theta)
		p.pose.orientation = Quaternion(*quaternions)
		p.header.frame_id= frame_id
		return p
	# [/MANUAL_FUNC]
