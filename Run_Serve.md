
## Конфигарация ***web.config*** через ***httpPlatformHandler***
Скачать и установить *httpPlatformHandler_amd64.msi*
Сервер IIS будет отслеживать свой порт, в данном случае http://127.0.0.1:8888/ и перезагружать uvicorn по порту http://127.0.0.1:7777/ при этом будут писаться логи uvicorn.
Не обращать внимания на ошибку по адресу http://127.0.0.1:8888/: Ошибка HTTP 502.3 — Bad Gateway

```xml
<configuration>
    <system.webServer>
        <handlers>
            <add name="httpPlatformHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified" requireAccess="Script" />
        </handlers>
        <httpPlatform
            `... Варианты подключения`
            processPath="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\python.exe" 
            arguments="-m flask run --port 7777 --debug=True"
            
            processPath="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\python.exe" 
            arguments="-m uvicorn src.main:app --port 7777"
            
            processPath="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\uvicorn.exe" 
            arguments="src.main:app --port 7777"
            
            processPath="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\python.exe" 
            arguments="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\uvicorn.exe src.main:app --port 7777"
            
            processPath="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\waitress-serve.exe" 
            arguments="--listen=127.0.0.1:7777 src.main:wsgi_app"
            
            processPath="C:\vxvproj\Sapsan_manager\Backend\venv\Scripts\python.exe" 
            arguments="-m hypercorn src.main:app -b 127.0.0.1:7777 --keep-alive 5 --worker-class asyncio --workers 4"
            
            `... Дополнительные параметы:`
            stdoutLogEnabled="true" 
            stdoutLogFile=".\LogFiles\stdout" 
            startupTimeLimit="60"
            requestTimeout="00:05:00" 
            startupRetryCount="1"
            processesPerApplication="16"            
        ></httpPlatform>
    </system.webServer>
</configuration>
```

`Консольные команды`
```bash
uvicorn src.main:app --host 127.0.0.1 --port 7777
hypercorn src.main:app --bind 127.0.0.1:7777
waitress-serve --listen=127.0.0.1:7777 src.main:wsgi_app
gunicorn src.main:wsgi_app --bind=127.0.0.1:7777 --worker-class uvicorn.workers.UvicornWorker
gunicorn -k uvicorn.workers.UvicornWorker
```

<!-- <?xml version="1.0" encoding="utf-8"?> -->
<configuration>
    <system.webServer>
        <handlers>
            <add name="httpPlatformHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified" />
        </handlers>
        <httpPlatform 
                    processPath="C:\nmol\hpt-api\venv\Scripts\python.exe"
                    arguments="-m hypercorn app.main:app -b 127.0.0.1:%HTTP_PLATFORM_PORT% --keep-alive 5 --worker-class asyncio --workers 4"
                    stdoutLogEnabled="true" 
                    stdoutLogFile="C:\nmol\hpt-api\logs\python-stdout.log" 
                    startupTimeLimit="120" 
                    requestTimeout="00:05:00" 
                    startupRetryCount="3"
					processesPerApplication="5">
            <environmentVariables>
                <environmentVariable name="PORT" value="%HTTP_PLATFORM_PORT%" />
            </environmentVariables>
        </httpPlatform>
    </system.webServer>
</configuration>

