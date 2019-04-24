    
@echo off

SET "pogo_protos_path=.\src\"**

SET "pogo_protos_target=WUProtos.Data.GameDataWrapper"**
SET "pogo_protos_template=.\src\WUProtos\Data\GameDataWrapper.proto"**

protoc --proto_path=%pogo_protos_path% --decode %pogo_protos_target%  %pogo_protos_template%  < %1 > %1_decoded.txt