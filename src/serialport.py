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
        while not self.stopped():
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

class SerialPortSendThread(threading.Thread):
    def __init__(self, parent):
        super(SerialPortSendThread, self).__init__()
        self.parent = parent
        self.thread = threading.Event()

    def stop(self):
        self.thread.set()

    def stopped(self):
        return self.thread.is_set()

    def run(self):
        while not self.stopped():
            try:
                if not self.parent.sendQueue.empty():
                    send_data = self.parent.sendQueue.get()
                    self.parent.serial.write(send_data)
                else:
                    time.sleep(0.01)
            except Exception as e:
                print(e)
                continue

class SerialPort(object):

    def __init__(self) -> None:
        self.serial = None
        self.receiveQueue = queue.Queue(1000)
        self.sendQueue = queue.Queue(1000)

    def open(self, port, baudrate, databit, checkbit, stopbit, xonxoff, rtscts, dsrdtr) -> bool:
        if self.serial is None:
            try:
                self.serial = serial.Serial(port, baudrate, databit, checkbit, stopbit, None, xonxoff, rtscts, None, dsrdtr)
                self.receiveThread = SerialPortReceiveThread(self)
                self.sendThread = SerialPortSendThread(self)
                self.receiveThread.start()
                self.sendThread.start()
                return True
            except Exception as e:
                print(e)
                return False
                

    def close(self) -> bool:
        if self.serial is not None:
            with self.receiveQueue.mutex:
                self.receiveQueue.queue.clear()
            
            with self.sendQueue.mutex:
                self.sendQueue.queue.clear()

            self.sendThread.stop()
            self.receiveThread.stop()
            self.sendThread.join()
            self.receiveThread.join()
            self.serial.close()
            self.serial = None
            return True
        return False
    
    def isOpen(self) -> bool:
        if self.serial is None:
            return False
        return True 

    def write(self, data: bytes) -> None:
        if self.serial is not None:
            self.sendQueue.put(data)

    def read(self) -> bytes:
        if self.serial is not None:
            if not self.receiveQueue.empty():
                return self.receiveQueue.get(False)
            
