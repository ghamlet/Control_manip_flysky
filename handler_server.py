#!/usr/bin/env python
import serial
from RoboticArmClass import RoboticArm
import publish_joint_state 

servos_name = ['ang_joint_1','ang_joint_2','ang_joint_3','ang_joint_4','ang_joint_5','gripper']
gripperPose = '0'
curJointState = [0,0,0,0,0]


def init_ser_connection(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        print("Serial connection established.")
        return ser
        
    except ValueError as ve:
        print("Error:", str(ve))
        return None
        
    except serial.SerialException as se:
        print("Serial port error:", str(se))
        return None
        
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def main_loop(conn):
    prev_decoded_response = None
   
    while True:
        response = conn.readline()
        decoded_response = response.decode('utf-8')
        
        print("I recive message: ", decoded_response)
        
        if decoded_response != prev_decoded_response:
            MoveToPointCallback(decoded_response)
            prev_decoded_response = decoded_response


def ParseMsg(msg):
    #здесь мы выделяем координаты из строки, но проблема в том что они не являются действительными координатами для манипулятора, ведь у нас они изменяются от -255 до 255. Нас интересует момент вверхбидет джойстик или вниз, чтобы постепенного увеличивать или уменьшать координату для каждого направления
    try:
        coord_list = msg.split(':')
        print(coord_list)
        
        x = float(coord_list[0])
        y = float(coord_list[1])
        z = float(coord_list[2])
        
        return x,y,z
        
    except ValueError:
        pass



def MoveToPointCallback(msg):
    x,y,z = ParseMsg(msg)
    roboticArm = RoboticArm()
    availJointState,goalJointState = roboticArm.InversProblem(x,y,z)

    if (not availJointState):
        print('Point cannot be reached') #если выводит это то надо изменять координаты или другие значения для манипулятора
    else:
        goalJointState = [str(el) for el in goalJointState]
        strName = ' '.join(servos_name)
        strJS = ' '.join(goalJointState) + ' ' + gripperPose
        strCmd = strName + ' ' + strJS

        print(strCmd)
        print('Point can be reached')
        
        
        joint_Cmd = publish_joint_state.convert_pose(strCmd)
        print("joint_Cmd: ", joint_Cmd)
        

        


if __name__=='__main__':

    ser_port, baudrate = "/dev/ttyACM0", 115200   #заменить на то как определяется манипулятор через /dev/tty*
    connection = init_ser_connection(ser_port, baudrate)
    
    main_loop(connection)

   
    

       