import time
from qhanutils.timer import Timer
from qhanutils.logger import get_logger


def main():
    t = Timer()

    t.set_unit('s')
    for i in range(10):
        t.tic('a')
        time.sleep(0.1)
        t.toc('a')
        t.tic('b')
        time.sleep(0.01)
        t.toc('b')
        
    t.summary()


if __name__ == '__main__':
    main()