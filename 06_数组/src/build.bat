@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  第6讲：数组 —— 从「一个账户」到「一批账户」
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  对比第5讲：单个 balance 换成 accounts[5] 数组 + 交易流水数组
REM  数组让「批量数据」成为可能，但大小写死 —— 这是第8讲链表的伏笔
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set TARGET=array_atm.exe

echo ============================================================
echo   第6讲 数组 - 构建
echo ============================================================
echo.

echo [1/2] 正在编译 %TARGET% ...
gcc %CFLAGS% -o %TARGET% array_atm.c
if errorlevel 1 goto fail
echo       OK -^> %TARGET%
echo.

if /i "%1"=="build" goto ok

echo [2/2] 自动演示：选账户1001 -^> 查询 -^> 存款500 -^> 取款200 -^> 流水 -^> 退出
echo ------------------------------------------------------------
(echo 1001& echo 1& echo 2& echo 500& echo 3& echo 200& echo 5& echo 6& echo 0) | %TARGET%
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
