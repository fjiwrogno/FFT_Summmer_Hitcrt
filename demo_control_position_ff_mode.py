from fi_fsa import fi_fsa_v2
import time
import math
import numpy as np
import pandas as pd

server_ip_list = []

input_data = pd.read_csv('data_2024-08-16.csv')

class Saver:
    def __init__(self, perioud, pvc0):
        self.input = np.ndarray((perioud, 1))
        self.pvc = np.ndarray((perioud, 1))
        self.input[0, :] = 0
        self.pvc[0, :] = pvc0
        self.data_idx = 0

    def update(self, i, input_, pvc):
        self.input[i + 1, :] = input_
        self.pvc[i + 1, :] = pvc
        self.data_idx = i + 1
        
    def saveData(self):
        input_ = self.input
        pvc = self.pvc
        df_input = pd.DataFrame(input_[:self.data_idx], columns=['Input'])
        df_pvc = pd.DataFrame(pvc[:self.data_idx,0:3], columns=['pos','vel','curr'])
        # 定义储存地址
        # saveAddress = ''
        df_input.to_csv("input", index=False)
        df_pvc.to_csv("pvc", index=False)

def main():
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

        # velocity ff ------------------------------------------------------

        # for i in range(len(server_ip_list)):
        #     dict = {  # 36
        #         'control_position_kp_imm': 0.0,
        #         'control_velocity_kp_imm': 0.04,
        #         'control_velocity_ki_imm': 0.0001,
        #         'control_current_kp_imm': 7.25,  # not work for now
        #         'control_current_ki_imm': 0.08,  # not work for now
        #     }
        #     fi_fsa_v2.set_pid_param_imm(server_ip_list[i], dict)
        #
        # print('\n')
        # time.sleep(1)
        #
        # # move a sin wave
        # count_max = round(100000 * 2 * math.pi)
        # for t in range(0, count_max):
        #     for i in range(len(server_ip_list)):
        #         set_velocity = 30.0  # * math.sin(t / 1000.0)  # [deg/s]
        #         fi_fsa_v2.set_position_control(server_ip_list[i], position=0, velocity_ff=set_velocity)
        #     time.sleep(0.01)
        #
        # time.sleep(1)

        # velocity ff ------------------------------------------------------

        # current ff ------------------------------------------------------

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

        # # set a constant
        # count_max = round(100000 * 2 * math.pi)
        # for t in range(0, count_max):
        #     for i in range(len(server_ip_list)):
        #         pvc = fi_fsa_v2.get_pvc(server_ip_list[i])
        #         k = 0.15
        #         set_current = k*np.sin(pvc[0]/180*3.141592654)
        #         fi_fsa_v2.set_position_control(
        #             server_ip_list[i], position=0, current_ff=set_current
        #         )
        #         print("position = ", pvc[0])
        #     time.sleep(0.01)

        # sweep
        sum_time_s = 100
        dt = 0.002
        saver = Saver(sum_time_s/dt, [0,0,0])
        for t in range(0, sum_time_s/dt):
            for i in range(len(server_ip_list)):
                pvc_now = fi_fsa_v2.get_pvc(server_ip_list[i])
                k = 0.15
                set_current = input_data['current'][t] + k*np.sin(pvc[0]/180*3.141592654)
                saver.update(t,input_data['current'][t],pvc_now)
                fi_fsa_v2.set_position_control(
                    server_ip_list[i], position=0, current_ff=set_current
                )
                # print("position = ", pvc[0])
            time.sleep(dt)
        saver.saveData()

        time.sleep(1)

        # current ff ------------------------------------------------------

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
