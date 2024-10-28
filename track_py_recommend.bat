@echo off
setlocal enabledelayedexpansion

REM 设定文件路径
set "file_list=PyRecommend.txt"

REM 检查文件是否存在
if not exist "!file_list!" (
    echo 文件 "!file_list!" 未找到.
    exit /b 1
)

REM 逐行读取文件并执行 git lfs track
for /f "delims=" %%i in (!file_list!) do (
    git lfs track "%%i"
)

REM add files
for /f "delims=" %%f in (!file_list!) do (
    git add "%%f"
)

REM 更新 .gitattributes 文件
git add .gitattributes
echo .gitattributes has been updated.
