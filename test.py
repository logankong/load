import random
import time

class test(object):
    def __init__(self):
        super(test, self).__init__()
        # self.arg = self.random_without_same(int(300*10/100), 3)

    def random_without_same(self, ma, num, mi=0):
        temp = list(range(mi, ma))
        print(temp)
        random.shuffle(temp)

        return temp[0:num]

    def abc(self):
        a = list(range(9))
        b = []

        for x in range(1, 7):
            retD = list(set(a).difference(set(b)))
            if retD:
                print('2222')
                return 'abc'
            print('11111111111111')
            new = random.sample(retD, 3)
            print(new)
            b.extend(new)
            if len(b) == len(a):
                b = []


if __name__ == '__main__':
    file = 'result_' + format(time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time())))
    print(file)
    b = 123
    print("a " + str(b) + " c")
    test = test()
    # test.abc()
