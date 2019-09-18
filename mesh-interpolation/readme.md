# 使用环境搭建

## 安装 python 3.7.4 及以上版本

    [下载地址](https://www.python.org/downloads/)

## 使用 pip 安装相关包

```
    pip install numpy scipy
```

## 安装 blender 2.80 及以上版本

    [下载地址](https://www.blender.org/download/)

# 脚本使用

## 插值脚本

    获取到形如'拟合点(1).xlsx'的原始数据，注意其中5为数据点排列小周期，后期会使用这个周期值来进行数据点的面生成。

    剔除第一列和第一行，只保留下数据点部分，另存为 1.csv。

    使用 notepad++ 打开 spherical/interpolateSpherical.py。将 1.csv 所在文件夹的绝对路径复制到第 10 行 directory 中替换，注意保留前缀 r 和前后单引号。将第 14 行 columns_count 值设为之前提到的原始数据的排列小周期值。可选修改第 15 行 intersection 值，该值越大，插入点的数量就越多。修改完之后保存。

    在脚本目录下 shift+ 右键打开一个命令行提示符或者 powershell 窗口，执行 interpolateSpherical.py 脚本。

    ```
    python interpolateSpherical.py
    ```

    执行正常则会输出两行相同的数字（默认为33），这个是生成的数据点集的新的排列小周期，这个记下来，后面有用。同时在 mesh-interpolation 目录下会生成或者更新 2.csv 文件，这里是插值后的坐标。

## blender 从 csv 文件生成 mesh 的脚本

    开启 blender，切换到 Scripting tab，点击 + New 按钮。使用 notepad++ 打开 mesh-interpolation 目录下的 blenderScript.py 文件。全选复制到 blender 刚才新建的文本框中。修改第 8 行中的绝对路径。修改第 38 行的 new_column_count 的值为第 6 行代码中 filename 指向的文件的数据点小周期。点击 Scripting tab 右上角的 run script 按钮。正常的话就会生成一个正常的曲面。如果生成点位置是正确的但是面片缝合有问题，需要检查 blender 脚本中第 38 行值是不是正确。

## 导出

    在场景中选中 mesh，点击 File --> Export --> .obj。左下方勾选 Selection Only，取消勾选 Write Materials。在右边更改路径和文件名，点击 Export OBJ 即可。之后可以将此 obj 文件导入到任何支持该文件格式的软件或者系统中。
