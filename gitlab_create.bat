:: Глобальные настройки
@REM git config --global user.name "Хомутский Владимир Валерьевич"
@REM git config --global user.email "vvkhomutskiy@tnnc.rosneft.ru"
@REM git config --system http.sslCAInfo false
@REM git config --global http.sslVerify false

:: Инициализируем GIT и отправляем в GitLab по урлу
git init
git remote add origin https://svp-tnnc/VVKhomutskiy/PRTG.git
git add .
git commit -m "Initial commit"
git push -u origin master

:: Отправляем на GitLab существующий репозиторий с git (push со всеми коммитами)
:: - не рекомендуется все коммиты весят много
@REM git remote rm origin
@REM git remote add origin https://svp-tnnc/VVKhomutskiy/PRTG.git
@REM git push -u origin master