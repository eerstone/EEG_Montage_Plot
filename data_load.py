# -*- coding: utf-8 -*-
# @Author: eerstone
# @Date:   2023-12-07 11:39:21
# @Last Modified by:   eerstone
# @Last Modified time: 2024-09-13 11:37:45
import numpy as np
import mne
import scipy.io as scio


def read_dat(filepath=None):
    '''
    读取Neuroscan的dat文件的Sensor Location
    '''
    if filepath == None:
        filepath = "electrode_location_file\\SynAmps2 Quik-Cap64NoM1M2.DAT"
    with open(filepath, "r") as f:
        lines = f.readlines()
    electrodes = {}
    nasion = lpa = rpa = None
    for i, line in enumerate(lines):
        items = line.split()
        if not items:
            continue
        elif len(items) != 4:
            raise ValueError("ERROR reading dat ERROR")
        pos = np.array([float(item) for item in items[1:]])
        if i == 0:
            nasion = pos
        elif i == 1:
            lpa = pos
        elif i == 2:
            rpa = pos
        elif items[0] == "VEO":
            break
        else:
            electrodes[items[0].upper()] = pos
    return mne.channels.make_dig_montage(electrodes, nasion, lpa, rpa)


def read_labelmat(filepath):
    '''
    从dpa.mat文件中导出sensorpos
    '''
    data = scio.loadmat(filepath)
    o_labels = data["labels"][0]
    labels = []
    for i in o_labels:
        val = i[0]
        val = val.upper()
        labels.append(val)
    labels = labels[:-1]
    return labels


def read_montagemat(filepath=None):
    '''
    从curry8 dpa文件中的sensorpos 和label生成montage
    filepath 为自己导出的sensorpos 和 labels的合并mat'
    导出时去掉m1 m2
    '''
    if filepath == None:
        filepath = "electrode_location_file\\Quik_Cap_Neo.mat"
    data = scio.loadmat(filepath)
    labels = read_labelmat(filepath)
    sensorpos = data["sensorpos"]
    sensorpos = np.transpose(sensorpos)
    # 暂时照抄read_dat中的nasion，lpa与rpa
    nasion = np.array([0.100031, 9.518287, 0])
    lpa = np.array([-6.902262, 0, 0])
    rpa = np.array([6.902262, 0, 0])
    channels = {}
    for i in range(64):
        key = labels[i]
        sensorpos[i][1] = -sensorpos[i][1]
        # 暂不清楚之前为啥 / 10 是原始数据比较大？
        channels[key] = sensorpos[i] / 10
    ref = ["M1", "M2"]
    labels.remove("M1")
    labels.remove("M2")
    for r in ref:
        if r in channels:
            del channels[r]
    return mne.channels.make_dig_montage(channels, nasion, lpa, rpa)


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
