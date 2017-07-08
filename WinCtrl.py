import win32api
from win32api import GetSystemMetrics
import time, math, pygame, win32con


# Defining constants for each button and axis according to the XBOX 360 joystick inputs
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_LB = 4
BUTTON_RB = 5
BUTTON_SEL = 6
BUTTON_ST = 7
BUTTON_L3 = 8
BUTTON_R3 = 9
AXIS_LEFT_X = 0
AXIS_LEFT_Y = 1
AXIS_RIGHT_X = 4
AXIS_RIGHT_Y = 3
AXIS_TRIGGERS = 2

# Dictionaries translating from button and axis constants to strings
buttons = {0:'A', 1: 'B', 2:'X', 3:'Y', 4:'LB', 5:'RB', 6:'SELECT', 7:'START', 8:'L3', 9:'R3'}
axes = {0:'LEFT_X', 1:'LEFT_Y', 3:'RIGHT_X', 4:'RIGHT_Y'}

# Pygame clock, to control the speed of the refresh rate.
clock = pygame.time.Clock()

# Constants for various speeds and sensitivities.
MOUSE_SPEED = 37
WHEEL_SPEED = 60
FRAMERATE = 40
orig_wheel_speed = WHEEL_SPEED
TRIGGER_SENSITIVITY= 30
DEAD_ZONE = 0.20

def moveMouse(x,y):
	win32api.SetCursorPos((x,y))
	
def left_click(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    
	
def un_left_click(x,y):
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

	
def right_click(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    
def un_right_click(x,y):
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
	
def mouse_wheel_down(x,y):
	win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x,y,WHEEL_SPEED,0)

def mouse_wheel_up(x,y):
	win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x,y,-WHEEL_SPEED,0)
	
	

	
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

p1 = joysticks[0]
p1.init()


last_event = None
right_x_axis, right_y_axis, left_x_axis, left_y_axis = (0,0,0,0)
right_trigger, left_trigger = (0,0)


while True:

	
	if abs(left_x_axis) > 0 or abs(left_y_axis) or abs(right_y_axis) or abs(right_x_axis) > 0:
		pygame.event.post(last_event)
	
	for event in pygame.event.get(): # User did something
		# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		
		if event.type == None and last_event.type == pygame.JOYAXISMOTION:
			event = last_event
		
		myEvent = event.__dict__
		
		
		
		if event.type == pygame.JOYBUTTONDOWN:
			button_pressed =  buttons[myEvent['button']]
			if button_pressed == buttons[BUTTON_A]:
				print ("Clicking!")
				x,y = win32api.GetCursorPos()
				left_click(x,y)
				
			if button_pressed == buttons[BUTTON_B]:
				print("Right click!")
				x,y = win32api.GetCursorPos()
				right_click(x,y)
				
			if button_pressed == buttons[BUTTON_ST]:
				print("Exiting!")
				pygame.joystick.quit()
				exit()
				
			if button_pressed == buttons[BUTTON_LB]:
				MOUSE_SPEED = int(MOUSE_SPEED/2)
			if button_pressed == buttons[BUTTON_RB]:
				orig_wheel_speed = WHEEL_SPEED
				WHEEL_SPEED = int(WHEEL_SPEED/2)
				
		if event.type == pygame.JOYBUTTONUP:
			button_released = buttons[myEvent['button']]
			x,y = win32api.GetCursorPos()
			
			if button_released == buttons[BUTTON_A]:
				un_left_click(x,y)
			if button_released == buttons[BUTTON_B]:
				un_right_click(x,y)
			if button_released == buttons[BUTTON_LB]:
				MOUSE_SPEED = int(MOUSE_SPEED*2)
			if button_released == buttons[BUTTON_RB]:
				WHEEL_SPEED = orig_wheel_speed
				
			
			
		if event.type == pygame.JOYAXISMOTION:
			left_x_axis = p1.get_axis(AXIS_LEFT_X)
			left_y_axis = p1.get_axis(AXIS_LEFT_Y)
			
			right_x_axis = p1.get_axis(AXIS_RIGHT_X)
			right_y_axis = p1.get_axis(AXIS_RIGHT_Y)
			
			
			#TODO fix this so that it adds in accordance with the current movement direction.
			if (myEvent['axis'] == AXIS_TRIGGERS and p1.get_axis(AXIS_TRIGGERS) > 0):
				left_trigger = abs(int(p1.get_axis(AXIS_TRIGGERS) * TRIGGER_SENSITIVITY))
			if left_trigger < DEAD_ZONE:
				left_trigger = 0
			
		#	if (myEvent['axis'] == AXIS_TRIGGERS and p1.get_axis(AXIS_TRIGGERS) < 0):
			#	right_trigger = abs(int(p1.get_axis(AXIS_TRIGGERS) * TRIGGER_SENSITIVITY))
			
			
			
			if abs(left_x_axis) < DEAD_ZONE:
				left_x_axis = 0
			if abs(left_y_axis) < DEAD_ZONE:
				left_y_axis = 0
			if abs(left_x_axis) < DEAD_ZONE and abs(left_y_axis) < DEAD_ZONE:
				left_trigger = 0
			if abs(right_x_axis) < DEAD_ZONE:
				right_x_axis = 0
			if abs(right_y_axis) < DEAD_ZONE:
				right_y_axis = 0
			
			new_x, new_y = win32api.GetCursorPos()
			if left_x_axis < 0:
				new_x += int(left_x_axis*MOUSE_SPEED - left_trigger)
				print("X")
				print(int(left_x_axis*MOUSE_SPEED - left_trigger))
			else:
				new_x += int(left_x_axis*MOUSE_SPEED + left_trigger)
				print("X")
				print(int(left_x_axis*MOUSE_SPEED + left_trigger))
				
			if left_y_axis < 0:
				new_y += int(left_y_axis*MOUSE_SPEED - left_trigger)
				print("Y")
				print(int(left_y_axis*MOUSE_SPEED - left_trigger))
			else:
				new_y += int(left_y_axis*MOUSE_SPEED + left_trigger)
				print("Y")
				print(int(left_y_axis*MOUSE_SPEED + left_trigger))
			
			right_x_axis = int(right_x_axis) + int(right_x_axis*WHEEL_SPEED + right_trigger)
			right_y_axis = int(right_y_axis) + int(right_y_axis*WHEEL_SPEED + right_trigger)
			
			
			
			moveMouse(new_x, new_y)
			
			if right_y_axis > 0:
				mouse_wheel_up(right_x_axis, right_y_axis)
			if right_y_axis < 0:
				mouse_wheel_down(right_x_axis, right_y_axis)
				
			
			last_event = event
			
			
		clock.tick(FRAMERATE)

# Disconnect the controller.
pygame.joystick.quit()