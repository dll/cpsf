@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM  第12讲：接口抽象 —— 结构体里装函数指针
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  对比第11讲：宿主不再靠字符串 "plugin_execute" 硬编码调用，
REM  而是约定一个 struct Plugin { 名称 + init/execute/cleanup 函数指针 }
REM  同一个接口，不同实现 —— 这就是 C 语言里的「多态」
REM
REM  本讲插件是编译进主程序的（重点在接口，不在加载）
REM  真正的「运行时加载」见第11讲，二者在第14讲合流
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set TARGET=plugin_atm.exe

echo ============================================================
echo   第12讲 接口抽象 - 构建
echo ============================================================
echo.

echo [1/2] 正在编译 %TARGET% ...
gcc %CFLAGS% -o %TARGET% plugin_atm.c
if errorlevel 1 goto fail
echo       OK -^> %TARGET%
echo.

if /i "%1"=="build" goto ok

echo [2/2] 自动演示（注册 -^> 发现 -^> 遍历 -^> 多态调用 -^> 清理）
echo ------------------------------------------------------------
%TARGET%
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
