Siri Server
===========

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
Note: you can also install libspeex via MacPorts, but libflac is not available in 64bit you need to supply `--disable-asm-optimizations` in configure to make it compile

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


Thanks
------
A bit thanks to [Applidium](http://applidium.com/en/news/cracking_siri/) and also [plamoni](https://github.com/plamoni/SiriProxy/) for his SiriProxy which inspired me
Thanks to everyone that contributed code or ideas

Licensing
---------
This is free software. You can reuse it under the terms of the [Creative Commons Attribution-NonCommercial-ShareAlike 3.0](http://creativecommons.org/licenses/by-nc-sa/3.0/) license. So you can do what ever you want with it. But you are not allowed to sell it.
If you like to do more than the license allows, please contact me and ask for a special commercial license.

Disclaimer
----------
Apple owns all the rights on Siri. I do not give any warranties or guaranteed support for this software. Use it as it is.
