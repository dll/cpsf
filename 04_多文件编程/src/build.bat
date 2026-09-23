@echo off
chcp 65001 >nul 2>&1

echo ============================================
echo   多文件ATM项目编译脚本
echo   第4讲：多文件编程
echo ============================================
echo.

echo [1/2] 正在编译...
gcc main.c menu.c account.c utils.c -o atm_multi.exe -Wall

if %errorlevel% equ 0 (
    echo.
    echo [2/2] 编译成功！
    echo.
    echo 生成的可执行文件：atm_multi.exe
    echo.
    echo 编译过程说明：
    echo   gcc 会把 4 个 .c 文件分别编译成 .o 目标文件
    echo   然后链接器把 4 个 .o 拼成 1 个 .exe
    echo.
    echo 各模块职责：
    echo   main.c     - 程序入口，调度各模块
    echo   menu.c     - 菜单显示和输入
    echo   account.c  - 账户业务（余额管理）
    echo   utils.c    - 工具函数（提示信息）
    echo.
    echo 运行方式：atm_multi.exe
) else (
    echo.
    echo [错误] 编译失败！请检查代码。
    echo.
    echo 常见错误：
    echo   1. 忘记包含头文件（#include "xxx.h"）
    echo   2. 头文件保护写错（#ifndef / #define / #endif）
    echo   3. 函数声明和定义不一致
)

echo.
pause
