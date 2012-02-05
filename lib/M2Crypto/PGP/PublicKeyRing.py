"""M2Crypto PGP2.

Copyright (c) 1999-2003 Ng Pheng Siong. All rights reserved."""

from constants import *
from packet import *
from PublicKey import *

class PublicKeyRing:
    def __init__(self, keyring):
        import warnings
        warnings.warn('Deprecated. No maintainer for PGP. If you use this, please inform M2Crypto maintainer.', DeprecationWarning)

        self._keyring = keyring
        self._userid = {}
        self._keyid = {}
        self._spurious = []
        self._pubkey = []

    def load(self):
        curr_pub = None
        curr_index = -1

        ps = packet_stream(self._keyring)
        while 1:
            pkt = ps.read() 

            if pkt is None:
                break

            elif isinstance(pkt, public_key_packet):
                curr_index = curr_index + 1
                curr_pub = PublicKey(pkt)
                self._pubkey.append(curr_pub)
                #self._keyid[curr_pub.keyid()] = (curr_pub, curr_index)

            elif isinstance(pkt, userid_packet):
                if curr_pub is None:
                    self._spurious.append(pkt)
                else:
                    curr_pub.add_userid(pkt)
                    self._userid[pkt.userid()] = (curr_pub, curr_index)

            elif isinstance(pkt, signature_packet):
                if curr_pub is None:
                    self._spurious.append(pkt)
                else:
                    curr_pub.add_signature(pkt)

            else:
                self._spurious.append(pkt)

        ps.close()
            
    def __getitem__(self, id):
        return self._userid[id][0]

    def __setitem__(self, *args):
        raise NotImplementedError

    def __delitem__(self, id):
        pkt, idx = self._userid[id]
        del self._pubkey[idx]
        del self._userid[idx]
        pkt, idx = self._keyid[id]
        del self._keyid[idx]

    def spurious(self):
        return tuple(self._spurious)

    def save(self, keyring):
        for p in self._pubkey:
            pp = p.pack()
            keyring.write(pp)


def load_pubring(filename='pubring.pgp'):
    pkr = PublicKeyRing(open(filename, 'rb'))
    pkr.load()
    return pkr

