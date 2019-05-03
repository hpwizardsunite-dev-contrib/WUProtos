#!/bin/sh

protoc --proto_path=src --decode WUProtos.Data.GameDataWrapper src/WUProtos/Data/GameDataWrapper.proto < GameDataWrapper.bytes > GameDataWrapper.bytes_decoded.txt
