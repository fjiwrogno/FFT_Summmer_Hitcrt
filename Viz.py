import matplotlib.pyplot as plt
def Visualize(x_data, y_data):
    # 设置大小
    fig = plt.figure(figsize=(15, 20))
    # 设置标题
    fig.suptitle(
            f"controlller "
    )
    plt.plot([0, x_data], y_data, label="y",linestyle="-.")
    # 图例的透明度
    plt.legend(framealpha = 0.5)
    plt.xlabel("Time (s)")
    plt.xlim([0, x_data])
    plt.ylabel("Position (m)")
    plt.grid(True)