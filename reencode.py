from speex import *
import sys
import math

def decodeToPCM(appleSpeex, rate, quality):
        dec = Decoder()
        dec.initialize(mode=SPEEX_MODEID_WB)
        raw = dec.decode(appleSpeex)
        dec.destroy()
	return raw

