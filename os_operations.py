# ========================================================================
# python 的目录相关操作
# ========================================================================

import os
print(os.listdir(os.getcwd())) # 获取目录内容
os.mkdir(path='./denis0726') # 创建新目录
os.mkdir(path='./spider/test_demo') # 在当前目录下创建名为:test_demo的目录
os.rmdir(path='./spider/test_demo') # 删除目录
print(os.path.isdir('./spider/test_demo')) # 判断目录是否存在

# 切换目录写入文件
os.chdir('./spider/test_demo')
with open('1.txt', 'a')as f:
    f.write('人在塔在!')

# 判断目录是否存在(绝对路径)
print(os.path.exists('/'))
