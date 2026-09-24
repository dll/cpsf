/*
 * ============================================================
 *  第11讲：运行时加载
 *  query_plugin.c —— 查询插件（编译成独立动态库）
 * ============================================================
 *
 *  查询插件不需要金额参数，但为了满足统一约定的
 *  plugin_execute(double amount)，它把 amount 忽略掉，直接报告余额。
 *
 *  【这就是本讲要留下的"新痛点"】
 *    约定只统一了"函数名"，没有统一"参数含义"。
 *    查询插件根本用不上 amount，却被迫带着这个参数；
 *    反过来，如果将来有个"转账插件"要传两个账户加金额，
 *    这个 double 参数又根本不够用。
 *
 *    宿主这边也只能按"金额"这一种语义去调用所有插件，
 *    无法区分"这个插件其实不需要金额"。
 *
 *    → 光统一名字是不够的，必须把"参数、返回值、元数据"
 *      一起抽象成一个统一接口结构体，这就是第12讲的课题。
 *
 *  编译命令：
 *    Windows: gcc -Wall -Wextra -shared -o query_plugin.dll query_plugin.c
 *    Linux  : gcc -Wall -Wextra -fPIC -shared -o query_plugin.so query_plugin.c
 */

#include "plugin_api.h"
#include <stdio.h>

/* 插件自己的状态：模拟一个账户的余额（演示用） */
static double g_balance = 1000.0;

/* 约定符号 1：返回插件名字 */
PLUGIN_API const char *plugin_name(void)
{
    return "查询插件";
}

/* 约定符号 2：执行查询（本插件忽略 amount 参数） */
PLUGIN_API int plugin_execute(double amount)
{
    /* 查询不需要金额，参数用 (void) 显式忽略，避免编译告警 */
    (void)amount;

    printf("    [查询插件] 当前余额：%.2f 元\n", g_balance);
    return 0;
}
