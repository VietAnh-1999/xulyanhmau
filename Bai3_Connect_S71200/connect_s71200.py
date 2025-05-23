from time import sleep
#from snap7 import Snap7Exception
import snap7
plc = snap7.client.Client()
plc.connect("192.168.0.154",0,1)
byte = bytearray([0,1])

while True:
    data = plc.db_read(1,0,6) # đọc tu byte 0 toi byte 6 của DB1
    result_int = snap7.util.get_int(data,0)
    print(f"value: {result_int}")
    #  print('Value:' + str(snap7.util.get_int(seft,1))) 
    sleep(1)