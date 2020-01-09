#!/bin/bash


`readelf -s $1 | gawk 'BEGIN {FS=" ";ORS="\n"}''{if ($4 == "FUNC" && $5 == "GLOBAL" && 0 == match($8, /^_/)) print ($8)}' > ./functions && \
/opt/toolchain/iProcLDK_3.4.6/usr/bin/arm-linux-objdump -d ./ISS.exe | gawk 'BEGIN {FS=" ";ORS="\n"}''{if (match($5, /^[<a-zA-Z]+[a-zA-Z_]*>/)) print ($5)}' | gawk 'BEGIN {FS="[<>]"; ORS="\n"}''{if (0 == match($2, /^_/)) print ($2)}' > ./used`
while IFS= read -r line
do
    grep $line ./used
    if [ $? -eq 1 ]
    then
        echo $line >> ./unused
    fi
done < ./functions
