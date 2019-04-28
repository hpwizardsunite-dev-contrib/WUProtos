#!/bin/sh

args=("$@")

function goto
{
label=$1
cmd=$(sed -n "/$label:/{:a;n;p;ba};" $0 | grep -v ':$')
eval "$cmd"
exit
}

echo WUProtos decode tool.
echo

if  [ "${args[0]}" = "" ]; then
	echo Usage ${args[0]} [file_to_decode.ext].
	exit
fi


echo Decoding ${args[0]}. Wait...
export  wu_protos_path=./src/*
export  wu_protos_target=WUProtos.Data.GameDataWrapper
export  wu_protos_template=./src/WUProtos/Data/GameDataWrapper.proto
protoc --proto_path=$wu_protos_path --decode $wu_protos_target  $wu_protos_template  < ${args[0]} > ${args[0]}_decoded.txt
echo Decoded file ${args[0]}_decoded.txt
