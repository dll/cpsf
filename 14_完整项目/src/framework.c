/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  framework.c —— 插件框架实现
 * ============================================================
 *
 *  本文件把全系列的知识点"拧成一股绳"：
 *    · 指针 / 函数指针（第5讲）    → Plugin 接口的函数指针
 *    · 结构体（第7讲）             → Plugin / PluginNode / MenuItem
 *    · 链表（第8讲）               → 插件链表、菜单链表、流水链表
 *    · 静态库 / 动态库（第9/10讲） → atmcore.dll 共享账务数据
 *    · 运行时加载（第11讲）        → dynamic_loader 扫描并加载 plugins/
 *    · 接口抽象（第12讲）          → 面向 Plugin 接口编程，多态调用
 *    · 插件框架（第13讲）          → 生命周期 + 管理器 + 配置化菜单
 *
 *  编译：随主程序一起编译，链接 atmcore.dll（见 build.bat / Makefile）
 * ============================================================
 */

#include "framework.h"
#include "dynamic_loader.h"
#include "account.h"
#include "transaction.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ============================================================
 *  全局状态
 * ============================================================
 *  管理器的链表用"头 + 尾 + 计数"三件套（第8讲尾插法）。
 */
static PluginNode *g_head = NULL;
static PluginNode *g_tail = NULL;
static int         g_count = 0;

/* 菜单链表（用头指针即可，有序插入不需要尾指针） */
static MenuItem *g_menu_head = NULL;
static int       g_menu_count = 0;

/* 已加载的动态库：退出时统一卸载，避免"加载了却没人管" */
typedef struct LoadedLib {
    DllHandle handle;
    char      path[512];
    struct LoadedLib *next;
} LoadedLib;
static LoadedLib *g_libs = NULL;

/* 内置回退插件（由 main.c 登记） */
static Plugin **g_builtins = NULL;
static int      g_builtin_count = 0;

/* ============================================================
 *  第一部分：插件管理器
 * ============================================================ */

const char* plugin_state_name(PluginState s)
{
    switch (s) {
        case PLUGIN_UNLOADED:    return "未加载";
        case PLUGIN_LOADED:      return "已加载";
        case PLUGIN_INITIALIZED: return "已初始化";
        case PLUGIN_STARTED:     return "已启动";
        case PLUGIN_STOPPED:     return "已停止";
        case PLUGIN_CLEANED:     return "已清理";
        default:                 return "未知";
    }
}

void manager_init(void)
{
    g_head = NULL;
    g_tail = NULL;
    g_count = 0;
}

int manager_register(Plugin* p)
{
    if (p == NULL) {
        printf("  [管理器] 拒绝注册空插件\n");
        return -1;
    }

    /* 去重：插件是系统的唯一标识，同名不允许重复注册 */
    if (manager_find(p->name) != NULL) {
        printf("  [管理器] 插件[%s]已存在，跳过注册\n", p->name);
        return -2;
    }

    PluginNode* node = (PluginNode*)malloc(sizeof(PluginNode));
    if (node == NULL) {
        printf("  [管理器] 内存分配失败\n");
        return -3;
    }
    node->plugin = p;
    node->next = NULL;

    if (g_head == NULL) {
        g_head = node;
        g_tail = node;
    } else {
        g_tail->next = node;
        g_tail = node;
    }
    g_count++;

    if (p->state == PLUGIN_UNLOADED) {
        p->state = PLUGIN_LOADED;
    }
    printf("  [注册] %-10s v%-4s menu=%d  %s\n",
           p->name, p->version, p->menu_id, p->description);
    return 0;
}

Plugin* manager_find(const char* name)
{
    PluginNode* cur = g_head;
    if (name == NULL) {
        return NULL;
    }
    while (cur != NULL) {
        if (strcmp(cur->plugin->name, name) == 0) {
            return cur->plugin;
        }
        cur = cur->next;
    }
    return NULL;
}

int manager_count(void)
{
    return g_count;
}

int manager_init_all(void)
{
    PluginNode* cur = g_head;
    int ok = 0;
    printf("\n--- 初始化所有插件 ---\n");
    while (cur != NULL) {
        Plugin* p = cur->plugin;
        if (p->init != NULL && p->init(p) == 0) {
            p->state = PLUGIN_INITIALIZED;
            ok++;
        } else {
            printf("  [警告] 插件[%s] 初始化失败，将跳过启动\n", p->name);
        }
        cur = cur->next;
    }
    return ok;
}

int manager_start_all(void)
{
    PluginNode* cur = g_head;
    int ok = 0;
    printf("\n--- 启动所有插件（挂载菜单）---\n");
    while (cur != NULL) {
        Plugin* p = cur->plugin;
        if (p->state != PLUGIN_INITIALIZED) {
            printf("  [跳过] 插件[%s] 未初始化\n", p->name);
            cur = cur->next;
            continue;
        }
        if (p->start == NULL || p->start(p) != 0) {
            printf("  [警告] 插件[%s] 启动失败\n", p->name);
            cur = cur->next;
            continue;
        }
        p->state = PLUGIN_STARTED;
        /* 【关键】插件自己声明菜单项，框架负责挂到配置化菜单链上 */
        if (p->menu_id != 0) {
            menu_add(p->menu_id, p->menu_label, p);
        }
        ok++;
        cur = cur->next;
    }
    return ok;
}

int manager_stop_all(void)
{
    PluginNode* cur = g_head;
    int ok = 0;
    printf("\n--- 停止所有插件（摘掉菜单）---\n");
    while (cur != NULL) {
        Plugin* p = cur->plugin;
        if (p->state == PLUGIN_STARTED) {
            if (p->menu_id != 0) {
                menu_remove(p->menu_id);
            }
            if (p->stop != NULL && p->stop(p) == 0) {
                p->state = PLUGIN_STOPPED;
                ok++;
            }
        }
        cur = cur->next;
    }
    return ok;
}

void manager_cleanup_all(void)
{
    PluginNode* cur = g_head;
    printf("\n--- 清理所有插件 ---\n");
    while (cur != NULL) {
        Plugin* p = cur->plugin;
        if (p->cleanup != NULL) {
            p->cleanup(p);
        }
        p->state = PLUGIN_CLEANED;
        cur = cur->next;
    }
}

void manager_destroy(void)
{
    PluginNode* cur = g_head;
    int freed = 0;
    while (cur != NULL) {
        PluginNode* tmp = cur;
        cur = cur->next;
        free(tmp);
        freed++;
    }
    g_head = NULL;
    g_tail = NULL;
    g_count = 0;
    printf("  [管理器] 已释放 %d 个插件节点\n", freed);
}

int manager_execute(const char* name, double amount)
{
    Plugin* p = manager_find(name);
    if (p == NULL || p->execute == NULL) {
        printf("  [管理器] 找不到可执行的插件[%s]\n", name);
        return -1;
    }
    return p->execute(p, amount);
}

void manager_print_all(void)
{
    PluginNode* cur = g_head;
    int i = 1;
    printf("\n--- 已注册插件列表（共 %d 个）---\n", g_count);
    printf("  %-4s %-12s %-6s %-8s %s\n", "序号", "名称", "版本", "状态", "说明");
    printf("  ------------------------------------------------------------\n");
    while (cur != NULL) {
        Plugin* p = cur->plugin;
        printf("  %-4d %-12s %-6s %-8s %s\n",
               i++, p->name, p->version,
               plugin_state_name(p->state), p->description);
        cur = cur->next;
    }
    printf("  ------------------------------------------------------------\n");
}

/* ============================================================
 *  第二部分：配置化菜单实现
 * ============================================================ */

void menu_init(void)
{
    g_menu_head = NULL;
    g_menu_count = 0;
}

/* 按 id 升序有序插入（第8讲"有序插入"的直接应用） */
int menu_add(int id, const char* label, Plugin* plugin)
{
    MenuItem* node;
    MenuItem* cur;

    if (menu_find(id) != NULL) {
        printf("  [菜单] 编号 %d 已存在，跳过\n", id);
        return -1;
    }

    node = (MenuItem*)malloc(sizeof(MenuItem));
    if (node == NULL) {
        return -2;
    }
    node->id = id;
    snprintf(node->label, sizeof(node->label), "%s", label);
    node->plugin = plugin;
    node->next = NULL;

    /* 情况1：空链表，或新节点应排在最前 */
    if (g_menu_head == NULL || g_menu_head->id > id) {
        node->next = g_menu_head;
        g_menu_head = node;
        g_menu_count++;
        return 0;
    }

    /* 情况2：找到第一个 id 更大的节点，插在它前面 */
    cur = g_menu_head;
    while (cur->next != NULL && cur->next->id < id) {
        cur = cur->next;
    }
    node->next = cur->next;
    cur->next = node;
    g_menu_count++;
    return 0;
}

int menu_remove(int id)
{
    MenuItem* cur = g_menu_head;
    MenuItem* prev = NULL;

    while (cur != NULL) {
        if (cur->id == id) {
            if (prev == NULL) {
                g_menu_head = cur->next;
            } else {
                prev->next = cur->next;
            }
            free(cur);
            g_menu_count--;
            return 0;
        }
        prev = cur;
        cur = cur->next;
    }
    return -1;
}

MenuItem* menu_find(int id)
{
    MenuItem* cur = g_menu_head;
    while (cur != NULL) {
        if (cur->id == id) {
            return cur;
        }
        cur = cur->next;
    }
    return NULL;
}

void menu_show(void)
{
    MenuItem* cur = g_menu_head;
    printf("\n============ ATM 主菜单 ============\n");
    while (cur != NULL) {
        printf("  %d. %s\n", cur->id, cur->label);
        cur = cur->next;
    }
    printf("  0. 退出\n");
    printf("====================================\n");
}

int menu_count(void)
{
    return g_menu_count;
}

void menu_destroy(void)
{
    MenuItem* cur = g_menu_head;
    int freed = 0;
    while (cur != NULL) {
        MenuItem* tmp = cur;
        cur = cur->next;
        free(tmp);
        freed++;
    }
    g_menu_head = NULL;
    g_menu_count = 0;
    printf("  [菜单] 已释放 %d 个菜单项\n", freed);
}

/* ============================================================
 *  第三部分：动态加载 plugins/ 目录
 * ============================================================
 *  这是第11讲（运行时加载）+ 第12讲（插件发现）的工程化落地：
 *    扫描目录 → 逐个 LoadLibrary → 取 get_plugin 符号 → 拿到 Plugin*
 *  任何一步失败都只影响当前这个文件，打印原因后继续，
 *  绝不让一个坏插件拖垮整个框架——这就是"优雅降级"。
 */

/* 记录已加载的库，供 framework_stop 统一卸载 */
static void remember_lib(DllHandle h, const char* path)
{
    LoadedLib* node = (LoadedLib*)malloc(sizeof(LoadedLib));
    if (node == NULL) {
        return;
    }
    node->handle = h;
    snprintf(node->path, sizeof(node->path), "%s", path);
    node->next = g_libs;
    g_libs = node;
}

/* dll_scan_dir 的回调上下文 */
typedef struct ScanCtx {
    int loaded;      /* 成功加载插件数 */
    int failed;      /* 加载失败文件数 */
    int not_plugin;  /* 非插件 DLL 数 */
} ScanCtx;

static void on_plugin_file(const char* fullpath, void* user)
{
    ScanCtx* ctx = (ScanCtx*)user;
    char err[512] = {0};
    DllHandle h;
    PluginEntry entry;
    Plugin* p;

    printf("  [发现] %s\n", fullpath);

    /* 第 1 步：加载动态库（失败则优雅降级） */
    h = dll_load(fullpath, err, sizeof(err));
    if (h == NULL) {
        printf("  [降级] 加载失败，跳过该文件。原因: %s\n", err);
        ctx->failed++;
        return;
    }

    /* 第 2 步：查找约定的入口符号 get_plugin */
    entry = (PluginEntry)dll_symbol(h, PLUGIN_ENTRY_NAME);
    if (entry == NULL) {
        printf("  [降级] 未导出符号 \"%s\"，不是本框架的插件，跳过\n",
               PLUGIN_ENTRY_NAME);
        dll_unload(h);
        ctx->not_plugin++;
        return;
    }

    /* 第 3 步：取得插件实例并注册 */
    p = entry();
    if (p == NULL) {
        printf("  [降级] get_plugin() 返回空，跳过\n");
        dll_unload(h);
        ctx->failed++;
        return;
    }

    p->state = PLUGIN_LOADED;
    if (manager_register(p) == 0) {
        remember_lib(h, fullpath);   /* 注册成功才记住句柄，失败则立刻卸载 */
        ctx->loaded++;
    } else {
        dll_unload(h);
        ctx->failed++;
    }
}

static void framework_load_plugins_dir(const char* dir)
{
    ScanCtx ctx = {0, 0, 0};
    int files;

    printf("\n=== 扫描插件目录: %s ===\n", dir);
    files = dll_scan_dir(dir, dll_extension(), on_plugin_file, &ctx);

    if (files == 0) {
        printf("  [提示] 目录不存在或没有 *%s 文件。\n", dll_extension());
        printf("         → 这没关系，框架会使用内置插件继续运行。\n");
        return;
    }
    printf("  [结果] 扫描 %d 个文件：成功 %d，失败 %d，非插件 %d\n",
           files, ctx.loaded, ctx.failed, ctx.not_plugin);
}

/* ============================================================
 *  第四部分：框架入口
 * ============================================================ */

void framework_set_builtins(Plugin** builtins, int count)
{
    g_builtins = builtins;
    g_builtin_count = count;
}

/* 动态加载失败时的回退：同名插件已从 DLL 加载则跳过，否则用内置实现 */
static void framework_register_fallbacks(void)
{
    int i;
    if (g_builtins == NULL || g_builtin_count == 0) {
        return;
    }
    printf("\n=== 检查内置回退插件 ===\n");
    for (i = 0; i < g_builtin_count; i++) {
        Plugin* p = g_builtins[i];
        if (p == NULL) {
            continue;
        }
        if (manager_find(p->name) != NULL) {
            printf("  [OK]   [%s] 已由动态库提供，不使用内置实现\n", p->name);
            continue;
        }
        printf("  [降级] [%s] 未从 plugins/ 加载到，启用内置实现\n", p->name);
        p->state = PLUGIN_LOADED;
        manager_register(p);
    }
}

void framework_start(void)
{
    printf("==================================================\n");
    printf("  第14讲：完整项目与总结展望\n");
    printf("  ATM 可插拔插件框架 —— 完整工程演示\n");
    printf("==================================================\n");

    manager_init();
    menu_init();

    printf("\n=== 初始化账务核心 ===\n");
    account_init_demo();

    /* 内置菜单项：不属于任何插件，用 plugin=NULL 表示 */
    menu_add(9, "插件列表", NULL);

    /* 路径一：从 plugins/ 目录动态加载 DLL */
    framework_load_plugins_dir("plugins");

    /* 路径二：内置插件直接注册（作为动态加载失败的回退） */
    framework_register_fallbacks();

    printf("\n=== 插件总览 ===\n");
    printf("  当前共注册 %d 个插件\n", manager_count());

    /* 生命周期：init_all → start_all */
    manager_init_all();
    manager_start_all();

    printf("\n=== 框架启动完成，菜单项 %d 个 ===\n", menu_count());
}

int framework_run(void)
{
    char line[64];

    /* 交互循环：所有业务操作都通过"菜单 → 插件接口"分发 */
    while (1) {
        int choice;
        MenuItem* item;
        Plugin* p;
        double amount = 0.0;

        menu_show();
        printf("请选择操作: ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            printf("\n[输入结束]\n");
            break;   /* stdin 关闭（例如管道输入用完）视为退出 */
        }
        choice = atoi(line);

        if (choice == 0) {
            printf("\n[收到退出指令]\n");
            break;
        }

        item = menu_find(choice);
        if (item == NULL) {
            printf("  [错误] 无效的菜单编号: %d\n", choice);
            continue;
        }

        /* 内置菜单项（如"插件列表"）：plugin 为 NULL */
        if (item->plugin == NULL) {
            manager_print_all();
            continue;
        }

        p = item->plugin;
        if (p->state != PLUGIN_STARTED) {
            printf("  [错误] 插件[%s] 当前状态为 %s，无法执行\n",
                   p->name, plugin_state_name(p->state));
            continue;
        }

        /* 是否需要框架先读金额，由插件自己声明（need_amount） */
        if (p->need_amount) {
            printf("请输入金额: ");
            if (fgets(line, sizeof(line), stdin) == NULL) {
                break;
            }
            amount = atof(line);
        }

        p->execute(p, amount);   /* 多态调用：同一行代码，不同插件不同行为 */
    }
    return 0;
}

void framework_stop(void)
{
    printf("\n=== 开始关闭框架 ===\n");

    /* 生命周期收尾：stop_all → cleanup_all */
    manager_stop_all();
    manager_cleanup_all();

    /* 释放账务模块与流水链表（谁分配谁释放） */
    printf("\n--- 释放账务资源 ---\n");
    transaction_destroy();

    manager_destroy();
    menu_destroy();

    /* 卸载所有加载过的动态库 */
    printf("\n--- 卸载动态库 ---\n");
    {
        LoadedLib* cur = g_libs;
        int n = 0;
        while (cur != NULL) {
            LoadedLib* tmp = cur;
            printf("  [卸载] %s\n", cur->path);
            dll_unload(cur->handle);
            cur = cur->next;
            free(tmp);
            n++;
        }
        g_libs = NULL;
        if (n == 0) {
            printf("  没有需要卸载的动态库\n");
        }
    }

    printf("\n=== 框架已安全关闭，再见！===\n");
}
