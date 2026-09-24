/*
 * ============================================================
 *  第12讲：接口抽象与插件发现
 *  plugin.h —— 插件接口定义（统一契约）
 * ============================================================
 *
 *  【核心思想】
 *    第11讲我们学会了 dlopen/dlsym 运行时加载动态库，
 *    但光能加载还不够——每个插件的函数名、参数都不同，
 *    调用方需要知道每个插件的细节，耦合度太高。
 *
 *    解决方案：定义统一的 Plugin 接口（结构体 + 函数指针），
 *    所有插件都实现这个接口，调用方只需要通过接口调用，
 *    不需要知道具体插件的实现细节——这就是多态！
 *
 *  【类比】
 *    USB接口：不管你插的是鼠标、键盘还是U盘，
 *    电脑只管通过USB协议通信，不关心设备内部实现。
 *    Plugin接口 = C语言版的USB接口
 *
 *  编译运行：
 *    gcc -Wall -o plugin_atm plugin_atm.c && ./plugin_atm
 * ============================================================
 */

#ifndef PLUGIN_H
#define PLUGIN_H

/*
 * ============================================================
 *  插件接口结构体 —— C语言的"接口"
 * ============================================================
 *
 *  【对比第5讲函数指针】
 *    第5讲：int (*fp)(int, int);  // 一个函数指针
 *    现在：把多个函数指针打包到结构体里 = 接口
 *
 *  【对比第7讲结构体】
 *    第7讲：结构体打包的是数据（id, name, balance）
 *    现在：结构体打包的是函数指针（init, execute, cleanup）
 *         从"数据封装"升级为"行为封装"
 *
 *  【对比面向对象】
 *    Java: interface Plugin { void init(); void execute(); void cleanup(); }
 *    C语言: 用结构体 + 函数指针模拟 interface
 *
 *  Plugin 接口要求每个插件实现三个方法：
 *    init()    —— 初始化插件（打开文件、分配资源等）
 *    execute() —— 执行插件功能（存款、取款、查询等）
 *    cleanup() —— 清理资源（关闭文件、释放内存等）
 *
 *  这就是插件的"生命周期"：
 *    加载 → init → execute(可多次) → cleanup → 卸载
 */

/* 插件接口结构体：定义所有插件必须实现的"契约" */
typedef struct Plugin {
    char name[32];              /* 插件名称（如"存款"、"取款"） */
    char version[16];           /* 插件版本号 */
    char description[64];       /* 插件功能描述 */

    /* ---- 函数指针：插件的行为 ---- */
    /* init: 初始化插件，返回0成功，非0失败 */
    int  (*init)(struct Plugin* self);

    /* execute: 执行插件功能，参数为操作金额 */
    int  (*execute)(struct Plugin* self, double amount);

    /* cleanup: 清理插件资源 */
    void (*cleanup)(struct Plugin* self);

} Plugin;

/*
 * ============================================================
 *  插件节点 —— 链表管理（衔接第8讲链表）
 * ============================================================
 *
 *  每个加载的插件 = 链表中的一个节点
 *  通过遍历链表，可以统一调用所有插件的 execute()
 *
 *  【对比第8讲】
 *    第8讲链表节点：数据域(amount) + 指针域(next)
 *    插件链表节点：Plugin接口 + 指针域(next)
 *    从"管理数据"升级为"管理行为"
 */
typedef struct PluginNode {
    Plugin* plugin;                  /* 指向插件接口 */
    struct PluginNode* next;          /* 指向下一个插件节点 */
} PluginNode;

/*
 * ============================================================
 *  插件管理器 —— 注册/查找/遍历（链表操作）
 * ============================================================
 *
 *  对外提供的函数声明（实现在 plugin_atm.c 中）
 */

/* 初始化插件管理器 */
void plugin_manager_init(void);

/* 注册插件到链表（头部插入，O(1)） */
int  plugin_register(Plugin* p);

/* 按名称查找插件 */
Plugin* plugin_find(const char* name);

/* 执行所有插件的 init() */
void plugin_init_all(void);

/* 执行所有插件的 execute() */
void plugin_execute_all(double amount);

/* 执行所有插件的 cleanup() */
void plugin_cleanup_all(void);

/* 销毁插件管理器（释放链表） */
void plugin_manager_destroy(void);

/* 打印已注册的插件列表 */
void plugin_list_print(void);

/* 扫描目录自动发现并加载插件 */
int  plugin_scan_directory(const char* dir_path);

/* 获取已注册插件数量 */
int  plugin_count(void);

#endif /* PLUGIN_H */
