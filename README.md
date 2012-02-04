Siri Server
===========

IMPORTANT
---------
There are currently only 3 plugins here, you can chat a little bit with siri.
You can ask it for the current time and the current time at a certain point in the world.
And you can ask it for the meaning of life.

You can contribute by making more plugins!

What is this?
-------------
This is a very early version of a Siri Server (not a proxy).

Apple's Siri is an voice controlled assistant on iPhone 4S.

With jailbreaking you can install it on other iDevices.
However, Siri needs a server to communicate to do the speech processing.
Apple only allows 4S devices on their servers.

This project tries to recreate the Apple Siri Server to use it with other iDevices.

You don't need any 4S keys to make it work, as it is independent from Apple.

It uses Google Speech-To-Text API. And therefore we are currently limited to 
commands that are shorter than 10 seconds (maybe we can overcome this).

What's new?
-----------
We have a new plugin system:
Check out the plugins folder and the [example plugin](https://github.com/Eichhoernchen/SiriServer/blob/master/plugins/examplePlugin.py) for more infos.
It supports multi-language inputs.

You should also checkout the [plugin.py](https://github.com/Eichhoernchen/SiriServer/blob/master/plugin.py) to see a plugin's predefined methods.
You can also look at the [time](https://github.com/Eichhoernchen/SiriServer/blob/master/plugins/time.py) plugin, it sends more complexe objects and does meaningful localized output. And does more complex processing of different inputs

What else is here?
------------------
The file SiriProtocol documents everything I (and others) found out about the protocol by now


Setup, Notes and Instructions
-----------------------------

**Install audio libraries**

For the audio handling you need [libspeex](http://www.speex.org/) and [libflac](http://flac.sourceforge.net/)

On Linux simply install it via you packet manager e.g. (or see instructions and note for OS X):

	sudo apt-get install libspeex1 libflac8

On OS X download libspeex and libflac from the websites above (the sources, not the binaries)
and compile and install them, or simply follow the following steps:

	wget http://downloads.xiph.org/releases/speex/speex-1.2rc1.tar.gz
	tar -xf speex-1.2rc1.tar.gz
	cd speex-1.2rc1
	./configure
	make
	sudo make install
	cd ..
	
	wget http://sourceforge.net/projects/flac/files/flac-src/flac-1.2.1-src/flac-1.2.1.tar.gz/download -O flac-1.2.1.tar.gz
	tar -xf flac-1.2.1.tar.gz
	./configure --disable-asm-optimizations
	make
	sudo make install
Note: you can also install libspeex via MacPorts, but libflac is not available in 64bit through MacPorts, to make it build with 64bit support you need to supply `--disable-asm-optimizations` in configure of libflac to make it compile

**Python requirements**

As this project is coded with python you need a python interpreter (this is usually already installed).
I work with python 2.6.6 and 2.7.2 and both work.

You also need some python packages to make it work:

	biplist
	M2Crypto

You can install both via `easy_install`,
easy_install is available at [http://pypi.python.org/pypi/setuptools](http://pypi.python.org/pypi/setuptools),
on Linux you can also get it via your packet manager:

	sudo apt-get install python-setuptools

After you installed it, run:

	easy_install biplist
	easy_install M2Crypto

**Certificate Generation**

We also need to generate certificates for`guzzoni.apple.com` or any other domain

	cd gen_certs
then

	./gen_certs.sh
or

	./gen_certs.sh 192.168.1.1
or

	./gen_certs.sh domain.com
this will generate a certifcaite for `guzzoni.apple.com`, `192.168.1.1` or `domain.com`

When you use Spire, just enter as address what ever parameter you supplied to `gen_certs.sh` e.g.:

	https://guzzoni.apple.com
or

	https://domain.com
or

	https://192.168.1.1

In case you don't have Spire or want to use `guzzoni.apple.com`
you need to setup a DNS spoofing or manipulate you hosts file

Please make sure to install the CA certificate on your iDevice (you can simply mail it to yourself).
It is the CA.pem file that was copied by gen_certs.sh to the servers root. 
In your mail, just click on the certificate and install it.

**Running the server**

Now you are ready to go, start the server with:

	sudo python siriServer.py
Note: You need to run it as root, as we use https port 443
(non root can only use ports > 1024) for incomming connections.


Common Errors
-------------
If we had the mid 90s this section would glow and sparkle to get your attention.
There are some errors that might occur even though you did everything that was written above...

**The server just crashes after a SpeechPacket**

You are running Linux right? Probably debian?
There is probably already a libspeex on your machine which is optimized for SSE2 which does not work with python (reason???)
Check if there is a `/usr/lib/sse2/libspeex.so.1`.

Option A: delete it (there should also be a version in /usr/lib if you installed via apt, or in /usr/local/lib if you compiled by hand)

Option B: ToDo

**This M2Crypto thing is not working**

Did you install all [dependencies](http://chandlerproject.org/Projects/MeTooCrypto#Requirements) of M2Crypto?

**I cannot get a connection from device to server**

Do you access your server over the internet? You need to setup your firewall and NAT to allow traffic for tcp port 443 directed to your server
Do you have a local firewall on the machine running the server? Also check if tcp port 443 is allowed for incomming connections


**There is an exception with something around a database lock**

	error: uncaptured python exception, closing channel <main.HandleConnection connected xxx.xxx.xxx.xxx:XXXX at 0xa65c368> (:database is locked
Solution: delete the .sqlite3 file and restart server

**There is something with SSL in the error**

Have you installed the ca.pem file on your phone? Do you have more than one CA certificate installed for the same domain?

=> Try deleting all certificates on the device and install the one created by gen_certs

Can I somehow verify the correct certificate? YES!

start siriServer.py, then take your ca.pem you think belongs to your servers certificate and run:

	 echo | openssl s_client -connect [DOMAIN]:443 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl verify -CAfile ca.pem 
Make sure to replace [DOMAIN] with the actual domain of the machine running siriServer.py (e.g. an IP address)
If your ca.pem matches your server certificate you should see `stdin: OK` as output!

OK, what else?
We can also setup a small test server using openssl to check if SSL is working (and to check if the iPhone correctly validates the server certificate):

	sudo openssl s_server -cert server.passless.crt -key server.passless.key -accept 443 -state
When you run this (siriServer should NOT run) it opens a basis server on port 443 using your servers certificate.

Now you can connect with your iPhone as if you would use Siri (of course Siri won't work, we are just testing the SSL layer)
It should output something like this, note the Ace http request near the end:

	 Using default temp DH parameters
	 Using default temp ECDH parameters  
	 ACCEPT
	 SSL_accept:before/accept initialization
	 SSL_accept:SSLv3 read client hello A
	 SSL_accept:SSLv3 write server hello A
	 SSL_accept:SSLv3 write certificate A
	 SSL_accept:SSLv3 write server done A
	 SSL_accept:SSLv3 flush data
	 SSL_accept:SSLv3 read client key exchange A
	 SSL_accept:SSLv3 read finished A
	 SSL_accept:SSLv3 write change cipher spec A
	 SSL_accept:SSLv3 write finished A
	 SSL_accept:SSLv3 flush data
	 -----BEGIN SSL SESSION PARAMETERS-----
	 MIGKAgEBAgIDAQQCAC8EIJ3DOw2nTgOAjdCNMqiFi+OmYU1fszwfH3jDk4q1P/mq
	 BDB7vM4nKFiGjLHpExNf4F1HZQ7ekRPaG/2X9EI/mqtpeWPp8vU1a/Em5JWomauK
	 jDShBgIETyr5oaIEAgIBLKQGBAQBAAAAphMEEWVob2VybmNoZW4uYXRoLmN4
	 -----END SSL SESSION PARAMETERS-----
 	 Shared ciphers:ECDHE-ECDSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-      ECDSA-DES-CBC3-SHA:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:ECDH-ECDSA-AES256-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-   SHA:AES128-SHA:RC4-SHA:RC4-MD5:AES256-SHA:DES-CBC3-SHA:DHE-RSA-AES128-SHA:DHE-RSA-AES256-  SHA:EDH-RSA-DES-CBC3-SHA
	 CIPHER is AES128-SHA
	 Secure Renegotiation IS supported
	 ACE /ace HTTP/1.0
	 Host: DOMAIN REMOVED
	 User-Agent: Assistant(iPhone/iPhone3,1; iPhone OS/5.0.1/9A405) Ace/1.0
	 Content-Length: 2000000000



Thanks
------
A big thanks to [Applidium](http://applidium.com/en/news/cracking_siri/) and also [plamoni](https://github.com/plamoni/SiriProxy/) for his SiriProxy which inspired me
Thanks to everyone that contributed code or ideas.

Licensing
---------
This is free software. You can reuse it under the terms of the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/) license. So you can do what ever you want with it. But you are not allowed to sell it.
If you like to do more than the license allows, please contact me and ask for a special commercial license.

Disclaimer
----------
Apple owns all the rights on Siri. I do not give any warranties or guaranteed support for this software. Use it as it is.
