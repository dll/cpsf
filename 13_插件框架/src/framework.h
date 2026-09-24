/*
 * ============================================================
 *  第13讲：插件框架架构
 *  framework.h —— 插件框架核心接口定义
 * ============================================================
 *
 *  【本讲核心】
 *    第12讲我们定义了 Plugin 接口，实现了注册和发现。
 *    但还缺一个"管理者"——谁来管理插件的完整生命周期？
 *    谁来提供扩展点？谁来管理配置化菜单？
 *
 *    本讲构建完整的插件框架，包含：
 *    1. 扩展的 Plugin 接口（init/start/stop/cleanup 四阶段生命周期）
 *    2. 插件管理器（统一管理加载/启动/停止/卸载）
 *    3. 配置化菜单（链表实现，插件动态注册菜单项）
 *    4. 开闭原则（加插件不改代码）
 *
 *  编译运行：
 *    gcc -Wall -o plugin_framework framework.c && ./plugin_framework
 *
 *  【补充说明（第13讲实现时补注）】
 *    上面的命令只编译了 framework.c，是为了突出"框架核心"。
 *    完整工程还包含 ATM 共享状态、4 个内置插件和主程序，实际构建请用：
 *      Windows： build.bat
 *      Linux / MinGW： make   （或 make run 自动演示）
 *    或手工：
 *      gcc -Wall -o plugin_framework framework.c atm_state.c \
 *          plugin_deposit.c plugin_withdraw.c plugin_query.c \
 *          plugin_transfer.c main.c
 *
 *    注意：本头文件是"契约"，函数名、参数、结构体字段、状态枚举
 *          一律不得改动；framework.c 必须严格实现下列声明。
 * ============================================================
 */

#ifndef FRAMEWORK_H
#define FRAMEWORK_H

/*
 * ============================================================
 *  第一部分：扩展的 Plugin 接口（完整生命周期）
 * ============================================================
 *
 *  【对比第12讲】
 *    第12讲：init → execute → cleanup （3阶段）
 *    第13讲：init → start → execute → stop → cleanup （5阶段）
 *
 *  为什么需要 start/stop？
 *    init: 分配资源、初始化数据（可能还没准备好服务）
 *    start: 开始提供服务（注册菜单项、监听事件等）
 *    stop: 停止服务（取消注册、停止监听）
 *    cleanup: 释放资源
 *
 *  生命周期状态机：
 *    UNLOADED → LOADED → INITIALIZED → STARTED → STOPPED → CLEANED → UNLOADED
 */

/* 插件状态 */
typedef enum {
    PLUGIN_UNLOADED = 0,     /* 未加载 */
    PLUGIN_LOADED,           /* 已加载（dlopen成功） */
    PLUGIN_INITIALIZED,      /* 已初始化（init成功） */
    PLUGIN_STARTED,          /* 已启动（start成功） */
    PLUGIN_STOPPED,          /* 已停止（stop成功） */
    PLUGIN_CLEANED           /* 已清理（cleanup成功） */
} PluginState;

/* 扩展的插件接口（完整生命周期） */
typedef struct Plugin {
    /* ---- 元数据 ---- */
    char name[32];              /* 插件名称 */
    char version[16];           /* 版本号 */
    char description[64];       /* 功能描述 */
    int  menu_id;               /* 菜单编号（0=无菜单项） */
    char menu_label[40];        /* 菜单显示文字 */

    /* ---- 生命周期方法（函数指针） ---- */
    int  (*init)(struct Plugin* self);        /* 初始化：分配资源 */
    int  (*start)(struct Plugin* self);       /* 启动：开始服务 */
    int  (*execute)(struct Plugin* self, double amount);  /* 执行核心功能 */
    int  (*stop)(struct Plugin* self);        /* 停止：停止服务 */
    void (*cleanup)(struct Plugin* self);     /* 清理：释放资源 */

    /* ---- 私有数据（类似C++的private成员） ---- */
    void* user_data;            /* 插件私有数据指针 */

    /* ---- 运行时状态 ---- */
    PluginState state;          /* 当前状态 */

} Plugin;

/*
 * ============================================================
 *  第二部分：插件节点（链表管理）
 * ============================================================
 *  衔接第8讲链表 + 第12讲插件链表
 */
typedef struct PluginNode {
    Plugin* plugin;
    struct PluginNode* next;
} PluginNode;

/*
 * ============================================================
 *  第三部分：插件管理器
 * ============================================================
 *
 *  管理器的职责（类似C++的PluginManager类）：
 *    1. 加载插件（register）
 *    2. 初始化所有插件（init_all）
 *    3. 启动所有插件（start_all）
 *    4. 查找插件（find）
 *    5. 执行插件（execute）
 *    6. 停止所有插件（stop_all）
 *    7. 清理所有插件（cleanup_all）
 *    8. 卸载所有插件（destroy）
 *
 *  对外提供完整的生命周期管理接口
 */

/* 初始化管理器 */
void manager_init(void);

/* 注册插件到管理器 */
int  manager_register(Plugin* p);

/* 初始化所有已注册插件 */
int  manager_init_all(void);

/* 启动所有插件 */
int  manager_start_all(void);

/* 停止所有插件 */
int  manager_stop_all(void);

/* 清理所有插件 */
void manager_cleanup_all(void);

/* 销毁管理器（释放链表） */
void manager_destroy(void);

/* 按名称查找插件 */
Plugin* manager_find(const char* name);

/* 执行指定插件 */
int  manager_execute(const char* name, double amount);

/* 获取插件数量 */
int  manager_count(void);

/* 打印所有插件及状态 */
void manager_print_all(void);

/*
 * ============================================================
 *  第四部分：配置化菜单（链表实现）
 * ============================================================
 *
 *  【核心思想】
 *    第2讲的菜单是写死的：
 *      printf("1. 存款\n");
 *      printf("2. 取款\n");
 *
 *    现在用链表实现动态菜单：
 *      插件注册时自动添加菜单项
 *      插件卸载时自动删除菜单项
 *      菜单完全由链表驱动，不需要改代码！
 *
 *  菜单项节点 = 链表节点
 *    菜单显示 = 遍历链表打印
 *    添加菜单 = 链表尾部插入
 *    删除菜单 = 链表删除节点
 */

/* 菜单项节点 */
typedef struct MenuItem {
    int  id;                        /* 菜单编号 */
    char label[40];                 /* 菜单文字 */
    Plugin* plugin;                 /* 关联的插件 */
    struct MenuItem* next;          /* 指向下一个菜单项 */
} MenuItem;

/* 菜单初始化 */
void menu_init(void);

/* 添加菜单项（尾部插入，保持顺序） */
int  menu_add(int id, const char* label, Plugin* plugin);

/* 删除菜单项（按ID） */
int  menu_remove(int id);

/* 显示菜单（遍历链表打印） */
void menu_show(void);

/* 处理用户选择 */
int  menu_handle(int choice, double amount);

/* 销毁菜单 */
void menu_destroy(void);

/*
 * ============================================================
 *  第五部分：框架入口（一键启动/关闭）
 * ============================================================
 *
 *  框架提供"一键"操作，简化使用：
 *    framework_start() → 初始化 + 注册 + init + start
 *    framework_run()   → 显示菜单 + 处理用户输入
 *    framework_stop()  → stop + cleanup + destroy
 */

/* 框架启动（初始化管理器 + 菜单 + 注册内置插件 + init + start） */
int  framework_start(void);

/* 框架运行（显示菜单 + 交互循环） */
int  framework_run(void);

/* 框架停止（stop + cleanup + destroy） */
void framework_stop(void);

#endif /* FRAMEWORK_H */
