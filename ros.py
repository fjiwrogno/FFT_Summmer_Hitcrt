from fi_fsa import fi_fsa_v2
import time
import math
import numpy as np
import pandas as pd
import rospy
from sensor_msgs.msg import JointState

server_ip_list = []

def main():
    joint_state_pub = rospy.Publisher("/test", JointState, queue_size=1)
    rate = rospy.Rate(500)

    server_ip_list = fi_fsa_v2.broadcast_func_with_filter(filter_type="Actuator")

    if server_ip_list:

        fsa_state = True
        for i in range(len(server_ip_list)):
            fsa_state = fi_fsa_v2.get_state(server_ip_list[i])
            print("State = %d" % fsa_state)

        print("\n")
        time.sleep(1)

        for i in range(len(server_ip_list)):
            fi_fsa_v2.get_config(server_ip_list[i])

        print("\n")
        time.sleep(1)

        for i in range(len(server_ip_list)):
            pvc = fi_fsa_v2.get_pvc(server_ip_list[i])
            print(
                "Position = %.2f, Velocity = %.3f, Current = %.4f"
                % (pvc[0], pvc[1], pvc[2])
            )
            time.sleep(0.01)

        print("\n")
        time.sleep(1)

        for i in range(len(server_ip_list)):
            dict = {  # 36control_PD_kd_imm
                "control_position_kp_imm": 0.0,
                "control_velocity_kp_imm": 0.0,
                "control_velocity_ki_imm": 0.0,
                "control_PD_kp_imm": 0.0,
                "control_PD_kd_imm": 0.0,
                "control_current_kp_imm": 0,  # not work for now
                "control_current_ki_imm": 0,  # not work for now
                # "control_current_kp_imm": 7.25,  # not work for now
                # "control_current_ki_imm": 0.08,  # not work for now
            }
            fi_fsa_v2.set_pid_param_imm(server_ip_list[i], dict)

        print("\n")
        time.sleep(1)

        # set current control current to 0.0
        for i in range(len(server_ip_list)):
            fi_fsa_v2.set_position_control(server_ip_list[i], position=0.0)

        print("\n")
        time.sleep(1)

        # enable all the motors
        for i in range(len(server_ip_list)):
            fi_fsa_v2.set_enable(server_ip_list[i])

        print("\n")
        time.sleep(1)

        # set work at current control mode
        for i in range(len(server_ip_list)):
            fi_fsa_v2.set_mode_of_operation(
                server_ip_list[i], fi_fsa_v2.FSAModeOfOperation.POSITION_CONTROL
            )

        print("\n")
        time.sleep(1)

        for i in range(len(server_ip_list)):
            fi_fsa_v2.set_position_control(server_ip_list[i], 0.0)

        time.sleep(1)

        while not rospy.is_shutdown():
            joint_state_msg = JointState()
            joint_state_msg.header.stamp = rospy.Time.now()
            joint_state_msg.name = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]
            joint_state_msg.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for i in range(len(server_ip_list)):
                pvc = fi_fsa_v2.get_pvc(server_ip_list[i])
                joint_state_msg.position[i] = pvc[0]
            joint_state_pub.publish(joint_state_msg)
            rate.sleep()

        for i in range(len(server_ip_list)):
            fi_fsa_v2.set_disable(server_ip_list[i])

        time.sleep(1)

        # set work at none control mode
        for i in range(len(server_ip_list)):
            fi_fsa_v2.set_mode_of_operation(
                server_ip_list[i], fi_fsa_v2.FSAModeOfOperation.POSITION_CONTROL
            )


if __name__ == "__main__":
    main()
