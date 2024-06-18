import serial
from RoboticArmClass import RoboticArm
import publish_joint_state 
import time

servos_name = ['ang_joint_1','ang_joint_2','ang_joint_3','ang_joint_4','ang_joint_5','gripper']
gripperPose = '0'
curJointState = [0,0,0,0,0]





def init_ser_connection(port, baudrate):
    ser = None
    first = False

    while not ser:
        try:
            ser = serial.Serial(port, baudrate=baudrate, timeout=1)
            print("\n Serial connection established.")
            return ser
        
        except ValueError as ve:
            print("Error:", str(ve))
            
        except serial.SerialException as se:
            if not first:
                error = "Serial port error:" + str(se) + "  "
                first = True

            error = error[1:] + error[0]
            print("\r" + error, end="")
            time.sleep(0.1)

            
        except Exception as e:
            print("An error occurred:", str(e))    



def MoveToPointCallback(x, y, z):
    # print("*" *20)
    roboticArm = RoboticArm()
    availJointState,goalJointState = roboticArm.InversProblem(x ,y ,z)

    if (not availJointState):
      
        # print('Point cannot be reached') #если выводит это то надо изменять координаты или другие значения для манипулятора
        return False    
    else:
        goalJointState = [str(el) for el in goalJointState]
        strName = ' '.join(servos_name)
        strJS = ' '.join(goalJointState) + ' ' + gripperPose
        strCmd = strName + ' ' + strJS

        # print(strCmd)
        # print('Point can be reached')
        return True
        
        
        # joint_Cmd = publish_joint_state.convert_pose(strCmd)
        # print("joint_Cmd: ", joint_Cmd)




def read_data_from_arduino(serial):
      
        try:
            data = serial.readline().decode("utf-8")
            return extract_coord(data)

        except:
            pass


def extract_coord(data):
    if data.count(":") == 2:
        x,y,z = data.split(":")
        return x, y,z


class NeedMove:
    prev_x, prev_y, prev_z = 0, 0, 0

    @classmethod
    def check(self, x, y, z):
        if self.prev_x != x or self.prev_y != y or self.prev_z != z:
            self.prev_x = x
            self.prev_y = y
            self.prev_z = z
            return True
    

def main():
    ser_con = init_ser_connection("/dev/ttyACM0", 115200)

    while True:
        try:
            x, y,z = read_data_from_arduino(ser_con)
            print(x,y,z)

            if NeedMove.check(x, y, z):
                MoveToPointCallback(x,y,z)
        

        except:
            continue



if __name__ == "__main__":
    main()

