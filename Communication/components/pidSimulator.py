from pid import AUVPID
import numpy as np
import time
import matplotlib.pyplot as plt

p = 1.167
i = 0
d = 0

if __name__ == '__main__':
    controller = AUVPID(6, p, i, d)
    currentPos = 0
    pos_list = np.array([0])

    for i in range(50):
        feedback = controller.pid(currentPos)
        currentPos += feedback
        pos_list = np.append(pos_list, currentPos)
        time.sleep(0.1)

    plt.plot(pos_list)
    print(pos_list)
    plt.show()