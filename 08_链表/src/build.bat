@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  第8讲：链表 —— 大小不再写死的数据结构
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  对比第7讲：数组（连续内存、大小固定） 换成 链表（指针串联、随用随长）
REM  链表是后面「插件注册表」「菜单项链表」的统一底座
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set TARGET=linked_atm.exe

echo ============================================================
echo   第8讲 链表 - 构建
echo ============================================================
echo.

echo [1/2] 正在编译 %TARGET% ...
gcc %CFLAGS% -o %TARGET% linked_atm.c
if errorlevel 1 goto fail
echo       OK -^> %TARGET%
echo.

if /i "%1"=="build" goto ok

echo [2/2] 自动演示：选账户1001 -^> 查询 -^> 存款500 -^> 取款200 -^> 链表管理演示 -^> 退出
echo ------------------------------------------------------------
(echo 1001& echo 1& echo 2& echo 500& echo 3& echo 200& echo 5& echo 7& echo 0) | %TARGET%
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
