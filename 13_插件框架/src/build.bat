@echo off
chcp 65001 >nul 2>&1
rem ============================================================
rem  第13讲：插件框架架构  —— 一键构建脚本（Windows）
rem ============================================================
rem  用法：
rem    build.bat          编译并自动运行演示
rem    build.bat build    只编译，不运行
rem ============================================================
setlocal

set TARGET=plugin_framework.exe
set SRCS=framework.c atm_state.c plugin_deposit.c plugin_withdraw.c plugin_query.c plugin_transfer.c main.c
set CFLAGS=-Wall -O2

echo ============================================
echo   第13讲 插件框架 - 构建
echo ============================================
echo.

gcc %CFLAGS% -o %TARGET% %SRCS%
if errorlevel 1 (
    echo.
    echo [失败] 编译出错，请检查上面的报错信息。
    exit /b 1
)

echo [成功] 已生成 %TARGET%
echo.

if /i "%1"=="build" (
    echo 跳过运行（build 模式）。
    exit /b 0
)

echo ============================================
echo   自动演示：喂入菜单输入
echo     1 -^> 500 （存款 500）
echo     2 -^> 200 （取款 200）
echo     3 -^> 0   （查询余额）
echo     4 -^> 300 （转账 300）
echo     0         （退出）
echo ============================================
echo.

(echo 1& echo 500& echo 2& echo 200& echo 3& echo 0& echo 4& echo 300& echo 0) | %TARGET%

echo.
echo ============================================
echo   运行结束
echo ============================================
endlocal
