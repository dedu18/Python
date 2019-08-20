# 有返回值
def sum(a, b, c=1):
    return a + b + 1;

sum_num = sum(1, 2)
print(sum_num)


# 无返回值
def printnum(str):
    print(str)

print(printnum("hello, method define!") == None)

###################CLASS DEFINE
class Animal(object):
    pass

class Fish(object):
    def __init__(self, name):
        self.__name = name
    def eat(self, food):
        print(self.__name + " is eatting " + food)

bird = Animal()
print(bird)

godFish = Fish("GodFish")
# print(godFish.name)
godFish.eat("apple")

#################


class CaptureManger(object):

    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):
        # 单下划线保护变量（子类可访问），双下划线私有变量（子类不可访问）
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview



