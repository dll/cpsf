/*
 * ============================================================
 *  第11讲：运行时加载
 *  broken_plugin.c —— 一个"不守约"的插件（反例，用于演示报错）
 * ============================================================
 *
 *  这个库故意"不按约定来"：
 *    - 它导出了 plugin_name（名字叫得对）
 *    - 但功能入口叫 plugin_run，而不是约定的 plugin_execute
 *
 *  于是宿主扫描到它时会发生什么？
 *    dynlib_open 成功 → 查到 plugin_name 成功 →
 *    但 dynlib_sym(handle, "plugin_execute") 返回 NULL →
 *    宿主优雅地打印"缺少约定符号，跳过该文件"并 dlclose，
 *    而不是直接崩溃。
 *
 *  这就是"插件合法性校验"的雏形：
 *    按名字取符号，取不到就说明这不是一个合格的插件。
 *
 *  【教训】运行时加载把"调用什么函数"的决定权交给了字符串。
 *    字符串打错一个字母、插件忘记加导出宏、用 C++ 编译被
 *    名字修饰、或者函数被 static/隐藏了——都会导致取不到符号。
 *    所以宿主必须把"取不到符号"当成正常情况来处理，不能想当然。
 *
 *  编译命令：
 *    Windows: gcc -Wall -Wextra -shared -o broken_plugin.dll broken_plugin.c
 *    Linux  : gcc -Wall -Wextra -fPIC -shared -o broken_plugin.so broken_plugin.c
 */

#include "plugin_api.h"
#include <stdio.h>

/* 名字导出得很好，符合约定 */
PLUGIN_API const char *plugin_name(void)
{
    return "坏插件（缺少约定符号）";
}

/* 功能入口——但名字写错了！不是约定的 plugin_execute */
PLUGIN_API int plugin_run(double amount)
{
    printf("    [坏插件] 本不该被调用到这里，金额 %.2f\n", amount);
    return 0;
}
