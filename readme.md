## 简介 Introduction

传统的电极展示方式可以使用eeglab工具的地形图或者mne库的montage plot。笔者出于如下需求对mne库的montage plot函数进行了魔改。

- 各电极独立分析与观察。人脑不同分区所反映的功能活动可能是完全不同的。因此使用地形图的方式会掩盖某些关键点所具有的独特信息（当然，相邻电极反映的脑活动可能具有相似性但并不绝对）。虽然脑电波本身的空间分辨率就不高，但这样做会更进一步削减图形反映的信息量。并且电极图上选择性地展示关键电极的名称也是必要的。
- 特定数据的定制化展示。在每个电极上，我们可能不仅关心传统的电极强度，我们可能想观察每个电极信号与某个其他信息的相关性强度，或者是任意其他以电极为单位的指定数据。
- 美观优化。mne过去的montage plot函数展示出来不够美观。仅能显示黑红色。如果针对给定条件的数据我想使用其他的颜色呢。这里支持使用任意colorbar。

## 版本信息 Requirement

mne == 0.21, numpy,  scipy, matplotlib

## 结构 Structure

- data_load.py:  从原始电极文件，如dat文件，进行电极读取
- montage_plot.py: 绘制电极图与电极名称

## 示例图 Example Figure

  

![image-20231207174528371](C:\Users\Brandon_pan\AppData\Roaming\Typora\typora-user-images\image-20231207174528371.png)







