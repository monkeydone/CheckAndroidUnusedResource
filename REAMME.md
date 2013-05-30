#目标
#功能
- 提供一个android工程，找到这个工程中，没有被显示调用过的类文件，布局文件，资源文件
- 提供一个参数将这些废弃的文件以test开头命名。
- 再次编译这个工程，如果确定没有错误，可以删除掉这些无用的文件。如果发现有错误，可以再次重命名文件，进行修复。
#使用方法
```
./checkResource.py -h
```
##测试有多少废弃文件
```
./checkResource.py -p your_project -t
```
##处理这些废弃文件
```
./checkResource.py -p your_project -r
```
##演示
目前提供了一个工程来演示这个脚本的功能
```
./checkResource.py -p ResourceExample -t
```

