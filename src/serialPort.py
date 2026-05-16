import serial
import queue
import threading
import time
import logging

logger = logging.getLogger(__name__)


class SerialPortReceiveThread(threading.Thread):
    def __init__(self, serial_port=None, read_queue=None, owner=None):
        super(SerialPortReceiveThread, self).__init__(daemon=True)
        self.serial = serial_port
        self.readQueue = read_queue
        self.owner = owner
        self.stopEvent = threading.Event()

    def stop(self):
        self.stopEvent.set()

    def _mark_connection_lost(self):
        if self.owner is not None:
            self.owner._connection_lost = True

    def run(self):
        while not self.stopEvent.is_set():
            try:
                if self.serial.in_waiting > 0:
                    recData = self.serial.read(self.serial.in_waiting)
                    if self.readQueue.full():
                        self.readQueue.get_nowait()
                    self.readQueue.put(recData)
                else:
                    time.sleep(0.01)  # No data, sleep to reduce CPU load.
            except serial.SerialException:
                logger.warning("Serial receive thread: connection lost")
                self._mark_connection_lost()
                break
            except Exception:
                logger.exception("Serial receive thread error")
                continue


class SerialPortSendThread(threading.Thread):
    def __init__(self, serial_port=None, write_queue=None, owner=None):
        super(SerialPortSendThread, self).__init__(daemon=True)
        self.serial = serial_port
        self.writeQueue = write_queue
        self.owner = owner
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def _mark_connection_lost(self):
        if self.owner is not None:
            self.owner._connection_lost = True

    def run(self):
        while not self.stop_event.is_set():
            try:
                send_data = self.writeQueue.get(True, 0.1)
                self.serial.write(send_data)
            except queue.Empty:
                continue
            except serial.SerialException:
                logger.warning("Serial send thread: connection lost")
                self._mark_connection_lost()
                break
            except Exception:
                logger.exception("Serial send thread error")
                continue


class SerialPort(object):

    def __init__(self) -> None:
        self.serial = None
        self.receiveQueue = queue.Queue(2000)
        self.sendQueue = queue.Queue(2000)
        self._connection_lost = False
        self.port_name = ""

    def open(self, port, baudrate, databit, checkbit, stopbit, xonxoff, rtscts, dsrdtr) -> bool:
        if self.serial is None:
            try:
                self._connection_lost = False
                self.port_name = port
                self.serial = serial.Serial(
                    port, baudrate, databit, checkbit, stopbit,
                    None, xonxoff, rtscts, None, dsrdtr
                )
                self.receiveThread = SerialPortReceiveThread(
                    self.serial, self.receiveQueue, self
                )
                self.sendThread = SerialPortSendThread(
                    self.serial, self.sendQueue, self
                )
                self.receiveThread.start()
                self.sendThread.start()
                return True
            except Exception:
                logger.exception("Failed to open serial port %s", port)
                self.serial = None
                self.port_name = ""
                return False
        return False

    def reconfigure(self, baudrate, databit, checkbit, stopbit, xonxoff, rtscts, dsrdtr) -> bool:
        if self.serial is None:
            return False
        try:
            self.serial.baudrate = baudrate
            self.serial.bytesize = databit
            self.serial.parity = checkbit
            self.serial.stopbits = stopbit
            self.serial.xonxoff = bool(xonxoff)
            self.serial.rtscts = bool(rtscts)
            self.serial.dsrdtr = bool(dsrdtr)
            return True
        except Exception:
            logger.exception("Failed to reconfigure serial port")
            return False

    def close(self) -> bool:
        if self.serial is not None:
            with self.receiveQueue.mutex:
                self.receiveQueue.queue.clear()

            with self.sendQueue.mutex:
                self.sendQueue.queue.clear()

            self.sendThread.stop()
            self.receiveThread.stop()
            self.sendThread.join(timeout=2.0)
            self.receiveThread.join(timeout=2.0)
            try:
                if self.serial.is_open:
                    self.serial.close()
            except Exception:
                logger.exception("Error while closing serial port")
            self.serial = None
            self.port_name = ""
            return True
        return False

    def isOpen(self) -> bool:
        return self.serial is not None

    def check_connection_health(self) -> bool:
        if self.serial is None:
            return False
        if self._connection_lost:
            return False
        if hasattr(self, "receiveThread") and not self.receiveThread.is_alive():
            return False
        try:
            return self.serial.is_open
        except Exception:
            return False

    def write(self, data: bytes) -> None:
        if self.serial is not None:
            self.sendQueue.put(data)

    def read_all_pending(self) -> bytes:
        if self.serial is None:
            return b""

        chunks = []
        while not self.receiveQueue.empty():
            try:
                chunks.append(self.receiveQueue.get_nowait())
            except queue.Empty:
                break
        return b"".join(chunks)
