import os
import sys
import time
from math import floor


class ProcessBar:
    def __init__(self, unit=2, max_len=100):
        if max_len > 100:
            raise IllegalUnitException("The maximum of max_len is 100. %s is too big." % max_len)
        if unit < 1:
            raise IllegalUnitException("The minimum of unit is 1. %s is too small." % unit)
        self._unit = floor(unit)
        self._max_len = floor(max_len)
        self._symbol = "#"
        self._status = 0
        self._bar = sys.stdout
        try:
            self._column = os.get_terminal_size().columns
        except (OSError, AttributeError):
            self._column = 60
        self._return = "\r"
        self._name = "Task"

    def init(self):
        self._bar.write("{0}\r".format(' ' * int(self._column)))
        self._bar.flush()
        self._status = 0

    def peek(self, location):
        self.init()
        if location > self._max_len:
            raise IllegalUnitException("location must smaller than max_len.")
        self._status = location
        self.show()

    def show(self, newline=False):
        self._bar.write("{0}: {1}{2} {3}%{4}".format(self._name, self._symbol * self._status,
                                                     " " * int(self._max_len - self._status), self._status,
                                                     self._return))
        if newline:
            self._bar.write("\n")
        self._bar.flush()

    def update(self, span=1, newline=False):
        self._status += span * self._unit
        self.show(newline)
        if self._status >= self._max_len:
            self.done()

    def done(self, prompt=None):
        self.init()
        self._bar.write("%s\n" % prompt if prompt else "{0} done!\n".format(self._name))

    @property
    def task_name(self):
        return self._name

    @task_name.setter
    def task_name(self, name):
        self._name = name

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        if isinstance(symbol, int):
            raise IllegalUnitException("symbol should be a str")
        self._symbol = str(symbol)

    def __repr__(self):
        return "<ProcessBar unit={0}, max_len={1}, symbol={2} [{3}]>".format(self._unit, self._max_len, self._symbol,
                                                                             sys.platform)


class IllegalUnitException(BaseException):
    pass


class NotInitException(BaseException):
    pass


if __name__ == '__main__':
    a = ProcessBar()
    print("Now start test.\nStage one..")
    for n in range(10):
        a.update(5)
        time.sleep(0.3)

    print("Second stage..")
    for n in range(10):
        time.sleep(0.4)
        a.update(4)
        if n == 7:
            a.update(span=0, newline=True)
            print("[!] Error. Stop the stage two")
            break
    print("The last stage...")
    # We need to reinit the processbar for the break just occurred
    # instead of the bar will continue from the breakpoint.
    a.init()
    for n in range(5):
        a.update(5)
        time.sleep(1)
    a.peek(100)
    time.sleep(0.3)
    a.done("Done")
