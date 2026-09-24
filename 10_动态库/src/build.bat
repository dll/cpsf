@echo off
chcp 65001 >nul 2>&1
REM ============================================================
REM 第10讲：动态库 - Windows 构建脚本
REM 使用 MinGW gcc 编译 account.dll（含导入库 libaccount.dll.a）
REM 并链接主程序 atm_dynamic.exe
REM
REM 与第9讲静态库的区别：
REM   静态库 ar rcs libaccount.a ...   —— 打包 .o
REM   动态库 gcc -shared ... account.dll —— 生成 .dll + 导入库 .dll.a
REM ============================================================

set CC=gcc
set CFLAGS=-Wall -Wextra -g
set DLL_NAME=account.dll
set IMPLIB=libaccount.dll.a
set TARGET=atm_dynamic.exe

REM 编译动态库时定义导出宏，ACCOUNT_API / TRANSACTION_API 展开为 dllexport
set DEFS=-DACCOUNT_EXPORTS -DTRANSACTION_EXPORTS

echo ============================================================
echo  第10讲：动态库构建
echo ============================================================
echo.

echo [步骤1] 编译动态库 %DLL_NAME% ...
REM -shared       生成动态库
REM -Wl,--out-implib  同时生成导入库 libaccount.dll.a（链接时用）
%CC% %CFLAGS% -shared -o %DLL_NAME% account.c transaction.c -Wl,--out-implib,%IMPLIB% %DEFS%
if errorlevel 1 (
    echo [错误] 动态库编译失败！
    exit /b 1
)
echo   -^> %DLL_NAME% 生成成功
echo   -^> %IMPLIB% 导入库生成成功
echo.

echo [步骤2] 链接主程序 %TARGET% ...
REM 链接的是导入库 libaccount.dll.a，运行时才加载真正的 account.dll
%CC% %CFLAGS% -o %TARGET% main.c -L. -laccount
if errorlevel 1 (
    echo [错误] 主程序链接失败！
    exit /b 1
)
echo   -^> %TARGET% 链接成功！
echo      方式: 加载时链接（exe 只记录导入表，启动时由 OS 加载 %DLL_NAME%）
echo.

echo ============================================================
echo  构建完成！请确保 %DLL_NAME% 与 %TARGET% 在同一目录再运行
echo ============================================================
echo.
echo  查看 dll 导出的符号: objdump -p %DLL_NAME% ^| findstr "Export"
echo  运行程序: %TARGET%
echo  清理产物: del *.o *.dll *.a *.exe
echo.
