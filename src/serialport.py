import serial
import queue
import threading
import time

class SerialPortReceiveThread(threading.Thread):
    def __init__(self, serial=None, readQueue=None):
        super(SerialPortReceiveThread, self).__init__()
        self.serial = serial
        self.readQueue = readQueue
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            try:
                if self.serial.in_waiting > 0:
                    recData = self.serial.read(self.serial.in_waiting)
                    if self.readQueue.full():
                        self.readQueue.get_nowait()
                    self.readQueue.put(recData)
                else:
                    time.sleep(0.01)  # No data, sleep to reduce CPU load.
            except Exception as e:
                print(e)
                continue

class SerialPortSendThread(threading.Thread):
    def __init__(self, serial=None, writeQueue=None):
        super(SerialPortSendThread, self).__init__()

        self.serial =serial
        self.writeQueue = writeQueue
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            try:
                send_data = self.writeQueue.get(True, 0.1)
                self.serial.write(send_data)
            except queue.Empty:
                continue
            except Exception as e:
                print(e)
                continue

class SerialPort(object):

    def __init__(self) -> None:
        self.serial = None
        self.receiveQueue = queue.Queue(2000)
        self.sendQueue = queue.Queue(2000)

    def open(self, port, baudrate, databit, checkbit, stopbit, xonxoff, rtscts, dsrdtr) -> bool:
        if self.serial is None:
            try:
                self.serial = serial.Serial(port, baudrate, databit, checkbit, stopbit, None, xonxoff, rtscts, None, dsrdtr)
                self.receiveThread = SerialPortReceiveThread(self.serial, self.receiveQueue)
                self.sendThread = SerialPortSendThread(self.serial, self.sendQueue)
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
            
