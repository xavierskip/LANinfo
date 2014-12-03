@ echo off
set base_dir=%~dp0  
%base_dir:~0,2%
pushd %base_dir%
cp data/network.db data/network.db.backup
popd