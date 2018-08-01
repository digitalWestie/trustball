import threading
import sys
import RPi.GPIO as GPIO

class StopThread(StopIteration): pass

threading.SystemExit = SystemExit, StopThread

class Thread2(threading.Thread):
    def stop(self):
        GPIO.cleanup()
        self.__stop = True

    def _bootstrap(self):
        if threading._trace_hook is not None:
            raise ValueError('Cannot run thread with tracing!')
        self.__stop = False
        sys.settrace(self.__trace)
        super()._bootstrap()

    def __trace(self, frame, event, arg):
        if self.__stop:
            raise StopThread()
        return self.__trace
