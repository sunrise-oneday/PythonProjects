import numpy as np
from Dog import Dog
a= np.array([[1,2,3],[4,5,6]])
b= np.array([[7,8],[10,11],[12,13]])
print(a.shape)
print(b.shape)
print(np.dot(a,b))
print("Hello World")
print("This is a test")
print("你好，世界")

myDog = Dog('Bob', 'Golden Retriever', 6)   # 提供三个参数
print(myDog.name)
