    
@echo off

SET "wu_protos_path=.\src\"**

SET "wu_protos_target=WUProtos.Data.GameDataWrapper"**
SET "wu_protos_template=.\src\WUProtos\Data\GameDataWrapper.proto"**

protoc --proto_path=%wu_protos_path% --decode %wu_protos_target%  %wu_protos_template%  < %1 > %1_decoded.txt
