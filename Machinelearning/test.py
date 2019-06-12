import numpy as np


def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

a = ['325', '0', '456', '0']
array = []
for item2 in a:
    b = int2bin(int(item2))
    for c in b:
        array.append(int(c))
array_to_mat = np.mat(array)  # 数组转矩阵
print(array_to_mat)
