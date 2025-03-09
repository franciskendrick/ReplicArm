import pyfirmata

comport = 'COM4'
board = pyfirmata.Arduino(comport)

# Define servo pins based on your setup
servo_pins = {
    1: board.get_pin('d:3:s'),  # 1st Servo (Z-axis rotation)
    2: board.get_pin('d:5:s'),  # 2nd Servo (X-axis rotation)
    3: board.get_pin('d:6:s'),  # 3rd Servo (X-axis rotation)
    4: board.get_pin('d:9:s'),  # 4th Servo (Z-axis rotation - hand rotation compensation)
    5: board.get_pin('d:10:s'), # 5th Servo (X-axis rotation - camera movement)
    6: board.get_pin('d:11:s'),  # 6th Servo (Z-axis rotation - emergency mobility)
    7: board.get_pin('d:12:s')
}

def set_servo_angle(servo_id, angle):
    """Set the angle of a specific servo motor."""
    if servo_id in servo_pins:
        servo_pins[servo_id].write(angle)
    else:
        print(f"Servo {servo_id} not found.")

def cleanup():
    """Safely close the board connection."""
    board.exit()
