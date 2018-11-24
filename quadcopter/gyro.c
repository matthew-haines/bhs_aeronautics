#include </Library/Frameworks/Python.framework/Versions/3.6/include/python3.6m/Python.h>
#include <stdio.h>
#include <stdlib.h>

#include <linux/i2c-dev.h>
#include <fcntl.h>

#include <sys/ioctl.h>
#include <sys/types.h>

// C API for Python 

#define ACCEL_X1 0x3b
#define ACCEL_X2 0x3c
#define ACCEL_Y1 0x3d
#define ACCEL_Y2 0x3e
#define ACCEL_Z1 0x3f
#define ACCEL_Z2 0x40

#define GYRO_X1 0x43
#define GYRO_X2 0x44   
#define GYRO_Y1 0x45
#define GYRO_Y2 0x46
#define GYRO_Z1 0x47
#define GYRO_Z2 0x48

#define TEMP1 0x41
#define TEMP2 0x42

#define POWER1 0x6b
#define POWER2 0x6c

static PyObject* sensor(PyObject* self, PyObject* args) {
    int fd;
    char *file = "/dev/i2c-1"; // Where sensor data is stored
    int address = 0x68;

    if ((fd = open(filename, 0_RDWR)) < 0) {
        PyErr_SetString(PyExc_TypeError, "Cannot open file");
        return (PyObject*) NULL;
    }  

    if (ioctl(fd, I2C_SLAVE, address) < 0) {
        PyErrSetString(PyExc_TypeError, "No bus-slave connection");
        return (PyObject*) NULL; 
    }

    int8_t power = i2c_smbus_read_byte_data(fd, MPU_POWER1);
    i2c_smbus_write_byte_data(fd, MPU_POWER1, ~(1 << 6) & power);
}

PyObject* data_fetch() {
    int16_t temp = i2c_smbus_read_byte_data(fd, MPU_TEMP1) << 8 | i2c_smbus_read_byte_data(fd, MPU_TEMP2);

    int16_t xaccel = i2c_smbus_read_byte_data(fd, MPU_ACCEL_XOUT1) << 8 | i2c_smbus_read_byte_data(fd, MPU_ACCEL_X2);
    int16_t yaccel = i2c_smbus_read_byte_data(fd, MPU_ACCEL_YOUT1) << 8 | i2c_smbus_read_byte_data(fd, MPU_ACCEL_Y2);
    int16_t zaccel = i2c_smbus_read_byte_data(fd, MPU_ACCEL_ZOUT1) << 8 | i2c_smbus_read_byte_data(fd, MPU_ACCEL_Z2);

    int16_t xgyro = i2c_smbus_read_byte_data(fd, MPU_GYRO_XOUT1) << 8 | i2c_smbus_read_byte_data(fd, MPU_GYRO_X2);
    int16_t ygyro = i2c_smbus_read_byte_data(fd, MPU_GYRO_YOUT1) << 8 | i2c_smbus_read_byte_data(fd, MPU_GYRO_Y2);
    int16_t zgyro = i2c_smbus_read_byte_data(fd, MPU_GYRO_ZOUT1) << 8 | i2c_smbus_read_byte_data(fd, MPU_GYRO_Z2);

    printf("temp: %f\n", (float)temp / 340.0f + 36.53);
    printf("accel x,y,z: %d, %d, %d\n", (int)xaccel, (int)yaccel, (int)zaccel);
    printf("gyro x,y,z: %d, %d, %d\n\n", (int)xgyro, (int)ygyro, (int)zgyro);
sleep(1);
}