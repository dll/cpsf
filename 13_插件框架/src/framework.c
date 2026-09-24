/*
 * ============================================================
 *  第13讲：插件框架架构
 *  framework.c —— 插件框架核心实现
 * ============================================================
 *
 *  【本文件实现 framework.h 中的全部接口】
 *
 *  三个关键点：
 *    1. 生命周期状态机
 *       UNLOADED → LOADED → INITIALIZED → STARTED → STOPPED
 *                → CLEANED → UNLOADED（销毁时回到起点）
 *       管理器严格按状态放行，状态不对就拒绝并打印原因。
 *
 *    2. 两条链表
 *       插件链表：PluginNode（管理插件生命周期）
 *       菜单链表：MenuItem  （管理用户看到的菜单）
 *       注册插件 = 挂插件节点 + 挂菜单项（尾部插入，保持顺序）
 *
 *    3. 控制反转（IoC）
 *       main() 从头到尾没有出现过"存款/取款"这些字眼，
 *       是框架在合适的时机回调插件的函数。
 *       库是你调用它；框架是它调用你。
 *
 *  编译运行：
 *    gcc -Wall -o plugin_framework framework.c && ./plugin_framework
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "framework.h"      /* 接口契约（不允许改动语义） */
#include "plugins.h"        /* 内置插件工厂函数 */
#include "atm_state.h"      /* ATM 共享业务状态 */

/* ============================================================
 *  全局状态：插件链表 + 菜单链表
 * ============================================================
 *  与第8讲、第12讲一样：链表的"头指针"是模块级 static 变量，
 *  外部只能通过函数操作它，保证链表不会被随意破坏。
 */

static PluginNode* g_plugin_head = NULL;    /* 插件链表头 */
static PluginNode* g_plugin_tail = NULL;    /* 插件链表尾（尾部插入 O(1)） */
static int         g_plugin_count = 0;      /* 已注册插件数量 */

static MenuItem*   g_menu_head = NULL;      /* 菜单链表头 */
static int         g_menu_count = 0;        /* 菜单项数量 */

/* ============================================================
 *  内部工具函数
 * ============================================================
 */

/* 状态枚举 → 可读字符串（打印错误原因时要说明"当前状态是什么"） */
static const char* state_name(PluginState s)
{
    switch (s) {
        case PLUGIN_UNLOADED:    return "UNLOADED";
        case PLUGIN_LOADED:      return "LOADED";
        case PLUGIN_INITIALIZED: return "INITIALIZED";
        case PLUGIN_STARTED:     return "STARTED";
        case PLUGIN_STOPPED:     return "STOPPED";
        case PLUGIN_CLEANED:     return "CLEANED";
        default:                 return "UNKNOWN";
    }
}

/* ============================================================
 *  第三部分实现：插件管理器
 * ============================================================
 */

/* 初始化管理器 */
void manager_init(void)
{
    g_plugin_head  = NULL;
    g_plugin_tail  = NULL;
    g_plugin_count = 0;
    printf("=== 插件管理器已初始化（插件链表为空）===\n");
}

/*
 * 注册插件到管理器
 *   成功：节点挂到链表尾部，状态 UNLOADED → LOADED，
 *         若插件定义了 menu_id 则自动挂载菜单项，返回 0
 *   失败：返回负值并打印原因（空指针 / 重复注册 / 内存不足）
 */
int manager_register(Plugin* p)
{
    PluginNode* node;

    /* --- 校验 1：空插件 --- */
    if (p == NULL) {
        printf("[注册失败] 插件指针为空，拒绝注册\n");
        return -1;
    }

    /* --- 校验 2：必须实现核心接口 --- */
    if (p->execute == NULL) {
        printf("[注册失败] 插件[%s] 没有实现 execute()，不是合法插件\n", p->name);
        return -1;
    }

    /* --- 校验 3：重名检查（重复注册必须被拒绝） --- */
    {
        PluginNode* cur = g_plugin_head;
        while (cur != NULL) {
            if (strcmp(cur->plugin->name, p->name) == 0) {
                printf("[注册失败] 插件[%s] 已存在，拒绝重复注册\n", p->name);
                return -1;
            }
            cur = cur->next;
        }
    }

    /* --- 分配节点（衔接第5讲堆内存、第8讲链表） --- */
    node = (PluginNode*)malloc(sizeof(PluginNode));
    if (node == NULL) {
        printf("[注册失败] 内存分配失败，无法注册插件[%s]\n", p->name);
        return -1;
    }
    node->plugin = p;
    node->next   = NULL;

    /* --- 尾部插入：保持注册顺序，与菜单显示顺序一致 --- */
    if (g_plugin_tail == NULL) {
        g_plugin_head = node;
        g_plugin_tail = node;
    } else {
        g_plugin_tail->next = node;
        g_plugin_tail = node;
    }
    g_plugin_count++;

    /* --- 状态流转：UNLOADED → LOADED --- */
    p->state = PLUGIN_LOADED;

    printf("[注册] %s v%s - %s  (状态: %s)\n",
           p->name, p->version, p->description, state_name(p->state));

    /* --- 配置化菜单：注册即挂载（插件不需要自己写菜单代码） --- */
    if (p->menu_id != 0) {
        if (menu_add(p->menu_id, p->menu_label, p) != 0) {
            printf("        └─ 菜单项挂载失败：编号 %d 可能已被占用\n", p->menu_id);
        }
    }

    return 0;
}

/*
 * 初始化所有已注册插件
 *   仅允许 LOADED → INITIALIZED，其它状态跳过并打印原因
 *   返回成功初始化的插件数量
 */
int manager_init_all(void)
{
    int ok = 0;
    int skip = 0;
    PluginNode* cur;

    printf("\n--- 批量初始化 init_all() ---\n");

    cur = g_plugin_head;
    while (cur != NULL) {
        Plugin* p = cur->plugin;

        if (p->state != PLUGIN_LOADED) {
            printf("  [%-6s] 跳过：当前状态 %s，不允许 init\n",
                   p->name, state_name(p->state));
            skip++;
        } else if (p->init == NULL) {
            /* 没有 init 的插件视为"无需初始化"，直接放行 */
            p->state = PLUGIN_INITIALIZED;
            printf("  [%-6s] 未实现 init，直接进入 INITIALIZED\n", p->name);
            ok++;
        } else if (p->init(p) == 0) {
            p->state = PLUGIN_INITIALIZED;      /* LOADED → INITIALIZED */
            ok++;
        } else {
            printf("  [%-6s] init 失败，保持 LOADED（不会被启动）\n", p->name);
        }
        cur = cur->next;
    }

    printf("--- init_all 完成：成功 %d 个，跳过 %d 个 ---\n", ok, skip);
    return ok;
}

/*
 * 启动所有插件
 *   仅允许 INITIALIZED → STARTED
 *   返回成功启动的插件数量
 */
int manager_start_all(void)
{
    int ok = 0;
    PluginNode* cur;

    printf("\n--- 批量启动 start_all() ---\n");

    cur = g_plugin_head;
    while (cur != NULL) {
        Plugin* p = cur->plugin;

        if (p->state != PLUGIN_INITIALIZED) {
            printf("  [%-6s] 跳过：当前状态 %s，不允许 start\n",
                   p->name, state_name(p->state));
        } else if (p->start == NULL) {
            p->state = PLUGIN_STARTED;          /* 无 start 视为立即可用 */
            printf("  [%-6s] 未实现 start，直接进入 STARTED\n", p->name);
            ok++;
        } else if (p->start(p) == 0) {
            p->state = PLUGIN_STARTED;          /* INITIALIZED → STARTED */
            ok++;
        } else {
            printf("  [%-6s] start 失败，保持 INITIALIZED\n", p->name);
        }
        cur = cur->next;
    }

    printf("--- start_all 完成：启动 %d 个插件 ---\n", ok);
    return ok;
}

/*
 * 停止所有插件
 *   仅允许 STARTED → STOPPED
 *   返回成功停止的插件数量
 */
int manager_stop_all(void)
{
    int ok = 0;
    PluginNode* cur;

    printf("\n--- 批量停止 stop_all() ---\n");

    cur = g_plugin_head;
    while (cur != NULL) {
        Plugin* p = cur->plugin;

        if (p->state == PLUGIN_STARTED) {
            if (p->stop != NULL) {
                p->stop(p);
            }
            p->state = PLUGIN_STOPPED;          /* STARTED → STOPPED */
            ok++;
        } else {
            printf("  [%-6s] 跳过：当前状态 %s，无需 stop\n",
                   p->name, state_name(p->state));
        }
        cur = cur->next;
    }

    printf("--- stop_all 完成：停止 %d 个插件 ---\n", ok);
    return ok;
}

/*
 * 清理所有插件
 *   任何"非 CLEANED/UNLOADED"的状态都会执行 cleanup，
 *   保证不会因为状态异常而漏掉资源释放。
 *   流转：STARTED/STOPPED/INITIALIZED/LOADED → CLEANED
 */
void manager_cleanup_all(void)
{
    PluginNode* cur;

    printf("\n--- 批量清理 cleanup_all() ---\n");

    cur = g_plugin_head;
    while (cur != NULL) {
        Plugin* p = cur->plugin;

        if (p->state == PLUGIN_CLEANED || p->state == PLUGIN_UNLOADED) {
            printf("  [%-6s] 跳过：当前状态 %s，已清理\n",
                   p->name, state_name(p->state));
        } else {
            if (p->state == PLUGIN_STARTED) {
                printf("  [%-6s] 警告：仍在运行（未 stop），一并清理\n", p->name);
            }
            if (p->cleanup != NULL) {
                p->cleanup(p);
            }
            p->state = PLUGIN_CLEANED;          /* → CLEANED */
        }
        cur = cur->next;
    }

    printf("--- cleanup_all 完成 ---\n");
}

/*
 * 销毁管理器：释放插件链表
 *   销毁前把每个插件的状态复位为 UNLOADED，
 *   完成 CLEANED → UNLOADED 的最后一步，形成闭环。
 */
void manager_destroy(void)
{
    PluginNode* cur = g_plugin_head;
    int released = 0;

    while (cur != NULL) {
        PluginNode* next = cur->next;           /* 先存下一个，再 free 当前 */
        cur->plugin->state = PLUGIN_UNLOADED;   /* CLEANED → UNLOADED */
        free(cur);
        cur = next;
        released++;
    }

    g_plugin_head  = NULL;
    g_plugin_tail  = NULL;
    g_plugin_count = 0;

    printf("\n=== 插件管理器已销毁（释放 %d 个节点，状态回到 UNLOADED）===\n",
           released);
}

/* 按名称查找插件，找不到返回 NULL */
Plugin* manager_find(const char* name)
{
    PluginNode* cur;

    if (name == NULL) {
        return NULL;
    }

    cur = g_plugin_head;
    while (cur != NULL) {
        if (strcmp(cur->plugin->name, name) == 0) {
            return cur->plugin;
        }
        cur = cur->next;
    }
    return NULL;
}

/*
 * 执行指定插件
 *   状态必须是 STARTED —— 没启动的插件不允许处理业务请求
 *   返回插件 execute 的返回值，失败返回负值
 */
int manager_execute(const char* name, double amount)
{
    Plugin* p = manager_find(name);

    if (p == NULL) {
        printf("  [执行失败] 未找到名为[%s]的插件\n", name);
        return -1;
    }
    if (p->state != PLUGIN_STARTED) {
        printf("  [执行失败] 插件[%s] 当前状态 %s，未启动不可执行\n",
               p->name, state_name(p->state));
        return -2;
    }
    if (p->execute == NULL) {
        printf("  [执行失败] 插件[%s] 未实现 execute()\n", p->name);
        return -3;
    }
    return p->execute(p, amount);
}

/* 获取插件数量 */
int manager_count(void)
{
    return g_plugin_count;
}

/* 打印所有插件及状态 */
void manager_print_all(void)
{
    PluginNode* cur;
    int i = 1;

    printf("\n--- 插件列表（共 %d 个）---\n", g_plugin_count);
    printf("  %-4s %-10s %-8s %-14s %s\n",
           "序号", "插件名", "版本", "状态", "描述");

    cur = g_plugin_head;
    while (cur != NULL) {
        Plugin* p = cur->plugin;
        printf("  %-4d %-10s %-8s %-14s %s\n",
               i++, p->name, p->version, state_name(p->state), p->description);
        cur = cur->next;
    }

    if (g_plugin_count == 0) {
        printf("  （空）\n");
    }
}

/* ============================================================
 *  第四部分实现：配置化菜单（链表）
 * ============================================================
 *
 *  【和第2讲的硬编码菜单对比】
 *    第2讲：
 *      printf("1. 存款\n");
 *      printf("2. 取款\n");
 *      switch (choice) {
 *        case 1: deposit();  break;
 *        case 2: withdraw(); break;
 *      }
 *    加一个功能 → 改三处 → 违背开闭原则。
 *
 *    现在：菜单 = 链表
 *      menu_show()   遍历链表打印
 *      menu_add()    尾部插入
 *      menu_remove() 摘除节点
 *      menu_handle() 查表 → 直接调用插件的 execute
 *    加一个功能 → 零改动（只要插件带上 menu_id/menu_label）
 */

/* 菜单初始化 */
void menu_init(void)
{
    g_menu_head  = NULL;
    g_menu_count = 0;
    printf("=== 配置化菜单已初始化（菜单链表为空）===\n");
}

/*
 * 添加菜单项（尾部插入，保持顺序）
 *   成功返回 0；编号重复 / 参数非法 / 内存不足返回 -1
 */
int menu_add(int id, const char* label, Plugin* plugin)
{
    MenuItem* item;
    MenuItem* cur;

    if (id == 0) {
        printf("  [菜单] 插件[%s] 的 menu_id 为 0（无菜单项），跳过挂载\n",
               (plugin != NULL) ? plugin->name : "?");
        return -1;
    }
    if (label == NULL) {
        printf("  [菜单] 菜单文字为空，拒绝挂载\n");
        return -1;
    }

    /* 查重：菜单编号必须唯一 */
    cur = g_menu_head;
    while (cur != NULL) {
        if (cur->id == id) {
            printf("  [菜单] 编号 %d 已被[%s]占用，拒绝挂载[%s]\n",
                   id, cur->label, label);
            return -1;
        }
        cur = cur->next;
    }

    item = (MenuItem*)malloc(sizeof(MenuItem));
    if (item == NULL) {
        printf("  [菜单] 内存分配失败\n");
        return -1;
    }
    item->id     = id;
    item->plugin = plugin;
    item->next   = NULL;
    snprintf(item->label, sizeof(item->label), "%s", label);

    /* 尾部插入：菜单顺序 = 插件注册顺序 */
    if (g_menu_head == NULL) {
        g_menu_head = item;
    } else {
        cur = g_menu_head;
        while (cur->next != NULL) {
            cur = cur->next;
        }
        cur->next = item;
    }
    g_menu_count++;

    printf("        └─ 菜单项已挂载： %d. %s\n", id, label);
    return 0;
}

/*
 * 删除菜单项（按ID）
 *   成功返回 0，未找到返回 -1
 *   —— "卸载即摘菜单"，主程序同样不需要改代码
 */
int menu_remove(int id)
{
    MenuItem* cur  = g_menu_head;
    MenuItem* prev = NULL;

    while (cur != NULL) {
        if (cur->id == id) {
            if (prev == NULL) {
                g_menu_head = cur->next;        /* 摘的是头节点 */
            } else {
                prev->next = cur->next;         /* 跳过当前节点 */
            }
            printf("  [菜单] 已摘除菜单项： %d. %s\n", cur->id, cur->label);
            free(cur);
            g_menu_count--;
            return 0;
        }
        prev = cur;
        cur = cur->next;
    }

    printf("  [菜单] 未找到编号 %d 的菜单项\n", id);
    return -1;
}

/* 显示菜单（遍历链表打印） */
void menu_show(void)
{
    MenuItem* cur = g_menu_head;

    printf("\n========== ATM 主菜单（共 %d 项，全部来自插件）==========\n",
           g_menu_count);

    if (cur == NULL) {
        printf("  （暂无插件提供功能）\n");
    }
    while (cur != NULL) {
        printf("  %d. %s\n", cur->id, cur->label);
        cur = cur->next;
    }

    /* "0. 退出"是框架自身的固定项，不属于任何插件 */
    printf("  0. 退出\n");
    printf("=======================================================\n");
}

/*
 * 处理用户选择
 *   注意：这里没有 switch！没有 if (choice == 1) ... ！
 *   "编号 → 插件"的映射完全由菜单链表给出，
 *   查表得到插件后直接调用它的 execute()——查表 + 多态。
 */
int menu_handle(int choice, double amount)
{
    MenuItem* cur = g_menu_head;

    while (cur != NULL) {
        if (cur->id == choice) {
            if (cur->plugin == NULL) {
                printf("  [菜单] 编号 %d 未关联插件，无法执行\n", choice);
                return -1;
            }
            return manager_execute(cur->plugin->name, amount);
        }
        cur = cur->next;
    }

    printf("  [菜单] 无效选择：没有编号 %d 的功能\n", choice);
    return -1;
}

/* 销毁菜单：释放所有菜单项节点 */
void menu_destroy(void)
{
    MenuItem* cur = g_menu_head;
    int released = 0;

    while (cur != NULL) {
        MenuItem* next = cur->next;
        free(cur);
        cur = next;
        released++;
    }

    g_menu_head  = NULL;
    g_menu_count = 0;

    printf("=== 菜单已销毁（释放 %d 个菜单项节点）===\n", released);
}

/* ============================================================
 *  第五部分实现：框架入口
 * ============================================================
 */

/*
 * 框架启动：一键完成
 *   manager_init → menu_init → 注册内置插件 → init_all → start_all
 *   返回 0 表示成功
 */
int framework_start(void)
{
    printf("============================================\n");
    printf("  第13讲：插件框架架构\n");
    printf("  ATM 插件框架 —— 生命周期 · 管理器 · 配置化菜单\n");
    printf("============================================\n\n");

    /* 1. 初始化两条链表 */
    manager_init();
    menu_init();

    /* 2. 注册内置插件
     *    注意：这里只写"注册谁"，不写"菜单长什么样"，
     *    菜单项随注册自动挂载到菜单链表上。 */
    printf("\n--- 注册内置插件（注册即挂载菜单项）---\n");
    if (manager_register(create_deposit_plugin())  != 0) return -1;
    if (manager_register(create_withdraw_plugin()) != 0) return -1;
    if (manager_register(create_query_plugin())    != 0) return -1;
    if (manager_register(create_transfer_plugin()) != 0) return -1;

    manager_print_all();

    /* 3. 批量初始化 + 批量启动 */
    if (manager_init_all() == 0) {
        printf("\n[框架] 没有任何插件初始化成功，启动中止\n");
        return -1;
    }
    manager_start_all();

    /* 4. 展示启动后的状态 */
    manager_print_all();

    /* 5. 菜单已经"长"出来了，全程没有一行硬编码菜单文字 */
    menu_show();

    return 0;
}

/*
 * 框架运行：显示菜单 + 交互循环
 *   输入流程：功能编号 → 金额（查询类输入 0）→ 回车
 *   输入 0 退出；输入流结束（如管道 EOF）也会安全退出
 */
int framework_run(void)
{
    int    choice = 0;
    double amount = 0.0;

    printf("\n[框架] 进入交互模式（输入 0 退出）\n");

    for (;;) {
        menu_show();

        printf("请选择功能编号: ");
        if (scanf("%d", &choice) != 1) {
            printf("\n[框架] 输入流已结束，自动退出\n");
            break;
        }
        if (choice == 0) {
            printf("\n[框架] 收到退出指令\n");
            break;
        }

        printf("请输入金额（查询类请输入 0）: ");
        if (scanf("%lf", &amount) != 1) {
            printf("\n[框架] 输入流已结束，自动退出\n");
            break;
        }

        /* 关键：不判断 choice 是 1 还是 2，交给菜单链表去查 */
        menu_handle(choice, amount);
    }

    return 0;
}

/*
 * 框架停止：一键完成
 *   stop_all → cleanup_all → menu_destroy → manager_destroy
 */
void framework_stop(void)
{
    printf("\n[框架] 开始安全关闭...\n");

    manager_stop_all();     /* STARTED → STOPPED */
    manager_cleanup_all();  /* STOPPED → CLEANED */
    menu_destroy();         /* 释放菜单链表 */
    manager_destroy();      /* CLEANED → UNLOADED，释放插件链表 */

    printf("\n=== 框架已安全关闭 ===\n");
}
