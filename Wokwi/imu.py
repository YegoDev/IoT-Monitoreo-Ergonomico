import utime
import ustruct

class Accel:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
        utime.sleep_ms(100)

    @property
    def accel(self):
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)
        x, y, z = ustruct.unpack('>hhh', data)
        scale = 16384.0
        return Accel(x / scale, y / scale, z / scale)