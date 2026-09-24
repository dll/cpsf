@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  第7讲：结构体 —— 把散落的数据打包成一个「东西」
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  对比第6讲：多个平行数组 换成 struct Account / struct Transaction
REM  结构体 = 自定义类型，是第12讲「接口（结构体+函数指针）」的前置知识
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set TARGET=struct_atm.exe

echo ============================================================
echo   第7讲 结构体 - 构建
echo ============================================================
echo.

echo [1/2] 正在编译 %TARGET% ...
gcc %CFLAGS% -o %TARGET% struct_atm.c
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
