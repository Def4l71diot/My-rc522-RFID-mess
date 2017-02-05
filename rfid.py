from pirc522 import RFID
import re
import time

rdr = RFID()
util = rdr.util()
oldId = None
util.debug = True
authModeA = True

errorR = re.compile("error", re.IGNORECASE)

print("Running")
try:
    while True:
        (error, tagType) = rdr.request()
        if not error:
            print("Tag detected")
            (error, uid) = rdr.anticoll()
            if not error:
                util.set_tag(uid)

                if authModeA:
                    print(str(util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])))
                else:
                    print(str(util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])))

                util.do_auth(9)
                (error, data) = rdr.read(9)

                if error:
                    authModeA = not authModeA
                    print("Mode A: " + str(authModeA))
                    util.deauth()
                    print("Please scan again!")
                    time.sleep(1)
                    continue

                print(str(error))
                print(str(data))

                util.deauth()
except KeyboardInterrupt:
    print("Exiting")
finally:
    rdr.cleanup()
