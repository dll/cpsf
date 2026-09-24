@echo off
REM ============================================================
REM  第14讲：完整项目与总结展望
REM  build.bat —— Windows 一键构建（MinGW / TDM-GCC）
REM ============================================================
REM  构建三步：
REM    1) 编译共享账务核心 atmcore.dll（主程序与所有插件共享它的数据）
REM    2) 编译四个插件为独立 DLL，输出到 plugins\ 目录
REM    3) 编译主程序 atm_framework.exe（框架 + 动态加载器 + 内置回退插件）
REM
REM  运行前请确保 gcc 在 PATH 中：
REM    gcc --version
REM ============================================================

setlocal
cd /d "%~dp0"

set CFLAGS=-Wall -O2
set CORE=account.c transaction.c
set PLUGIN_NAMES=deposit withdraw query transfer

echo ============================================================
echo   第14讲 完整项目构建
echo ============================================================
echo.

REM ---------- 第 1 步：共享账务核心 ----------
echo [1/3] 编译共享账务核心 atmcore.dll ...
gcc %CFLAGS% -shared -o atmcore.dll %CORE% -Wl,--out-implib,libatmcore.a -DATMCORE_BUILD
if errorlevel 1 goto fail
echo       OK  -> atmcore.dll + libatmcore.a
echo.

REM ---------- 第 2 步：插件 DLL ----------
echo [2/3] 编译插件 DLL 到 plugins\ ...
if not exist plugins mkdir plugins
for %%P in (%PLUGIN_NAMES%) do (
    echo       编译 plugins\%%P_plugin.dll ...
    gcc %CFLAGS% -shared -DPLUGIN_DLL -o plugins\%%P_plugin.dll plugins\%%P_plugin.c -I. -Iplugins -L. -latmcore
    if errorlevel 1 goto fail
)
echo       OK  -> 4 个插件 DLL
echo.

REM ---------- 第 3 步：主程序 ----------
echo [3/3] 编译主程序 atm_framework.exe ...
gcc %CFLAGS% -o atm_framework.exe main.c framework.c dynamic_loader.c ^
    plugins\deposit_plugin.c plugins\withdraw_plugin.c plugins\query_plugin.c plugins\transfer_plugin.c ^
    -I. -Iplugins -L. -latmcore
if errorlevel 1 goto fail
echo       OK  -> atm_framework.exe
echo.

echo ============================================================
echo   构建成功！
echo ------------------------------------------------------------
echo   直接运行：
echo     atm_framework.exe
echo.
echo   管道测试（存500 - 取200 - 查余额 - 转100到1002 - 插件列表 - 退出）：
echo     在 Git Bash 中执行：
echo     printf '1\n500\n2\n200\n3\n0\n4\n1002\n100\n9\n0\n' ^| ./atm_framework.exe
echo ============================================================
goto end

:fail
echo.
echo [构建失败] 请检查上面的错误信息。
exit /b 1

:end
endlocal
