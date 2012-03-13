#!/bin/sh

# DO NOT USE THIS FILE IF YOU USE GIT

# here you can name files you wan't to exclude from an update
noUpdate=`echo "plugins.conf apiKeys.conf"`

[ -e newVersion.zip ] && rm newVersion.zip

curl -L https://github.com/jimmykane/SiriServer/zipball/master > newVersion.zip

newVersionFolder=`unzip -l newVersion.zip | sed -e 's_.*\(jimmykane-SiriServer-[a-z0-9]+\/\).*_\1_p' | awk '{i=i+1; if (i == 5) print $4}'`

[ -d $newVersionFolder ] && rm -rf $newVersionFolder

unzip -qq newVersion.zip
rm newVersion.zip

for toDelete in $noUpdate
do
   rm $newVersionFolder$toDelete
done

cp -Rf $newVersionFolder* .
rm -Rf $newVersionFolder
