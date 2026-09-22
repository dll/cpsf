@echo off
chcp 65001 >nul
echo ========================================
echo   第2阶段：函数封装 - 编译脚本
echo ========================================
echo.

echo [1/2] 编译进化前版本（屎山main）...
gcc atm_bad.c -o atm_bad.exe
if %errorlevel%==0 (
    echo ✅ 编译成功：atm_bad.exe
) else (
    echo ❌ 编译失败
)

echo.
echo [2/2] 编译进化后版本（函数封装）...
gcc atm_good.c -o atm_good.exe
if %errorlevel%==0 (
    echo ✅ 编译成功：atm_good.exe
) else (
    echo ❌ 编译失败
)

echo.
echo ========================================
echo   编译完成！
echo   运行 atm_bad.exe 查看屎山版本
echo   运行 atm_good.exe 查看封装版本
echo ========================================
pause
