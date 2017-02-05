from pirc522 import RFID
import time

rdr = RFID()
util = rdr.util()
oldId = None


def read_sector(block_address):
    try:
        util.do_auth(block_address)
        res = rdr.read(block_address)
        return res
    except Exception:
        return True, None

print("Running")
try:
    while True:
        (error, tagType) = rdr.request()
        if not error:
            (error, uid) = rdr.anticoll()
            if not error:
                util.set_tag(uid)
                if oldId == uid:
                    should_continue = input("Same tag detected. Should I continue? (y/n)")
                    if should_continue == "n":
                        continue
                    elif should_continue == "y":
                        oldId = None
                        continue
                    else:
                        print("Unknown option. Assuming that's a 'no'")
                        continue

                oldId = uid
                print("Tag prepared")

                # Set the correct auth mode
                util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                (error, data) = read_sector(0)

                if error:
                    util.deauth()
                    (error, tagType) = rdr.request()
                    if error:
                        oldId = None
                        util.deauth()
                        print("Please don't remove the tag!")
                        continue
                    (error, uid) = rdr.anticoll()
                    if error:
                        oldId = None
                        util.deauth()
                        print("Please don't remove the tag!")
                        continue

                    util.set_tag(uid)
                    util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
                    (error, data) = read_sector(0)
                    if error:
                        oldId = None
                        util.deauth()
                        print("Auth key error!")
                        continue
                tagRemoved = False
                for i in range(0, 64):
                    (error, data) = read_sector(i)
                    if error:
                        break
                    print("Block " + str(i) + ": " + str(data))
                if tagRemoved:
                    oldId = None
                    print("Please don't remove the tag!")
                    time.sleep(1)

                util.deauth()
except KeyboardInterrupt:
    print("Exiting")
finally:
    rdr.cleanup()
