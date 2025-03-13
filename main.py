"""
Bike Telemetry Project
Converted from Arduino to Python for new microprocessor platform
"""

import time
import datetime
import os
'''
import board
import busio
import digitalio
import adafruit_sdcard
import storage
import adafruit_rtc
import adafruit_ism330dhcx
'''


class BikeTelemetry:
    def __init__(self):
        # Pin definitions (these will need to be updated based on your specific hardware)
        self.LINEAR_POT_FRONT = 'A1'  # Analog pin
        self.LINEAR_POT_REAR = 'A2'  # Analog pin
        self.BATTERY_PIN = 'A7'  # Analog pin
        self.SD_CARD_DETECT = 7  # Digital pin
        self.START_BUTTON = 10  # Digital pin
        self.RGB_RED = 13
        self.RGB_GREEN = 12
        self.RGB_BLUE = 11

        # File management
        self.file_name = "run1.txt"
        self.data_log = None

        # Timing variables
        self.start_time = 0
        self.stop_time = 0
        self.total_time = 0
        self.previous_millis_record = 0
        self.time_period_record = 1  # 1ms = 1000Hz record rate

        # Calibration variables
        self.rear_calibration_initial = 0
        self.front_calibration_initial = 0

        # Button debounce variables
        self.last_button_state = 0
        self.last_debounce_time = 0
        self.debounce_delay = 10
        self.button_state = 0
        self.led_state = 1

        # Setup
        self.setup_gpio()
        self.setup_sd_card()
        self.setup_rtc()
        self.setup_accelerometer()

        # Initial calibration
        self.flash_led()
        self.check_battery_voltage()
        self.set_rgb_color(0, 1, 0)  # Green
        time.sleep(2)
        self.rear_calibration_initial = self.read_analog(self.LINEAR_POT_REAR)
        self.front_calibration_initial = 1023 - self.read_analog(self.LINEAR_POT_FRONT)
        self.set_rgb_color(0, 0, 0)  # Off
        time.sleep(5)

    def setup_gpio(self):
        """Setup GPIO pins (this would be platform-specific)"""
        print("Setting up GPIO pins")
        # In a real implementation, you would initialize your GPIO pins here
        # For example with RPi.GPIO or CircuitPython's digitalio

    def setup_sd_card(self):
        """Initialize SD card"""
        print("Setting up SD card")
        try:
            # This is a placeholder for the actual SD card initialization
            # In CircuitPython, you might use something like:
            # spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            # cs = digitalio.DigitalInOut(board.SD_CS)
            # sdcard = adafruit_sdcard.SDCard(spi, cs)
            # vfs = storage.VfsFat(sdcard)
            # storage.mount(vfs, "/sd")
            print("SD card initialized")
        except Exception as e:
            print(f"SD card initialization failed: {e}")
            self.set_rgb_color(0, 0, 1)  # Blue = error
            time.sleep(3)
            self.set_rgb_color(0, 0, 0)  # Off

    def setup_rtc(self):
        """Initialize real-time clock"""
        print("Setting up RTC")
        try:
            # This is a placeholder for the actual RTC initialization
            # In CircuitPython, you might use:
            # i2c = busio.I2C(board.SCL, board.SDA)
            # self.rtc = adafruit_rtc.DS3231(i2c)
            print("RTC initialized")
        except Exception as e:
            print(f"RTC initialization failed: {e}")
            self.set_rgb_color(1, 0, 1)  # Purple = RTC error
            time.sleep(3)
            self.set_rgb_color(0, 0, 0)  # Off

    def setup_accelerometer(self):
        """Initialize the ISM330DHCX accelerometer and gyroscope"""
        print("Setting up accelerometer")
        try:
            # This is a placeholder for the actual accelerometer setup
            # In CircuitPython, you might use:
            # i2c = busio.I2C(board.SCL, board.SDA)
            # self.ism = adafruit_ism330dhcx.ISM330DHCX(i2c)
            print("Accelerometer initialized")
        except Exception as e:
            print(f"Accelerometer initialization failed: {e}")
            self.set_rgb_color(1, 0, 1)  # Purple = sensor error
            time.sleep(3)
            self.set_rgb_color(0, 0, 0)  # Off

    def read_analog(self, pin):
        """Read analog value (placeholder)"""
        # This would be implemented based on your specific hardware
        # For example with CircuitPython's analogio
        return 512  # Placeholder value

    def read_digital(self, pin):
        """Read digital value (placeholder)"""
        # This would be implemented based on your specific hardware
        return False  # Placeholder value

    def set_rgb_color(self, red, green, blue):
        """Set RGB LED color"""
        print(f"Setting LED: R={red}, G={green}, B={blue}")
        # This would be implemented based on your specific hardware
        # For CircuitPython, you might use digitalio outputs

    def flash_led(self):
        """Flash LED white for testing"""
        for _ in range(20):
            self.set_rgb_color(1, 1, 1)  # White
            time.sleep(0.05)
            self.set_rgb_color(0, 0, 0)  # Off
            time.sleep(0.05)

    def get_button_state(self):
        """Get debounced button state"""
        reading = self.read_digital(self.START_BUTTON)

        current_time = time.monotonic() * 1000  # Convert to milliseconds

        if reading != self.last_button_state:
            self.last_debounce_time = current_time

        if (current_time - self.last_debounce_time) > self.debounce_delay:
            if reading != self.button_state:
                self.button_state = reading
                if self.button_state:  # If HIGH
                    self.led_state = not self.led_state

        self.last_button_state = reading
        return self.led_state

    def check_battery_voltage(self):
        """Check battery voltage and warn if low"""
        battery_value = self.read_analog(self.BATTERY_PIN)
        # Convert to voltage (this calculation will depend on your hardware)
        battery_voltage = battery_value * 6.6 / 1024

        if battery_voltage < 3.3:  # Low battery
            self.set_rgb_color(1, 1, 0)  # Yellow
            time.sleep(2)
            self.set_rgb_color(0, 0, 0)  # Off

        return battery_voltage

    def open_new_file(self):
        """Open a new data file with unique name"""
        # Check if file exists and create new name if needed
        file_name = self.file_name
        base_name = file_name.split('.')[0][:3]  # Get base name (e.g., "run")
        extension = ".txt"
        counter = 1

        try:
            while os.path.exists(f"/sd/{file_name}"):
                counter += 1
                file_name = f"{base_name}{counter}{extension}"

            # Would open the file here in a real implementation
            # self.data_log = open(f"/sd/{file_name}", "w")
            print(f"New file created: {file_name}")
            return file_name
        except Exception as e:
            print(f"File error: {e}")
            self.set_rgb_color(0, 0, 1)  # Blue = error
            time.sleep(3)
            self.set_rgb_color(0, 0, 0)  # Off
            return None

    def start_run(self):
        """Start a new recording run"""
        self.file_name = self.open_new_file()
        if not self.file_name:
            return False

        # Would open file for writing here in a real implementation
        print(f"Starting run with file: {self.file_name}")

        # Write header information
        print("///HEADER///")
        print(f"Rear sus recording frequency : {1000 / self.time_period_record}")
        print(f"Front sus recording frequency : {1000 / self.time_period_record}")
        print(f"RB:250:test2,FB:250:test3")

        print(f"Rear Calibration Value : {self.rear_calibration_initial}")
        print(f"Front Calibbration Value : {self.front_calibration_initial}")

        print("///RUN COMMENTS///")
        print(" ")

        print("///RUN DATA///")
        time.sleep(1)
        self.start_time = time.monotonic() * 1000  # Convert to milliseconds
        return True

    def record_data(self):
        """Record sensor data to file"""
        current_time = time.monotonic() * 1000  # Convert to milliseconds

        if (current_time - self.previous_millis_record) >= self.time_period_record:
            self.previous_millis_record = current_time

            # Would read acceleration and gyro data in a real implementation
            accel_x, accel_y, accel_z = 0, 0, 0  # Placeholder values
            gyro_x, gyro_y, gyro_z = 0, 0, 0  # Placeholder values

            # Read suspension position
            rear_pos = self.read_analog(self.LINEAR_POT_REAR)
            front_pos = 1023 - self.read_analog(self.LINEAR_POT_FRONT)

            # TODO : change the formatting of this line so it is more intuitive ? why are there 0s at the end
            data_line = f"{accel_x},{accel_y},{accel_z},{gyro_x},{gyro_y},{gyro_z},{rear_pos},{front_pos},0.0,0.0"
            print(f"Data: {data_line}")

            # Would write to file in a real implementation
            return True
        return False

    def finish_run(self):
        """Finish the current recording run"""
        self.stop_time = time.monotonic() * 1000  # Convert to milliseconds
        self.total_time = self.stop_time - self.start_time

        print(f"Run completed. Duration: {self.total_time}ms")

        # Would write final data and close file in a real implementation
        # self.data_log.flush()
        # self.data_log.close()


    def run(self):
        """Main run loop"""
        while True:
            button_state = self.get_button_state()
            button_state = 0
            if button_state == 0:  # Recording mode
                self.set_rgb_color(1, 0, 0)  # Red = recording
                if self.start_run():
                    # Record until button state changes
                    while self.get_button_state() == 0:
                        self.record_data()
                    self.finish_run()

            else:  # Standby mode
                self.set_rgb_color(0, 1, 0)  # Green = ready
                # Check for upload request
                # In a real implementation, you would check for serial data here

                # Placeholder for upload detection
                # if serial_data_available():


if __name__ == "__main__":
    telemetry = BikeTelemetry()
    try:
        telemetry.run()
    except KeyboardInterrupt:
        print("Program terminated by user")
    except Exception as e:
        print(f"Error: {e}")
        # Flash error code
        telemetry.set_rgb_color(0, 0, 1)  # Blue = error
        time.sleep(3)
        telemetry.set_rgb_color(0, 0, 0)  # Off