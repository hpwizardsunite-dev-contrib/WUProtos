@echo off

SET "pogo_protos_path=.\src\"**

SET "pogo_protos_target=WUProtos.Networking.Responses.DownloadGmTemplatesResponse"**
SET "pogo_protos_template=.\src\WUProtos\Networking\Responses\DownloadGmTemplatesResponse.proto"**

protoc --proto_path=%pogo_protos_path% --decode %pogo_protos_target%  %pogo_protos_template%  < %1 > %1_decoded.txt

