import serial, os, time, sys, glob, datetime
import RPi.GPIO as GPIO


def logfilename():
    now = datetime.datetime.now()
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("dir path:",dir_path)
    return os.path.join(dir_path,'logs/NMEA_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.nmea' % \
                (now.year, now.month, now.day,
                 now.hour, now.minute, now.second))
    

def parse_nmea_sentence(nmea_sentence):
    # Split the NMEA sentence by commas

    fields = nmea_sentence.strip().split(',')
    print(fields)
    # Extract the validity (status) and speed

    type = fields[0]

    if type != "$GPRMC":
        return None, None, None
    
    validity = fields[2]
    speed = fields[7]
    
    return type, validity, speed

def blink_led(times):
    for i in range (times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)



# Set up GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 18 # Change this to the GPIO pin your LED is connected to
GPIO.setup(LED_PIN, GPIO.OUT)

blink_led(3)

# Error reading serial port TypeError: write() argument must be str, not bytes

try:
    while True:

        port = "/dev/ttyUSB0"
        try:
            # try to read a line of data from the serial port and parse
            with serial.Serial(port, 9600, timeout=1) as ser:
                # 'warm up' with reading some input
                for i in range(10):
                    ser.readline()
                

                # log data
                outfname = logfilename()

                
                #with open(outfname, 'a+') as f:
                    # loop will exit with Ctrl-C, which raises a
                    # KeyboardInterrupt

                while True:
                    line = ser.readline().decode('utf-8')
                    
                    try:
                        msg = parse_nmea_sentence(line)
                        print("message parse out:",msg)

                        if msg[0] == "$GPRMC":
                            # Get the current system clock timestamp with microsecond precision
                            dt = datetime.datetime.now()
                            timestamp = dt.strftime("[%Y-%m-%d %H:%M:%S.%f]")
                            # Append the timestamp to the GPS data string
                            timestamped_line = f"{timestamp} {line}\n"
                            # Log the timestamped GPS data
                            print(timestamped_line)
                            with open(outfname, 'a+') as f:
                                f.write(timestamped_line)

                            if msg[1] != 'V':
                                print("Valid data received")
                                # Turn on the LED
                                GPIO.output(LED_PIN, GPIO.HIGH)
                            else:
                                print("Invalid data received")
                                # Turn off the LED
                                GPIO.output(LED_PIN, GPIO.LOW)
                            
                            # the LED task and the validity should be checked here.

                    except Exception as e:
                        print("Expection occured:", e)

                    print(line)
            
        except Exception as e:
            sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
           

        sys.stderr.write('Scanned all ports, waiting 10 seconds...press Ctrl-C to quit...\n')
        time.sleep(10)

except KeyboardInterrupt:
    sys.stderr.write('Ctrl-C pressed, exiting port scanner\n')




# split, strip






# def parse_nmea_sentence(nmea_sentence):
#     # Split the NMEA sentence by commas
#     fields = nmea_sentence.split(',')
#     
#     # Extract the validity (status) and speed
#     validity = fields[2]
#     speed = fields[7]
#     
#     return validity, speed
# 
# # Example NMEA sentences
# nmea_sentence1 = '$GPRMC,134632.00,A,3825.59916,N,02708.07357,E,0.332,,170424,,,A*72'
# nmea_sentence2 = '$GPRMC,134632.34,V,,,,,,,170424,,,N*7F'
# 
# # Parse the sentences and print the extracted information
# validity1, speed1 = parse_nmea_sentence(nmea_sentence1)
# validity2, speed2 = parse_nmea_sentence(nmea_sentence2)
# 
# print(f"Validity: {validity1}, Speed: {speed1}")
# print(f"Validity: {validity2}, Speed: {speed2}")





# import serial, os, time, sys, glob, datetime
# import RPi.GPIO as GPIO
# 
# def logfilename():
#     now = datetime.datetime.now()
#     return 'NMEA_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.nmea' % \
#                 (now.year, now.month, now.day,
#                  now.hour, now.minute, now.second)
# 
# def parse_nmea_sentence(nmea_sentence):
#     # Split the NMEA sentence by commas
#     fields = nmea_sentence.split(',')
#     
#     # Check if the sentence is a $GPRMC sentence
#     if fields[0] != '$GPRMC':
#         return None, None
#     
#     # Extract the validity (status) and speed
#     validity = fields[2]
#     speed = fields[7]
#     
#     return validity, speed
# 
# # Set up GPIO
# GPIO.setmode(GPIO.BCM)
# LED_PIN = 18 # Change this to the GPIO pin your LED is connected to
# GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.output(LED_PIN, GPIO.HIGH)
# time.sleep(1)
# GPIO.output(LED_PIN, GPIO.LOW)
# 
# 
# while True:
#     port = "/dev/serial0"
#     try:
#         with serial.Serial(port, 9600, timeout=1) as ser:
#             
#             outfname = logfilename()
#             with open(outfname, 'a+') as f:
#                 while True:
#                     line = ser.readline()
#                     decoded_line = line.decode('ascii', errors='replace').strip()
#                     
#                     validity, speed = parse_nmea_sentence(decoded_line)
#                     
#                     
# 
#                     dt = datetime.datetime.now()
#                     timestamp = dt.strftime("[%Y-%m-%d %H:%M:%S.%f]")
#                     timestamped_line = f"{timestamp} {decoded_line}\n"
#                     print(timestamped_line)
#                     f.write(timestamped_line)
#                     
#                     if validity != 'V':
#                         print("Valid data received")
#                         GPIO.output(LED_PIN, GPIO.HIGH)
#                     else:
#                         print("Invalid data received")
#                         GPIO.output(LED_PIN, GPIO.LOW)
#                     
#                     print(decoded_line)
#         
#     except Exception as e:
#         sys.stderr.write('Error reading serial port %s: %s\n' % (type(e).__name__, e))
#        
#     sys.stderr.write('Scanned all ports, waiting 10 seconds...press Ctrl-C to quit...\n')
#     time.sleep(10)

