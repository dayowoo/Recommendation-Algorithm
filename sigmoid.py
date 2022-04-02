import numpy as np
import matplotlib.pyplot as plt



# 프로필 설정한 경우
def isSigmoid(x):
    # exp(-x) = exp^-x
    return 2 / (1 +np.exp(-x))


# 프로필 설정하지 않은 경우
def noneSigmoid(x):
    return 2 / (1 +np.exp(-x)) - 1


# 0에서 5까지 0.1씩 증가
x = np.arange(0, 5.0, 0.1)
isY = isSigmoid(x)
noneY = noneSigmoid(x)


# plt.plot(x, isY, color='blue')
plt.plot(x, noneY, color='red')
# y축 값의 범위 설정
plt.ylim(-0.1, 2.1)

# x, y축 이름 설정
plt.xlabel('f')
plt.ylabel('S')
# plt.show()




