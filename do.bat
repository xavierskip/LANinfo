@ echo off
set base_dir=%~dp0  
%base_dir:~0,2%
pushd %base_dir%
echo # %time%  >> data/log/%date:~0,4%-%date:~5,2%.log
python run.py >>  data/log/%date:~0,4%-%date:~5,2%.log  
popd