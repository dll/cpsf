/*
 * ============================================================
 *  第11讲：运行时加载
 *  withdraw_plugin.c —— 取款插件（编译成独立动态库）
 * ============================================================
 *
 *  与 deposit_plugin.c 结构完全相同，只是功能变成"取款"。
 *
 *  【对比要点】两个插件是分别编译、分别加载的两个独立动态库。
 *    它们各自有自己的 g_balance，互不干扰——
 *    因为它们是两个不同的"模块实例"。
 *
 *    （真正的 ATM 当然应该共享同一个账户；等到第12讲把
 *      数据结构抽象成统一接口后，共享状态才好自然地表达。
 *      本讲的重点是"加载"这件事本身。）
 *
 *  编译命令：
 *    Windows: gcc -Wall -Wextra -shared -o withdraw_plugin.dll withdraw_plugin.c
 *    Linux  : gcc -Wall -Wextra -fPIC -shared -o withdraw_plugin.so withdraw_plugin.c
 */

#include "plugin_api.h"
#include <stdio.h>

/* 插件自己的状态：模拟一个账户的余额（演示用） */
static double g_balance = 1000.0;

/* 约定符号 1：返回插件名字 */
PLUGIN_API const char *plugin_name(void)
{
    return "取款插件";
}

/* 约定符号 2：执行取款 */
PLUGIN_API int plugin_execute(double amount)
{
    if (amount <= 0.0) {
        printf("    [取款插件] 金额 %.2f 非法，取款失败\n", amount);
        return -1;
    }
    if (amount > g_balance) {
        printf("    [取款插件] 余额不足（余额 %.2f，需取 %.2f）\n",
               g_balance, amount);
        return -1;
    }

    g_balance -= amount;
    printf("    [取款插件] 取出 %.2f 元，"
           "当前余额 %.2f 元\n", amount, g_balance);
    return 0;
}
