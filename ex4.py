import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
start_time=time.time()
# 使用 seaborn 加载 iris 数据集
iris = sns.load_dataset('iris')

# 显示数据集的前几行
print("Data preview:")
print(iris.head())

# 显示数据集的基本统计描述
print("\nBasic statistical details:")
print(iris.describe())

# 数据集的类别分布
print("\nSpecies count:")
print(iris['species'].value_counts())

# 画出各个特征的箱线图
plt.figure(figsize=(8, 6))
sns.boxplot(data=iris)
plt.title('Boxplot of Iris Features')
plt.show()

# 画出特征之间的关系
sns.pairplot(iris, hue='species')
plt.title('Pairplot of Iris Features by Species')
plt.show()

end_time=time.time()
print(end_time-start_time)