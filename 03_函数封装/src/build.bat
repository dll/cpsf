@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  第3讲：函数封装 —— 给代码找个家
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  对比第2讲：main 里的长代码被拆成了一个个函数
REM  每个函数一个职责：查询 / 存款 / 取款 / 转账
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set TARGET=atm_func.exe

echo ============================================================
echo   第3讲 函数封装 - 构建
echo ============================================================
echo.

echo [1/2] 正在编译 %TARGET% ...
gcc %CFLAGS% -o %TARGET% atm_func.c
if errorlevel 1 goto fail
echo       OK -^> %TARGET%
echo.

if /i "%1"=="build" goto ok

echo [2/2] 自动演示：查询 -^> 存款500 -^> 取款200 -^> 转账100 -^> 退出
echo ------------------------------------------------------------
(echo 1& echo 2& echo 500& echo 3& echo 200& echo 4& echo 100& echo 2002& echo 0) | %TARGET%
echo ------------------------------------------------------------
goto ok

:fail
echo.
echo [构建失败] 请检查上面的错误信息。
exit /b 1

:ok
echo.
echo 手动运行：%TARGET%
echo 清理产物：del %TARGET%
endlocal
