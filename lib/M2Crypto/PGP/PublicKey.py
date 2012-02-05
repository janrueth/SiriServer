"""M2Crypto PGP2.

Copyright (c) 1999-2003 Ng Pheng Siong. All rights reserved."""

from constants import *
from packet import *
import RSA

class PublicKey:
    def __init__(self, pubkey_pkt):
        import warnings
        warnings.warn('Deprecated. No maintainer for PGP. If you use this, please inform M2Crypto maintainer.', DeprecationWarning)

        self._pubkey_pkt = pubkey_pkt
        self._pubkey = RSA.new_pub_key((pubkey_pkt._e, pubkey_pkt._n))
        self._userid = {}
        self._signature = {}

    def keyid(self):
        return self._pubkey.n[-8:]

    def add_userid(self, u_pkt):
        assert isinstance(u_pkt, userid_packet)
        self._userid[u_pkt.userid()] = u_pkt

    def remove_userid(self, userid):
        del self._userid[userid]

    def add_signature(self, userid, s_pkt):
        assert isinstance(s_pkt, signature_packet)
        assert self._userid.has_key(userid)
        if self._signature.has_key(userid):
            self._signature.append(s_pkt)
        else:
            self._signature = [s_pkt]
        
    def __getitem__(self, id):
        return self._userid[id]
    
    def __setitem__(self, *args):
        raise NotImplementedError

    def __delitem__(self, id):
        del self._userid[id]
        if self._signature[id]:
            del self._signature[id]

    def write(self, stream):
        pass

    def encrypt(self, ptxt):
        # XXX Munge ptxt into pgp format.
        return self._pubkey.public_encrypt(ptxt, RSA.pkcs1_padding)

    def decrypt(self, ctxt):
        # XXX Munge ctxt into pgp format.
        return self._pubkey.public_encrypt(ctxt, RSA.pkcs1_padding)

