@echo off
chcp 65001 >nul
REM ============================================================
REM 第11讲：运行时加载 - Windows 一键构建脚本
REM 依赖：MinGW gcc（已在 PATH 中）
REM
REM 产出：
REM   deposit_plugin.dll / withdraw_plugin.dll / query_plugin.dll
REM   broken_plugin.dll（反例：缺少约定符号，用于演示优雅报错）
REM   host.exe
REM   并把 4 个 dll 复制到 plugins\ 供 host.exe 扫描
REM ============================================================

setlocal
set CC=gcc
set CFLAGS=-Wall -Wextra -g

echo ============================================================
echo  第11讲：运行时加载 —— 构建
echo ============================================================
echo.

echo [步骤 1/4] 编译插件（动态库）...
%CC% %CFLAGS% -shared -o deposit_plugin.dll  deposit_plugin.c
if errorlevel 1 ( echo [错误] deposit_plugin.c 编译失败！& exit /b 1 )
echo   -^> deposit_plugin.dll

%CC% %CFLAGS% -shared -o withdraw_plugin.dll withdraw_plugin.c
if errorlevel 1 ( echo [错误] withdraw_plugin.c 编译失败！& exit /b 1 )
echo   -^> withdraw_plugin.dll

%CC% %CFLAGS% -shared -o query_plugin.dll    query_plugin.c
if errorlevel 1 ( echo [错误] query_plugin.c 编译失败！& exit /b 1 )
echo   -^> query_plugin.dll

%CC% %CFLAGS% -shared -o broken_plugin.dll   broken_plugin.c
if errorlevel 1 ( echo [错误] broken_plugin.c 编译失败！& exit /b 1 )
echo   -^> broken_plugin.dll  (反例，缺少 plugin_execute)

echo.
echo [步骤 2/4] 编译宿主程序...
%CC% %CFLAGS% -o host.exe host.c
if errorlevel 1 ( echo [错误] host.c 编译失败！& exit /b 1 )
echo   -^> host.exe

echo.
echo [步骤 3/4] 准备 plugins 目录并放入插件...
if not exist plugins mkdir plugins
copy /Y deposit_plugin.dll  plugins\ >nul
copy /Y withdraw_plugin.dll plugins\ >nul
copy /Y query_plugin.dll    plugins\ >nul
copy /Y broken_plugin.dll   plugins\ >nul
echo   -^> plugins\ 已就绪

echo.
echo [步骤 4/4] 构建完成！
echo ============================================================
echo  运行宿主观摩运行时加载效果：
echo      host.exe
echo ============================================================
echo.

endlocal
