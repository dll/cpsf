/*
 * ============================================================
 *  第13讲：插件框架架构
 *  plugins.h —— 内置插件工厂函数声明
 * ============================================================
 *
 *  【工厂函数：create_xxx_plugin()】
 *    为什么不让框架直接 extern 一个 Plugin 变量？
 *      1. 变量在别的文件里是 static 的（第4讲：static 限制作用域），
 *         外部拿不到，只能靠函数把指针"交出去"；
 *      2. 工厂函数是统一入口：将来改成从动态库读取（第11讲 dlopen），
 *         函数名不变，框架代码一行都不用改。
 *
 *  这正是"依赖稳定点"的做法：
 *    框架依赖的是 create_xxx_plugin 这个稳定的名字，
 *    而不是插件内部千变万化的实现。
 * ============================================================
 */

#ifndef PLUGINS_H
#define PLUGINS_H

#include "framework.h"

/* 内置插件工厂函数：返回指向插件实例的指针 */
Plugin* create_deposit_plugin(void);    /* 存款   menu_id = 1 */
Plugin* create_withdraw_plugin(void);   /* 取款   menu_id = 2 */
Plugin* create_query_plugin(void);      /* 查余额 menu_id = 3 */
Plugin* create_transfer_plugin(void);   /* 转账   menu_id = 4 */

#endif /* PLUGINS_H */
