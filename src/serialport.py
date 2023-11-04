import serial
import queue
import threading
import time

class SerialPortReceiveThread(threading.Thread):
    def __init__(self, parent):
        super(SerialPortReceiveThread, self).__init__()
        self.parent = parent
        self.thread = threading.Event()

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.is_set()

    def run(self):
        while True:
            if self.stopped():
                break
            try:
                nums = self.parent.serial.in_waiting
                if (nums > 0):
                    recData = self.parent.serial.read(nums)
                else:
                    time.sleep(0.01)
                    continue
                if self.parent.receiveQueue.full():
                    self.parent.receiveQueue.get(False)
                self.parent.receiveQueue.put(recData)
            except Exception as e:
                print(e)
                continue

class SerialPort(object):

    def __init__(self) -> None:
        self.serial = None
        self.receiveQueue = queue.Queue(1000)

    def open(self, port, baudrate, databit, checkbit, stopbit, xonxoff, rtscts, dsrdtr) -> bool:
        if self.serial is None:
            try:
                self.serial = serial.Serial(port, baudrate, databit, checkbit, stopbit, None, xonxoff, rtscts, None, dsrdtr)
                self.receiveThread = SerialPortReceiveThread(self)
                self.receiveThread.start()
                return True
            except Exception as e:
                print(e)
                return False
                

    def close(self) -> bool:
        if self.serial is not None:
            with self.receiveQueue.mutex:
                self.receiveQueue.queue.clear()

            self.receiveThread.stop()
            self.receiveThread.join()
            self.serial.close()
            self.serial = None
            return True
        return False
    
    def isOpen(self) -> bool:
        if self.serial is None:
            return False
        else:
            return True 

    def write(self, data) -> None:
        if self.serial is not None:
            self.serial.write(data)

    def read(self) -> bytes:
        if self.serial is not None:
            if not self.receiveQueue.empty():
                return self.receiveQueue.get(False)
            
