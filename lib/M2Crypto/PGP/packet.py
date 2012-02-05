"""M2Crypto PGP2.

This module implements PGP packets per RFC1991 and various source distributions.

Each packet type is represented by a class; packet classes derive from 
the abstract 'packet' class. 

The 'message digest' packet type, mentioned but not documented in RFC1991,
is not implemented.

Copyright (c) 1999-2003 Ng Pheng Siong. All rights reserved."""

# XXX Work-in-progress.

# Be liberal in what you accept.
# Be conservative in what you send. 
# Be lazy in what you eval.

import struct, time

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from M2Crypto import EVP, RSA
from M2Crypto.util import octx_to_num

from constants import *

_OK_VERSION     = ('\002', '\003')
_OK_VALIDITY    = ('\000',)
_OK_PKC         = ('\001',)


class packet:
    def __init__(self, ctb, body=None):
        import warnings
        warnings.warn('Deprecated. No maintainer for PGP. If you use this, please inform M2Crypto maintainer.', DeprecationWarning)
        
        self.ctb = ctb
        if body is not None:
            self.body = StringIO(body)
        else:
            self.body = None

    def validate(self):
        return 1

    def pack(self):
        raise NotImplementedError, '%s.pack(): abstract method' % (self.__class__,)

    def version(self):
        if hasattr(self, '_version'):
            return ord(self._version)
        else:
            return None

    def timestamp(self):
        if hasattr(self, '_timestamp'):
            return struct.unpack('>L', self._timestamp)[0]
        else:
            return None

    def validity(self):
        if hasattr(self, '_validity'):
            return struct.unpack('>H', self._validity)[0]
        else:
            return None

    def pkc(self):
        if hasattr(self, '_pkc'):
            return self._pkc
        else:
            return None

    def _llf(self, lenf):
        if lenf < 256:  
            return (0, chr(lenf))
        elif lenf < 65536:
            return (1, struct.pack('>H', lenf))
        else: 
            assert lenf < 2L**32
            return (2, struct.pack('>L', lenf))

    def _ctb(self, llf):
        ctbv = _FACTORY[self.__class__]
        return chr((1 << 7) | (ctbv << 2) | llf)


class public_key_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if self.body is not None:
            self._version = self.body.read(1)
            self._timestamp = self.body.read(4)
            self._validity = self.body.read(2)
            self._pkc = self.body.read(1)

            self._nlen = self.body.read(2)
            nlen = (struct.unpack('>H', self._nlen)[0] + 7) / 8
            self._n = self.body.read(nlen)
            
            self._elen = self.body.read(2)
            elen = (struct.unpack('>H', self._elen)[0] + 7) / 8
            self._e = self.body.read(elen)

    def pack(self):
        if self.body is None:
            self.body = StringIO()
            self.body.write(self._version)
            self.body.write(self._timestamp)
            self.body.write(self._validity)
            self.body.write(self._pkc)
            self.body.write(self._nlen)
            self.body.write(self._n)
            self.body.write(self._elen)
            self.body.write(self._e)
        self.body = self.body.getvalue()
        llf, lenf = self._llf(len(self.body))
        ctb = self._ctb(llf)
        return '%s%s%s' % (ctb, lenf, self.body)

    def pubkey(self):
        return self._pubkey.pub()


class trust_packet(packet):
    # This implementation neither interprets nor emits trust packets.
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self.trust = self.body.read(1)


class userid_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self._userid = body

    def pack(self):
        if self.body is None:
            self.body = StringIO()
            self.body.write(chr(len(self._userid)))
            self.body.write(self._userid)
            self.body = self.body.getvalue()
        return self.ctb + self.body

    def userid(self):   
        return self._userid


class comment_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self.comment = self.body.getvalue()

    def pack(self):
        if self.body is None:
            self.body = StringIO()
            self.body.write(chr(len(self.comment)))
            self.body.write(self.comment)
            self.body = self.body.getvalue()
        return self.ctb + self.body


class signature_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self._version = self.body.read(1)
            self._len_md_stuff = self.body.read(1)
            self._classification = self.body.read(1)
            self._timestamp = self.body.read(4)
            self._keyid = self.body.read(8)
            self._pkc = self.body.read(1)
            self._md_algo = self.body.read(1)
            self._md_chksum = self.body.read(2)
            self._sig = self.body.read()

    def pack(self):
        if self.body is None:
            self.body = StringIO()
            self.body.write(self._version)
            self.body.write(self._len_md_stuff)
            self.body.write(self._classification)
            self.body.write(self._timestamp)
            self.body.write(self._keyid)
            self.body.write(self._pkc)
            self.body.write(self._md_algo)
            self.body.write(self._md_chksum)
            self.body.write(self._sig)
            self.body = self.body.getvalue()
        llf, lenf = self._llf(len(body))
        self.ctb = self.ctb | llf
        return '%s%s%s' % (self.ctb, lenf, self.body)


    def validate(self):
        if self._version not in _OK_VERSION:
            return None
        if self._len_md_stuff != '\005':
            return None


class private_key_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self._version = self.body.read(1)
            self._timestamp = self.body.read(4)
            self._validity = self.body.read(2)
            self._pkc = self.body.read(1)

            self._nlen = self.body.read(2)
            nlen = (struct.unpack('>H', self._nlen)[0] + 7) / 8
            self._n = self.body.read(nlen)
            
            self._elen = self.body.read(2)
            elen = (struct.unpack('>H', self._elen)[0] + 7) / 8
            self._e = self.body.read(elen)

            self._cipher = self.body.read(1)
            if self._cipher == '\001':
                self._iv = self.body.read(8)
            else:
                self._iv = None
    
            for param in ['d', 'p', 'q', 'u']:
                _plen = self.body.read(2)
                setattr(self, '_'+param+'len', _plen)
                plen = (struct.unpack('>H', _plen)[0] + 7) / 8
                setattr(self, '_'+param, self.body.read(plen))
    
            self._cksum = self.body.read(2)

    def is_encrypted(self):
        return ord(self._cipher)


class cke_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self._iv = self.body.read(8)
            self._cksum = self.body.read(2)
            self._ctxt = self.body.read()


class pke_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self._version = self.body.read(1)
            self._keyid = self.body.read(8)
            self._pkc = ord(self.body.read(1))
    
            deklen = (struct.unpack('>H', self.body.read(2))[0] + 7 ) / 8
            self._dek = octx_to_num(self.body.read(deklen))


class literal_packet(packet):
    def __init__(self, ctb, body=None):
        packet.__init__(self, ctb, body)
        if body is not None:
            self.fmode = self.body.read(1)
            fnlen = self.body.read(1)
            self.fname = self.body.read(fnlen)
            self.ftime = self.body.read(4)
            #self.data = self.body.read()


class compressed_packet(packet):
    def __init__(self, ctb, stream):
        packet.__init__(self, ctb, '')
        if body is not None:
            self.algo = stream.read(1)
            # This reads the entire stream into memory.
            self.data = stream.read()

    def validate(self):
        return (self.algo == '\001')

    def uncompress(self):
        import zlib
        decomp = zlib.decompressobj(-13)    # RFC 2440, pg 61.
        # This doubles the memory usage.
        stream = StringIO(decomp.decompress(self.data))
        return stream


_FACTORY = { 
    1 : pke_packet,
    2 : signature_packet,
    #3 : message_digest_packet,     # XXX not implemented
    5 : private_key_packet,
    6 : public_key_packet,
    #8 : compressed_packet,         # special case
    9 : cke_packet,
    11 : literal_packet,
    12 : trust_packet,
    13 : userid_packet,
    14 : comment_packet,
    pke_packet : 1,
    signature_packet : 2,
    #3 : message_digest_packet,     
    private_key_packet : 5,
    public_key_packet : 6,
    #8 : compressed_packet,
    cke_packet : 9,
    literal_packet : 11,
    trust_packet : 12,
    userid_packet : 13,
    comment_packet : 14
}


class packet_stream:
    def __init__(self, input):
        self.stream = input
        self.under_current = None
        self._count = 0

    def close(self):
        self.stream.close()
        if self.under_current is not None:
            self.under_current.close()

    def read(self, keep_trying=0):
        while 1:
            ctb0 = self.stream.read(1)
            if not ctb0:
                return None
            ctb = ord(ctb0)
            if is_ctb(ctb):
                break
            elif keep_trying:
                continue
            else:
                raise XXXError
        ctbt = (ctb & 0x3c) >> 2

        if ctbt == CTB_COMPRESSED_DATA:
            self.under_current = self.stream
            cp = compressed_packet(ctb0, self.stream)
            self.stream = cp.uncompress()
            return self.read()

        # Decode the length of following data. See RFC for details.
        llf = ctb & 3
        if llf == 0:
            lenf = ord(self.stream.read(1))
        elif llf == 1:
            lenf = struct.unpack('>H', self.stream.read(2))[0]
        elif llf == 2:
            lenf = struct.unpack('>L', self.stream.read(4))[0]
        else: # llf == 3
            raise XXXError, 'impossible case'

        body = self.stream.read(lenf)
        if not body or (len(body) != lenf):
            raise XXXError, 'corrupted packet'

        self._count = self.stream.tell()
        try: 
            return _FACTORY[ctbt](ctb0, body) 
        except KeyError:
            return packet(ctb0, body)

    def count(self):
        return self._count

def is_ctb(ctb):
    return ctb & 0xc0

def make_ctb(value, llf):
    return chr((1 << 7) | (value << 2) | llf)
