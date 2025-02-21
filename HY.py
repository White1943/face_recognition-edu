def test():
    return 2,3
print(test())
print(*test())
print(format(test()))
# print(format(*test()))
print("{:.2f} hh {:.1f}".format(*test()))
# 这个*test，中的*，不是c语言里的指针，而是 是解包操作符，把元组解开成独立的参数. 将（2，3）拆解为 2 3 输出结果同下行函数
print("{:.2f} hh {:.1f}".format(2 ,3))
