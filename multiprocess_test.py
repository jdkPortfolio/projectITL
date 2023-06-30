import multiprocessing
import time
def add():
    for i in range(0, 10):
        print (1)
        time.sleep(3)
        # return "add"

def sud():
     for i in range(0, 10):
        print(0)
        time.sleep(3)
        # return "sud"
if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=add)
    p = multiprocessing.Process(name='p', target=sud)
    p1.start()
    p.start()
    # print(val, var)