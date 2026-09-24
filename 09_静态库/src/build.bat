@echo off
REM ============================================================
REM 第9讲：静态库 - Windows构建脚本
REM 使用 MinGW gcc 编译，ar 打包静态库
REM ============================================================

set CC=gcc
set CFLAGS=-Wall -Wextra -g
set LIB_NAME=libaccount.a
set TARGET=atm_static.exe

echo ============================================================
echo  第9讲：静态库构建
echo ============================================================
echo.

echo [步骤1] 编译 account.c ...
%CC% %CFLAGS% -c account.c -o account.o
if errorlevel 1 (
    echo [错误] account.c 编译失败！
    exit /b 1
)
echo   -> account.o 生成成功

echo [步骤2] 编译 transaction.c ...
%CC% %CFLAGS% -c transaction.c -o transaction.o
if errorlevel 1 (
    echo [错误] transaction.c 编译失败！
    exit /b 1
)
echo   -> transaction.o 生成成功

echo [步骤3] 用 ar 打包静态库 %LIB_NAME% ...
ar rcs %LIB_NAME% account.o transaction.o
if errorlevel 1 (
    echo [错误] 静态库创建失败！
    exit /b 1
)
echo   -> %LIB_NAME% 创建成功！
echo      包含: account.o + transaction.o

echo [步骤4] 编译 main.c ...
%CC% %CFLAGS% -c main.c -o main.o
if errorlevel 1 (
    echo [错误] main.c 编译失败！
    exit /b 1
)
echo   -> main.o 生成成功

echo [步骤5] 链接可执行文件（静态链接）...
%CC% %CFLAGS% -o %TARGET% main.o -L. -laccount
if errorlevel 1 (
    echo [错误] 链接失败！
    exit /b 1
)
echo   -> %TARGET% 链接成功！
echo      方式: 从 libaccount.a 复制代码到可执行文件

echo.
echo ============================================================
echo  构建完成！运行 %TARGET% 体验ATM静态库版
echo ============================================================
echo.
echo  查看静态库内容: ar t %LIB_NAME%
echo  查看符号表:     nm %LIB_NAME%
echo.
