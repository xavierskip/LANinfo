@ echo off
set base_dir=%~dp0  
%base_dir:~0,2%
pushd %base_dir%
cd data
copy /y network.db network.db.backup
popd