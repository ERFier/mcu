#!/usr/bin/env python

# The Digital Bitbox must be in bootloader mode to use this script:
#   1- Unlock the bootloader using send_command.py to send '{"bootloader":"unlock"}' 
#   2- Hold the touch button 3 seconds to permit unlocking.
#   3- Replug the device, and briefly touch the touch button within 3 seconds. 
#      The LED will flash a few times quickly when entering bootloader mode.
# 
# Firmware signatures are valid for deterministically built firware releases (refer to the github readme for building).
# Invalid firmware cannot be run.
#
# After loading new firmware, re-lock the bootloader using send_command.py to send '{"bootloader":"lock"}' 


import sys
import binascii
import ecdsa
from ecdsa.curves import SECP256k1
from dbb_utils import *


if len(sys.argv) is not 3:
    print '\n\nUsage:\n\tpython load_firmware.py firmware_name firmware_version\n\n'
    sys.exit()
else:
    fn = sys.argv[1]
    version = sys.argv[2]


# Private key signatures (order is important)
if version == 'v1.3.0' or version == '1.3.0':
    ### firmware v1.3.0
    sig0 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig1 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig2 = '92698f29dd642efdd20f73df889eab009f8ae83b293511f9e14de566d69c34b6c119522c7aeba584098d6721be5c00e3a4f81f6d4d2b4f6c666b1caf1ac51e5e'
    sig3 = '843aed7ac36b332bcf422bbc4ecaf5464b57c2cd470dc87f04a840942409a7aff51b305e84dd0c8f9aa95adcb4239ae5935fe67738720a27a72e1dd4eab4862b'
    sig4 = '96463dc7e6e161d693e044e47be2a5d360253245087562c6d5160372d9b84cffbee379c4fca8695b563508d32b6b5eadddde19c411cf9438c253674dad59fb96'
    sig5 = 'e46ad7a1a56eacb2dbcf683b517d18ecd69c1029b5d8b9c5db88a81cc5b0652ed70211ffea7135571b0b59ec565da02fb264bda84a49bbf293400acd3a8e2847'
elif version == 'v1.3.1' or version == '1.3.1':
    ### firmware v1.3.1
    sig0 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig1 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig2 = 'eb1e8f653addd1e72c2cf8c6466bd15b1e07bfa22c17485b86ce82b7bcfb1171970768aaf63adc174c39a3c6969688ba831932b196195668b00cec0fd9ae3e56'
    sig3 = '68d80baa2d60782b3309ddd749a01dbcb53a124e4206a68ab7ee605435e5f4f566c7a4db5ddfa6f2c6def76d86f3e8e82f4391718fbc463acd7e106e180b8bbf'
    sig4 = 'fc1ac3a7732e43b8b41730359a3cf878305212dc5c9c617a1c118ffcff3d08b4c7bdede9c77fbe57a9562a6abd3c3604535a4f301ed224fa07275dffcc52c6cb'
    sig5 = '586eef9e69ac6e1bec5b40d99b595818b2a55cd344f335fa87594cea9135a88806947d87058447234b2a9025a287fe10ae6cbc0e49a1c0d1b1ef5a32a93f535d'
elif version == 'v1.3.2' or version == '1.3.2':
    ### firmware v1.3.2
    sig0 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig1 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig2 = '4356bff6caf8e72885b5b280e413b4d63ef301197c818a10fda1ce63ee2360890cc097469c791043c503b655ce8be682bd114362bc23a636ba812cd949401c2b'
    sig3 = 'e25bc6f477adda36634f87133262c7700e78ac55c738ac238ce3225b6b38603b921a3b5ebeee3b086f507f354752138eb9522b7f9fe091f9b8672d1e77972cdc'
    sig4 = 'ab40c629dc4d535aaf09fa79115849629f1fdca5b71995ffcdfadd005e8c0486a610069e39d87837584d60a28a119eb4e3b2905a0dfbfb3cca5768bc4cef9607'
    sig5 = '2de5977ef06db2b59fc8f144d2273cca85b4e60fbb32936d02f8f905ad86b4c787c80b8c5519da58a2b87602caf09a80123cbf28af9e173dacf0b86ae5792723'
elif version == 'v2.0.0' or version == '2.0.0':
    ### v2.0.0
    sig0 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig1 = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    sig2 = '302731115cafd4eb0d25747e604fe2a45f541c5e238dd5e946a34d608be104575b781b06f6b629e9debdfa1fe9cd27615fb0613bd90ccc527f5c9b838459c36e'
    sig3 = '20b6aa64e7f1dfce652cf69966abdda71a76560011159620d6704036ee96705e019e5bc8de2ddfa1656879744611b6909568f07deec7cfc6b6a967431b9ce81a'
    sig4 = 'f82b0f23ebf8cfec971150580343327801a6a4f4a30473929ff681e9791f79bb5d645157378acdeaa1fdce6f3fea418829a04a2c6c5a4c27b3707b77a134f5d2'
    sig5 = '4c9b22dbc81d5765b6d9bc008777dae96df90162b54b7802699f4d197d8eb28c27323bcf218b0f2437f9fdd1e1f06ccfabca6a26605115c131fb5bbd9195a11e'
else:
    print '\n\nError: invalid firmware version ({}). Use the form \'vX.X.X\'\n\n'.format(version)
    sys.exit()

test_key = 'e0178ae94827844042d91584911a6856799a52d89e9d467b83f1cf76a0482a11'

def sign(privkey, message):
    private_key = ecdsa.SigningKey.from_secret_exponent( privkey, curve = SECP256k1 )
    public_key = private_key.get_verifying_key()
    signature = private_key.sign_digest_deterministic( (message), hashfunc=hashlib.sha256, sigencode = ecdsa.util.sigencode_string )
    return binascii.hexlify(signature)


def verifyBin(filename):    
    with open(filename, "rb") as f:
        data = ""
        while True:     
            d = f.read(chunksize)
            if d == "":
                break
            data = data + d
    data = data + '\xFF' * (applen - len(data)) 
    print 'hashed firmware', binascii.hexlify(Hash(data))
    sigs = sign(int(test_key, 16), Hash(data))
    sigs += sig0 + sig1 + sig2 + sig3 + sig4 + sig5
    return sigs


# ----------------------------------------------------------------------------------
try:

    openHid()

    sig = verifyBin(fn)
    
    sendPlainBoot("b") # blink led
    sendPlainBoot("v") # bootloader version
    sendPlainBoot("e") # erase existing firmware (required)
    sendBin(fn)        # send new firmware
    
    if sendPlainBoot("s" + "0" + sig) != '0': # verify new firmware
        print 'ERROR: invalid firmware signature\n\n'
    else:
        print 'SUCCESS: valid firmware signature\n\n'


except IOError, ex:
    print ex
except (KeyboardInterrupt, SystemExit):
    print "Exiting code"


dbb.close()









