@ echo off
set base_dir=%~dp0  
%base_dir:~0,2%
pushd %base_dir%
python run.py >>  data/log/%date:~0,4%-%date:~5,2%.log 2>&1
echo #%date:~5,2%-%time%  >> data/log/%date:~0,4%-%date:~5,2%.log
popd