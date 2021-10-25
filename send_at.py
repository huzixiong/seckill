from find_ports_at import At
from serial import Serial
import time


class SendAt:
    def __init__(self):
        self.modem_port = At().modem_port


    def send_at(self,port,cmd):
        try:
            cmd = cmd + "\r\n"
            ser = Serial(port, 9600, timeout=0.5, writeTimeout=0.5)
            ser.write(cmd.encode())
            result = ser.readlines()
            ser.close()
            print(result)
        except:
            pass
    def send_at1(self,cmd):
        try:
            cmd = cmd + "\r\n"
            ser = Serial("COM92", 9600, timeout=0.5, writeTimeout=0.5)
            ser.write(cmd.encode())
            result = ser.readlines()
            ser.close()
            print(result)
        except:
            pass



if __name__ == "__main__":
    start = time.time()
    test = SendAt()

    # test.send_at(test.modem_port,"ate")
    test.send_at1("ate")
    end = time.time()
    # print(At().is_qcom)
    total = end - start
    print(total)
