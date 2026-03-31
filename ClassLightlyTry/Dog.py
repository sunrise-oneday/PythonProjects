class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.age = age
        self.breed = breed   # 保存品种
    def sit(self):
        print(self.name+'is now sitting.')
    def roll_over(self):
        print(self.name+'rolled over.')