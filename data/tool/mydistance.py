from scipy.spatial.distance import euclidean

# distance 

def mydistance(v1, v2, weight=None):
    if weight is None:
        weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    va = v1.reshape(17, 3)
    vb = v2.reshape(17, 3)
    sum = 0.0
    for i in range(va.shape[0]):
        sum += weight[i] * euclidean(va[i], vb[i])
    return sum
