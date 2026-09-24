@echo off
chcp 65001 >nul 2>&1
REM 第1讲 你好世界 - build.bat (用法: build.bat [build])
echo [编译中] 使用 GCC 编译 hello.c ...
gcc -Wall -o hello.exe hello.c

if %ERRORLEVEL% EQU 0 (
    echo [编译成功] 生成 hello.exe
    if /i "%1"=="build" goto end
    echo.
    echo [运行程序]
    hello.exe
) else (
    echo [编译失败] 请检查代码
    exit /b 1
)

:end
echo.
if not "%1"=="build" pause
