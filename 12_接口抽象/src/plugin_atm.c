/*
 * ============================================================
 *  第12讲：接口抽象与插件发现
 *  plugin_atm.c —— ATM 插件接口化版本
 * ============================================================
 *
 *  目标：从"运行时加载"进化到"接口抽象"
 *
 *  第11讲的成果：
 *    学会了 dlopen/dlsym 运行时加载动态库
 *    但——每个插件的函数名不同，调用方式不同，耦合度高
 *
 *  第12讲的进步：
 *    1. 定义统一的 Plugin 接口结构体（init/execute/cleanup）
 *    2. 用链表管理已注册的插件（衔接第8讲链表）
 *    3. 实现插件注册机制（register → 链表插入）
 *    4. 实现目录扫描自动发现插件
 *    5. 通过统一接口调用不同插件 = 多态！
 *
 *  核心思想：
 *    "不管你是什么插件，只要你实现了 Plugin 接口，
 *     我就能统一加载、统一调用、统一清理"
 *    —— 这就是 C语言的面向对象设计
 *
 *  编译运行：
 *    gcc -Wall -o plugin_atm plugin_atm.c && ./plugin_atm
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>     /* malloc / free */
#include <string.h>     /* strcpy / strcmp */
#include "plugin.h"     /* 插件接口定义 */

/* ============================================================
 *  目录扫描支持（跨平台）
 * ============================================================
 *  Windows: 使用 FindFirstFile / FindNextFile
 *  Linux/Mac: 使用 dirent.h 的 opendir / readdir
 *
 *  这部分代码演示了如何扫描 plugins/ 目录，
 *  发现 .dll(Windows) 或 .so(Linux) 插件文件
 */
#ifdef _WIN32
    #include <windows.h>
    #define PLUGIN_EXT ".dll"
    #define DIR_SEP "\\"
#else
    #include <dirent.h>
    #define PLUGIN_EXT ".so"
    #define DIR_SEP "/"
#endif

/* ============================================================
 *  全局变量 —— 插件链表头指针
 * ============================================================
 *
 *  【对比第8讲】
 *    第8讲：TransactionNode* trans_head;  // 交易记录链表
 *    现在：PluginNode* plugin_head;       // 插件链表
 *    数据结构完全一样，但管理的对象从"数据"变成了"接口"
 */
static PluginNode* plugin_head = NULL;
static int plugin_total = 0;  /* 已注册插件计数 */

/* ============================================================
 *  第一部分：内置插件实现
 * ============================================================
 *
 *  三个内置 ATM 插件：存款、取款、查询余额
 *  每个插件都实现 Plugin 接口的三个方法：
 *    init() → 初始化（设置初始状态）
 *    execute() → 执行核心功能
 *    cleanup() → 清理资源
 *
 *  【关键】这三个插件虽然功能不同，但接口统一！
 *  调用方不需要知道每个插件的具体实现，只需通过接口调用。
 *
 *  这就是多态：不同插件，同一接口，统一调用
 */

/* 全局余额（ATM系统的共享状态） */
static double g_balance = 10000.0;

/* ---- 存款插件 ---- */

/* 存款 init：打印欢迎信息 */
static int deposit_init(Plugin* self)
{
    printf("  [%s] 初始化完成 v%s\n", self->name, self->version);
    return 0;  /* 返回0表示成功 */
}

/* 存款 execute：执行存款操作 */
static int deposit_execute(Plugin* self, double amount)
{
    if (amount <= 0) {
        printf("  [%s] 错误：存款金额必须大于0\n", self->name);
        return -1;
    }
    g_balance += amount;
    printf("  [%s] 存入 %.2f 元，余额: %.2f 元\n",
           self->name, amount, g_balance);
    return 0;
}

/* 存款 cleanup：清理（无额外资源需要释放） */
static void deposit_cleanup(Plugin* self)
{
    printf("  [%s] 已清理\n", self->name);
}

/* 存款插件实例（实现了Plugin接口） */
static Plugin deposit_plugin = {
    .name        = "存款",
    .version     = "1.0",
    .description = "向账户存入现金",
    .init        = deposit_init,
    .execute     = deposit_execute,
    .cleanup     = deposit_cleanup,
};

/* ---- 取款插件 ---- */

static int withdraw_init(Plugin* self)
{
    printf("  [%s] 初始化完成 v%s\n", self->name, self->version);
    return 0;
}

static int withdraw_execute(Plugin* self, double amount)
{
    if (amount <= 0) {
        printf("  [%s] 错误：取款金额必须大于0\n", self->name);
        return -1;
    }
    if (amount > g_balance) {
        printf("  [%s] 错误：余额不足！当前余额: %.2f\n",
               self->name, g_balance);
        return -2;
    }
    g_balance -= amount;
    printf("  [%s] 取出 %.2f 元，余额: %.2f 元\n",
           self->name, amount, g_balance);
    return 0;
}

static void withdraw_cleanup(Plugin* self)
{
    printf("  [%s] 已清理\n", self->name);
}

static Plugin withdraw_plugin = {
    .name        = "取款",
    .version     = "1.0",
    .description = "从账户取出现金",
    .init        = withdraw_init,
    .execute     = withdraw_execute,
    .cleanup     = withdraw_cleanup,
};

/* ---- 查询余额插件 ---- */

static int query_init(Plugin* self)
{
    printf("  [%s] 初始化完成 v%s\n", self->name, self->version);
    return 0;
}

static int query_execute(Plugin* self, double amount)
{
    (void)amount;  /* 查询不需要金额参数 */
    printf("  [%s] 当前余额: %.2f 元\n", self->name, g_balance);
    return 0;
}

static void query_cleanup(Plugin* self)
{
    printf("  [%s] 已清理\n", self->name);
}

static Plugin query_plugin = {
    .name        = "查询余额",
    .version     = "1.0",
    .description = "查询账户当前余额",
    .init        = query_init,
    .execute     = query_execute,
    .cleanup     = query_cleanup,
};

/* ============================================================
 *  第二部分：插件管理器（链表操作）
 * ============================================================
 *
 *  【衔接第8讲链表】以下操作和第8讲的链表操作完全一样：
 *    注册   = 头部插入（O(1)）
 *    查找   = 遍历比较
 *    销毁   = 遍历free
 *  区别只是节点内容从 TransactionNode 变成了 PluginNode
 */

/* 初始化插件管理器 */
void plugin_manager_init(void)
{
    plugin_head = NULL;
    plugin_total = 0;
    printf("=== 插件管理器已初始化 ===\n\n");
}

/* 注册插件到链表（头部插入，O(1)） */
int plugin_register(Plugin* p)
{
    if (p == NULL) {
        printf("错误：无法注册空插件\n");
        return -1;
    }

    /* 检查是否已注册（避免重复） */
    PluginNode* cur = plugin_head;
    while (cur != NULL) {
        if (strcmp(cur->plugin->name, p->name) == 0) {
            printf("警告：插件[%s]已注册，跳过\n", p->name);
            return -2;
        }
        cur = cur->next;
    }

    /* 创建新节点（malloc分配，衔接第5讲堆内存） */
    PluginNode* node = (PluginNode*)malloc(sizeof(PluginNode));
    if (node == NULL) {
        printf("错误：内存分配失败\n");
        return -3;
    }

    node->plugin = p;

    /* 头部插入：新节点指向旧头，头指针指向新节点 */
    node->next = plugin_head;
    plugin_head = node;
    plugin_total++;

    printf("[注册] 插件[%s] v%s - %s\n",
           p->name, p->version, p->description);
    return 0;
}

/* 按名称查找插件（遍历链表，O(n)） */
Plugin* plugin_find(const char* name)
{
    PluginNode* cur = plugin_head;
    while (cur != NULL) {
        if (strcmp(cur->plugin->name, name) == 0) {
            return cur->plugin;  /* 找到了 */
        }
        cur = cur->next;
    }
    return NULL;  /* 没找到 */
}

/* 执行所有插件的 init() —— 遍历链表统一调用 */
void plugin_init_all(void)
{
    printf("\n--- 初始化所有插件 ---\n");
    PluginNode* cur = plugin_head;
    while (cur != NULL) {
        if (cur->plugin->init != NULL) {
            cur->plugin->init(cur->plugin);  /* 多态调用！ */
        }
        cur = cur->next;
    }
}

/* 执行所有插件的 execute() —— 多态的威力 */
void plugin_execute_all(double amount)
{
    printf("\n--- 执行所有插件 (金额=%.2f) ---\n", amount);
    PluginNode* cur = plugin_head;
    while (cur != NULL) {
        if (cur->plugin->execute != NULL) {
            cur->plugin->execute(cur->plugin, amount);  /* 统一调用 */
        }
        cur = cur->next;
    }
}

/* 执行所有插件的 cleanup() */
void plugin_cleanup_all(void)
{
    printf("\n--- 清理所有插件 ---\n");
    PluginNode* cur = plugin_head;
    while (cur != NULL) {
        if (cur->plugin->cleanup != NULL) {
            cur->plugin->cleanup(cur->plugin);
        }
        cur = cur->next;
    }
}

/* 销毁插件管理器（释放链表，衔接第8讲 destroy） */
void plugin_manager_destroy(void)
{
    PluginNode* cur = plugin_head;
    while (cur != NULL) {
        PluginNode* tmp = cur;    /* 先保存当前节点 */
        cur = cur->next;          /* 移到下一个 */
        free(tmp);                /* 再释放当前的 */
    }
    plugin_head = NULL;
    plugin_total = 0;
    printf("\n=== 插件管理器已销毁（释放 %d 个节点）===\n", plugin_total);
}

/* 打印已注册的插件列表 */
void plugin_list_print(void)
{
    printf("\n--- 已注册插件列表 (%d个) ---\n", plugin_total);
    PluginNode* cur = plugin_head;
    int i = 1;
    while (cur != NULL) {
        printf("  %d. %s v%s - %s\n",
               i++, cur->plugin->name,
               cur->plugin->version,
               cur->plugin->description);
        cur = cur->next;
    }
}

/* 获取已注册插件数量 */
int plugin_count(void)
{
    return plugin_total;
}

/* ============================================================
 *  第三部分：目录扫描自动发现插件
 * ============================================================
 *
 *  【核心思想】
 *    不需要手动注册每个插件！
 *    扫描 plugins/ 目录，发现 .dll/.so 文件，
 *    自动加载并注册——这就是"插件自动发现"
 *
 *  【实际应用】
 *    VS Code、Eclipse、Photoshop 都是这样发现插件的
 *    扫描固定目录 → 发现插件文件 → 加载 → 注册
 *
 *  【本讲演示】
 *    由于内置插件不是真正的动态库文件，
 *    这里模拟目录扫描过程，展示发现和注册的逻辑。
 *    真正的 dlopen 加载在第11讲已讲过，第14讲会整合。
 */

/* 模拟从动态库中加载插件（简化版） */
static Plugin* load_plugin_from_file(const char* filepath)
{
    /*
     * 实际流程（第11讲已学 dlopen/dlsym）：
     *   1. void* handle = dlopen(filepath, RTLD_LAZY);
     *   2. Plugin* (*get_plugin)() = dlsym(handle, "get_plugin");
     *   3. Plugin* p = get_plugin();
     *   4. return p;
     *
     * 本讲简化：根据文件名匹配内置插件
     */
    if (strstr(filepath, "deposit") != NULL) {
        return &deposit_plugin;
    }
    if (strstr(filepath, "withdraw") != NULL) {
        return &withdraw_plugin;
    }
    if (strstr(filepath, "query") != NULL) {
        return &query_plugin;
    }
    return NULL;  /* 无法识别的插件 */
}

/* 扫描目录自动发现并加载插件 */
int plugin_scan_directory(const char* dir_path)
{
    int found = 0;
    printf("\n=== 扫描插件目录: %s ===\n", dir_path);

#ifdef _WIN32
    /* Windows: 使用 FindFirstFile / FindNextFile */
    char search_path[256];
    WIN32_FIND_DATA find_data;
    HANDLE h_find;

    /* 构造搜索路径: dir_path\*.dll */
    snprintf(search_path, sizeof(search_path), "%s\\*%s", dir_path, PLUGIN_EXT);

    h_find = FindFirstFile(search_path, &find_data);
    if (h_find == INVALID_HANDLE_VALUE) {
        printf("  目录不存在或无插件文件，跳过自动发现\n");
        /* 没有实际目录也没关系，我们用模拟插件演示 */
        return 0;
    }

    do {
        /* 跳过 . 和 .. */
        if (find_data.cFileName[0] == '.') continue;

        char filepath[512];
        snprintf(filepath, sizeof(filepath), "%s\\%s", dir_path, find_data.cFileName);
        printf("  发现插件文件: %s\n", find_data.cFileName);

        Plugin* p = load_plugin_from_file(filepath);
        if (p != NULL) {
            plugin_register(p);
            found++;
        }
    } while (FindNextFile(h_find, &find_data));

    FindClose(h_find);

#else
    /* Linux/Mac: 使用 opendir / readdir */
    DIR* dir = opendir(dir_path);
    if (dir == NULL) {
        printf("  目录不存在或无法打开，跳过自动发现\n");
        return 0;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != NULL) {
        /* 跳过 . 和 .. */
        if (entry->d_name[0] == '.') continue;

        /* 检查是否是 .so 文件 */
        if (strstr(entry->d_name, PLUGIN_EXT) == NULL) continue;

        char filepath[512];
        snprintf(filepath, sizeof(filepath), "%s/%s", dir_path, entry->d_name);
        printf("  发现插件文件: %s\n", entry->d_name);

        Plugin* p = load_plugin_from_file(filepath);
        if (p != NULL) {
            plugin_register(p);
            found++;
        }
    }
    closedir(dir);
#endif

    if (found == 0) {
        /* 没有找到实际文件，用模拟的插件文件名演示发现过程 */
        printf("  未找到实际插件文件，使用模拟发现...\n\n");
        const char* simulated_files[] = {
            "deposit" PLUGIN_EXT,
            "withdraw" PLUGIN_EXT,
            "query" PLUGIN_EXT,
        };
        int num_files = (int)(sizeof(simulated_files) / sizeof(simulated_files[0]));

        for (int i = 0; i < num_files; i++) {
            printf("  [模拟] 发现插件文件: %s\n", simulated_files[i]);
            Plugin* p = load_plugin_from_file(simulated_files[i]);
            if (p != NULL) {
                plugin_register(p);
                found++;
            }
        }
    }

    printf("\n  目录扫描完成，发现并注册 %d 个插件\n", found);
    return found;
}

/* ============================================================
 *  第四部分：演示通过接口统一调用（多态）
 * ============================================================
 *
 *  【关键】这个函数只接收 Plugin* 指针
 *    它不知道也不关心这个插件是存款、取款还是查询
 *    它只通过接口调用 init/execute/cleanup
 *    —— 这就是"面向接口编程"，C语言的多态
 */
static void use_plugin(Plugin* p, double amount)
{
    if (p == NULL) return;

    printf("\n>>> 使用插件: %s\n", p->name);

    /* 通过接口统一调用，不关心具体实现 */
    if (p->init) p->init(p);
    if (p->execute) p->execute(p, amount);
    if (p->cleanup) p->cleanup(p);
}

/* ============================================================
 *  第五部分：主函数 —— ATM 插件系统演示
 * ============================================================
 */
int main(void)
{
    printf("============================================\n");
    printf("  第12讲：接口抽象与插件发现\n");
    printf("  ATM 插件接口化版本\n");
    printf("============================================\n\n");

    /* 1. 初始化插件管理器 */
    plugin_manager_init();

    /* 2. 演示手动注册插件 */
    printf("--- 手动注册插件 ---\n");
    plugin_register(&deposit_plugin);
    plugin_register(&withdraw_plugin);
    plugin_register(&query_plugin);

    /* 3. 演示目录扫描自动发现（模拟） */
    plugin_scan_directory("plugins");

    /* 4. 打印已注册插件列表 */
    plugin_list_print();

    /* 5. 初始化所有插件（遍历链表调用init） */
    plugin_init_all();

    /* 6. 演示多态：通过接口统一调用不同插件 */
    printf("\n========================================\n");
    printf("  演示多态：通过接口统一调用\n");
    printf("========================================\n");

    /* 查找并使用"存款"插件 */
    Plugin* p1 = plugin_find("存款");
    use_plugin(p1, 500.0);

    /* 查找并使用"取款"插件 */
    Plugin* p2 = plugin_find("取款");
    use_plugin(p2, 200.0);

    /* 查找并使用"查询余额"插件 */
    Plugin* p3 = plugin_find("查询余额");
    use_plugin(p3, 0.0);

    /* 7. 执行所有插件（遍历链表） */
    printf("\n========================================\n");
    printf("  遍历执行所有插件\n");
    printf("========================================\n");
    plugin_execute_all(100.0);

    /* 8. 清理所有插件 */
    plugin_cleanup_all();

    /* 9. 销毁插件管理器 */
    plugin_manager_destroy();

    /* 总结 */
    printf("\n");
    printf("┌──────────────────────────────────────┐\n");
    printf("│           第12讲 核心收获            │\n");
    printf("├──────────────────────────────────────┤\n");
    printf("│ 1. 结构体接口 = 多个函数指针打包     │\n");
    printf("│ 2. 链表管理 = 衔接第8讲              │\n");
    printf("│ 3. 注册机制 = 头部插入到链表          │\n");
    printf("│ 4. 目录扫描 = 自动发现插件           │\n");
    printf("│ 5. 多态调用 = 统一接口，不同实现     │\n");
    printf("│ 这就是C语言的面向对象设计！           │\n");
    printf("└──────────────────────────────────────┘\n");

    return 0;
}
