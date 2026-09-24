@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  第2讲：控制结构 —— ATM 简易菜单
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  本讲重点：顺序 / 分支 / 循环 三种控制结构
REM  全部代码都在 main 里，为第3讲「函数封装」埋下伏笔
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set TARGET=atm_menu.exe

echo ============================================================
echo   第2讲 控制结构 - 构建
echo ============================================================
echo.

echo [1/2] 正在编译 %TARGET% ...
gcc %CFLAGS% -o %TARGET% atm_menu.c
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
