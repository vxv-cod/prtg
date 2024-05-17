
CALL venv\Scripts\activate.bat
wt --title redis-server %cd%\Redis-x64-5.0.14.1\redis-server.exe; ^
sp -V -s 0.3 --title redis-cli %cd%\Redis-x64-5.0.14.1\redis-cli.exe