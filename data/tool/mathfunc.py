import numpy as np
import pandas as pd
import scipy
from scipy import stats
from sklearn import preprocessing

import project_config as cf


def analysis(res, gra, pre_process=None):
    result = pd.read_table(res, sep=',', header=None)
    # df=pd.read_table('/Users/yanting/Desktop/Projects/Golf/detect-new/data/Result.txt', sep=',', header=None)
    # grades = pd.read_table(gra, sep='\t', header=None)
    grades = pd.read_csv(gra, sep=',', header=None)

    # fun1  preprocessing.minmax_scale(X, feature_range=(0, 1), axis=0, copy=True)
    # fun2  preprocessing.scale(X,axis=0, with_mean=True, with_std=True, copy=True)
    if pre_process is not None:
        d_a = pre_process(result[1])
        d_b = pre_process(grades[1])
    else:
        d_a = result[1]
        d_b = grades[1]

    # df = pd.DataFrame({'x': d_a, 'y': d_b})
    df = pd.DataFrame({'x': d_a[:190], 'y': d_b[:190]})

    return [np.mean(df.x), np.var(df.x), scipy.stats.pearsonr(df.x, df.y),
            scipy.stats.spearmanr(df.x, df.y),
            scipy.stats.kendalltau(df.x, df.y)]


if __name__ == "__main__":
    gra_p = f'{cf.PROJECT_ROOT}data/grades/Grading.csv'
    res_p = f"{cf.PROJECT_ROOT}data/grades/Resultstd.txt"
    # res_p = f"{cf.PROJECT_ROOT}doc/backup/grades/Result.txt"
    # res_p = f"{cf.PROJECT_ROOT}doc/backup/grades/Result.txt"

    ans = analysis(res_p, gra_p)

    # use minmax_scale
    # ans = analysis(res_p, gra_p, lambda x: preprocessing.minmax_scale(x, feature_range=(0, 1), axis=0, copy=True))
    # ans = analysis(res_p,gra_p,lambda x :preprocessing.scale(x,axis=0, with_mean=True, with_std=True, copy=True))
    print(f"mean {ans[0]}, var {ans[1]}\npearson\nr {ans[2][0]},p {ans[2][1]}", '\n', ans[3], '\n', ans[4])

    # analysis(res_p,gra_p,lambda x :preprocessing.scale(x,axis=0, with_mean=True, with_std=True, copy=True))
