import MFRC522

import RPi.GPIO as GPIO
import signal

continue_reading = True


def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

reader = MFRC522.MFRC522()

while continue_reading:
    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    if status == reader.MI_OK:
        print "Tag detected"

    (status, uid) = reader.MFRC522_Anticoll()

    if status == reader.MI_OK:
        print "UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])

        auth_key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        reader.MFRC522_SelectTag(uid)

        status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 8, auth_key, uid)

        if not status == reader.MI_OK:
            status = reader.MFRC522_Auth(reader.PICC_AUTHENT1B, 8, auth_key, uid)
            if not status == reader.MI_OK:
                print "Error"
                continue

        print(str(reader.MFRC522_Read(8)))
        reader.MFRC522_StopCrypto1()
