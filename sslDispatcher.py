#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import ssl
    import asyncore
except ImportError:
    pass
else:
    class ssl_dispatcher(asyncore.dispatcher_with_send):
        """A dispatcher subclass supporting SSL."""

        _ssl_accepting = False
        _ssl_established = False
        _ssl_closing = False

        # --- public API

        def secure_connection(self, certfile, keyfile, version=ssl.PROTOCOL_TLSv1, verify=ssl.CERT_NONE, server_side=False):
            """Setup encrypted connection."""
            self.socket = ssl.wrap_socket(self.socket, do_handshake_on_connect=False, certfile=certfile, keyfile=keyfile, suppress_ragged_eofs=True, server_side=server_side)
            self._ssl_accepting = True

        def ssl_shutdown(self):
            """Tear down SSL layer switching back to a clear text connection."""
            if not self._ssl_established:
                raise ValueError("not using SSL")
            self._ssl_closing = True
            try:
                self.socket = self.socket.unwrap()
            except ssl.SSLError as err:
                if err.args[0] in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE):
                    return
                elif err.args[0] == ssl.SSL_ERROR_SSL:
                    pass
                else:
                    raise
            except socket.error as err:
                # Any "socket error" corresponds to a SSL_ERROR_SYSCALL
                # return from OpenSSL's SSL_shutdown(), corresponding to
                # a closed socket condition. See also:
                # http://www.mail-archive.com/openssl-users@openssl.org/msg60710.html
                pass
            self._ssl_closing = False
            self.handle_ssl_shutdown()

        def handle_ssl_established(self):
            """Called when the SSL handshake has completed."""
            self.log_info('unhandled handle_ssl_established event', 'warning')

        def handle_ssl_shutdown(self):
            """Called when SSL shutdown() has completed"""
            self.log_info('unhandled handle_ssl_shutdown event', 'warning')

        # --- internals

        def _do_ssl_handshake(self):
            try:
                self.socket.do_handshake()
            except ssl.SSLError as err:
                if err.args[0] in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE):
                    return
                elif err.args[0] == ssl.SSL_ERROR_EOF:
                    return self.handle_close()
                raise
            else:
                self._ssl_accepting = False
                self._ssl_established = True
                self.handle_ssl_established()

        def handle_read_event(self):
            if self._ssl_accepting:
                self._do_ssl_handshake()
            elif self._ssl_closing:
                self.ssl_shutdown()
            else:
                asyncore.dispatcher_with_send.handle_read_event(self)

        def handle_write_event(self):
            if self._ssl_accepting:
                self._do_ssl_handshake()
            elif self._ssl_closing:
                self.ssl_shutdown()
            else:
                asyncore.dispatcher_with_send.handle_write_event(self)

        def send(self, data):
            try:
                asyncore.dispatcher_with_send.send(self, data)
            except ssl.SSLError as err:
                if err.args[0] in (ssl.SSL_ERROR_EOF, ssl.SSL_ERROR_ZERO_RETURN):
                    return 0
                raise

        def recv(self, buffer_size):
            try:
                return asyncore.dispatcher_with_send.recv(self, buffer_size)
            except ssl.SSLError as err:
                if err.args[0] in (ssl.SSL_ERROR_EOF, ssl.SSL_ERROR_ZERO_RETURN):
                    self.handle_close()
                    return ''
                if err.args[0] in (ssl.SSL_ERROR_WANT_READ, ssl.SSL_ERROR_WANT_WRITE):
                    return ''
                raise


