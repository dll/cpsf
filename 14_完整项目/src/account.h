/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  account.h —— 账户模块接口（沿用第9讲"库化"思路）
 * ============================================================
 *
 *  【第9讲的思路】
 *    第9讲我们把 account / transaction 编译成静态库 libaccount.a，
 *    主程序只 #include 头文件、链接库即可使用，接口与实现分离。
 *
 *  【本讲的进化】
 *    为了让"主程序 + 多个插件 DLL"共享同一份账户数据，
 *    本讲把这两个模块编译成一个 **共享库 atmcore.dll**：
 *
 *      主程序     ─┐
 *      插件 DLL A ─┼──> atmcore.dll（唯一的账户/交易数据）
 *      插件 DLL B ─┘
 *
 *    为什么必须共享？因为 DLL 里的全局变量是"每个 DLL 各一份"。
 *    如果把 account.c 分别编进每个插件，每个插件都会有自己的
 *    余额副本——存了钱再查余额就变回原样了。
 *    把它做成共享库，所有模块才看到同一份数据。
 *    这正是"模块 → 库 → 共享库"这层抽象在工程上的价值。
 *
 *  【导出宏说明】
 *    ATMCORE_BUILD 只在编译 atmcore.dll 时定义：
 *      编译共享库时 → __declspec(dllexport) 导出符号
 *      其它模块引用时 → __declspec(dllimport) 声明导入
 *    Linux 下两者都为空（默认导出全部符号）。
 * ============================================================
 */

#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <stdbool.h>

#ifdef _WIN32
    #ifdef ATMCORE_BUILD
        #define ATMCORE_API __declspec(dllexport)
    #else
        #define ATMCORE_API __declspec(dllimport)
    #endif
#else
    #define ATMCORE_API
#endif

#define MAX_NAME_LEN   50    /* 户名最大长度 */
#define MAX_ACCOUNTS   100   /* 最大账户数 */

/* 账户结构体 */
typedef struct {
    int    id;                    /* 账户ID */
    char   name[MAX_NAME_LEN];    /* 户名 */
    double balance;               /* 账户余额 */
    bool   active;                /* 是否活跃 */
} Account;

/*
 * ---- 生命周期 / 演示数据 ----
 */

/* 初始化演示账户（张三 1001 / 李四 1002）并清空数据 */
ATMCORE_API void account_init_demo(void);

/* ---- 账户操作 ---- */

/* 创建账户，返回账户ID，失败返回 -1 */
ATMCORE_API int account_create(const char *name, double initial_balance);

/* 查找账户，返回账户指针，未找到返回 NULL */
ATMCORE_API Account* account_find(int id);

/* 存款，成功返回 true */
ATMCORE_API bool account_deposit(int id, double amount);

/* 取款，成功返回 true */
ATMCORE_API bool account_withdraw(int id, double amount);

/* 查询余额，账户不存在返回 -1.0 */
ATMCORE_API double account_get_balance(int id);

/* 列出所有账户 */
ATMCORE_API void account_list_all(void);

/* 获取账户总数 */
ATMCORE_API int account_count(void);

/*
 * ---- "当前账户"概念 ----
 *   ATM 场景里用户插入一张卡，后续存取查都作用在这张卡上。
 *   这里用"当前账户"模拟这张卡，插件不需要自己维护这个状态。
 */
ATMCORE_API int  account_current_id(void);
ATMCORE_API void account_set_current(int id);

#endif /* ACCOUNT_H */
