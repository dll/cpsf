@echo off
REM ============================================
REM 第1阶段：你好世界 - 编译脚本
REM ============================================
REM 使用 GCC 编译 hello.c
REM 输出：hello.exe
REM ============================================

echo [编译中] 使用 GCC 编译 hello.c ...
gcc -Wall -o hello.exe hello.c

if %ERRORLEVEL% EQU 0 (
    echo [编译成功] 生成 hello.exe
    echo.
    echo [运行程序]
    hello.exe
) else (
    echo [编译失败] 请检查代码
)

echo.
pause
