/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  framework.h —— 插件框架接口（管理器 + 配置化菜单 + 生命周期）
 * ============================================================
 *
 *  【第13讲成果的整合】
 *    第13讲给出了 framework.h 的接口设计，本讲把它落成真正的实现，
 *    并补上第11 / 12 / 13讲串起来时缺的那一环——**运行时从目录加载插件**。
 *
 *  【框架的职责（控制反转的关键）】
 *    1. 管理插件：加载 / 初始化 / 启动 / 停止 / 清理 / 卸载
 *    2. 配置化菜单：菜单由链表驱动，插件启动时挂菜单、停止时摘菜单
 *    3. 一键入口：framework_start → framework_run → framework_stop
 *
 *  【与控制反转（IoC）的关系】
 *    传统写法：主程序主动调用库函数（你调用库）
 *    框架写法：主程序只负责"把控制权交给框架"，
 *              由框架回调插件的 init/start/execute/stop/cleanup。
 *              "框架调用你的代码"——控制权反过来了，这就是 IoC。
 * ============================================================
 */

#ifndef FRAMEWORK_H
#define FRAMEWORK_H

#include "plugin.h"

/* ============================================================
 *  第一部分：插件管理器
 * ============================================================
 *  用链表管理插件（衔接第8讲链表 + 第12讲插件发现）
 *  节点内容从"数据"变成了"接口"。
 */

/* 初始化管理器 */
void manager_init(void);

/* 注册插件（尾插，保持注册顺序） */
int  manager_register(Plugin* p);

/* 依次调用所有插件的 init() */
int  manager_init_all(void);

/* 依次调用所有插件的 start()，并挂上配置化菜单 */
int  manager_start_all(void);

/* 依次调用所有插件的 stop()，并摘掉菜单 */
int  manager_stop_all(void);

/* 依次调用所有插件的 cleanup() */
void manager_cleanup_all(void);

/* 销毁管理器（释放链表节点，不负责卸载 DLL） */
void manager_destroy(void);

/* 按名称查找插件 */
Plugin* manager_find(const char* name);

/* 按名称执行插件 */
int  manager_execute(const char* name, double amount);

/* 已注册插件数量 */
int  manager_count(void);

/* 打印所有插件及其状态 */
void manager_print_all(void);

/* 状态枚举转文字 */
const char* plugin_state_name(PluginState s);

/* ============================================================
 *  第二部分：配置化菜单（链表实现）
 * ============================================================
 *  菜单项也是链表节点：
 *    添加菜单 = 按 id 有序插入（借用第8讲"有序插入"的技巧）
 *    删除菜单 = 链表删除节点
 *    显示菜单 = 遍历链表打印
 *  这样一来，菜单顺序与插件加载顺序无关，
 *  加一个插件只改 plugins/ 目录，不改主程序一行代码（开闭原则）。
 */
typedef struct MenuItem {
    int  id;                        /* 菜单编号 */
    char label[40];                 /* 菜单文字 */
    Plugin* plugin;                 /* 关联插件（NULL = 内置功能） */
    struct MenuItem* next;          /* 下一个菜单项 */
} MenuItem;

/* 菜单初始化 */
void menu_init(void);

/* 添加菜单项（按 id 升序有序插入） */
int  menu_add(int id, const char* label, Plugin* plugin);

/* 按 id 删除菜单项 */
int  menu_remove(int id);

/* 按 id 查找菜单项 */
MenuItem* menu_find(int id);

/* 显示整个菜单（遍历链表） */
void menu_show(void);

/* 菜单项数量 */
int  menu_count(void);

/* 销毁菜单链表 */
void menu_destroy(void);

/* ============================================================
 *  第三部分：框架入口
 * ============================================================
 *  main() 里只需要三行：
 *      framework_set_builtins(...);   // 可选：登记内置回退插件
 *      framework_start();             // 加载 + 注册 + init + start
 *      framework_run();               // 菜单交互循环
 *      framework_stop();              // stop + cleanup + 卸载
 */

/*
 * 登记"内置插件"作为动态加载的回退方案：
 *   若 plugins/ 里的同名 DLL 加载失败，框架自动启用内置实现，
 *   并打印一行说明——这就是课堂要演示的"优雅降级"。
 */
void framework_set_builtins(Plugin** builtins, int count);

/* 框架启动：初始化 + 动态加载 + 回退注册 + init_all + start_all */
void framework_start(void);

/* 框架运行：显示配置化菜单 + 交互循环；返回 0 正常退出 */
int  framework_run(void);

/* 框架停止：stop_all + cleanup_all + destroy + 卸载 DLL */
void framework_stop(void);

#endif /* FRAMEWORK_H */
