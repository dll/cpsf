/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  plugins/plugins.h —— 插件实现清单（内置回退 + 动态库共用）
 * ============================================================
 *
 *  每个插件源文件都提供 xxx_plugin_create()：
 *    · 编译成 DLL 时（定义 PLUGIN_DLL），额外导出 get_plugin 符号
 *    · 直接编进主程序时，用 create() 拿到实例作为"内置回退"
 *
 *  同一份源码、两种用法，避免为"回退"再抄一遍插件逻辑。
 * ============================================================
 */

#ifndef PLUGINS_H
#define PLUGINS_H

#include "plugin.h"

/* 返回各插件的单例实例（静态存储，无需释放） */
Plugin* deposit_plugin_create(void);    /* 存款 */
Plugin* withdraw_plugin_create(void);   /* 取款 */
Plugin* query_plugin_create(void);      /* 查询 */
Plugin* transfer_plugin_create(void);   /* 转账 */

#endif /* PLUGINS_H */
