/*
 * ============================================================
 *  第11讲：运行时加载
 *  deposit_plugin.c —— 存款插件（编译成独立动态库）
 * ============================================================
 *
 *  这个文件会被单独编译成一个动态库（deposit_plugin.dll / .so），
 *  它不链接进宿主程序，而是被宿主在运行时"按需加载"。
 *
 *  编译命令：
 *    Windows: gcc -Wall -Wextra -shared -o deposit_plugin.dll deposit_plugin.c
 *    Linux  : gcc -Wall -Wextra -fPIC -shared -o deposit_plugin.so deposit_plugin.c
 *
 *  它必须导出 plugin_api.h 里约定的两个符号：
 *    plugin_name    —— 告诉宿主"我叫什么"
 *    plugin_execute —— 宿主真正调用的功能入口
 *
 *  【关键理解】插件内部用 static 变量保存自己的状态。
 *    因为插件是被加载进"宿主的进程"里运行的，
 *    这块内存会一直存在，直到这个库被 dlclose/FreeLibrary 卸载。
 *    所以每次调用 plugin_execute，余额都能累加——
 *    这正好说明"库是一个活着的、有状态的模块"，而不只是一段代码。
 */

#include "plugin_api.h"
#include <stdio.h>

/* 插件自己的状态：模拟一个账户的余额（演示用） */
static double g_balance = 1000.0;

/* ------------------------------------------------------------
 *  约定符号 1：plugin_name
 *  返回插件名字，宿主加载后先调用它，打印"我加载了谁"。
 * ------------------------------------------------------------ */
PLUGIN_API const char *plugin_name(void)
{
    return "存款插件";
}

/* ------------------------------------------------------------
 *  约定符号 2：plugin_execute
 *  执行"存款"这件事：把金额加到余额上。
 *  返回值：0 成功，-1 失败（金额非法）。
 * ------------------------------------------------------------ */
PLUGIN_API int plugin_execute(double amount)
{
    if (amount <= 0.0) {
        printf("    [存款插件] 金额 %.2f 非法，存款失败\n", amount);
        return -1;
    }

    g_balance += amount;
    printf("    [存款插件] 存入 %.2f 元，"
           "当前余额 %.2f 元\n", amount, g_balance);
    return 0;
}
