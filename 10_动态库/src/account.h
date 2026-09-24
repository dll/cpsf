/**
 * account.h - ATM账户管理模块接口（动态库版）
 * 第10讲：动态库
 *
 * 这是动态库 account.dll / libaccount.so 对外暴露的接口头文件。
 * 与第9讲静态库版最大的区别：函数声明上多了导出/导入宏 ACCOUNT_API。
 *
 * 为什么要这个宏？
 *   静态库(.a)是把代码复制进 exe，函数符号天然可见，不需要标记。
 *   动态库(.dll/.so)是把代码放在单独的二进制文件里，必须显式声明
 *   "哪些函数要导出给外部使用"，否则链接时会找不到符号。
 *
 * 跨平台写法：
 *   Windows: __declspec(dllexport) 导出 / __declspec(dllimport) 导入
 *   Linux:   __attribute__((visibility("default")))
 *
 * 用 ACCOUNT_EXPORTS 做开关：
 *   编译动态库本身   → 加 -DACCOUNT_EXPORTS  → 函数用 dllexport 导出
 *   编译使用库的程序 → 不加宏                → 函数用 dllimport 导入
 */
#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <stdbool.h>

/* ============================================================
 * 常量定义
 * ============================================================ */
#define MAX_NAME_LEN   50    /* 户名最大长度 */
#define MAX_ACCOUNTS   100   /* 最大账户数   */

/* ============================================================
 * 跨平台导出 / 导入宏（本讲的第一个新知识点）
 * ============================================================ */
#if defined(_WIN32) || defined(_MSC_VER)
    /* Windows 平台：用 __declspec 声明导出或导入 */
    #ifdef ACCOUNT_EXPORTS
        #define ACCOUNT_API __declspec(dllexport)
    #else
        #define ACCOUNT_API __declspec(dllimport)
    #endif
#else
    /* Linux / macOS 平台：默认可见性即导出 */
    #define ACCOUNT_API __attribute__((visibility("default")))
#endif

/* ============================================================
 * 账户结构体
 * ============================================================ */
typedef struct {
    int    id;                    /* 账户ID       */
    char   name[MAX_NAME_LEN];    /* 户名         */
    double balance;               /* 账户余额     */
    bool   active;                /* 是否活跃     */
} Account;

/* ============================================================
 * 账户管理接口（均带 ACCOUNT_API，会被导出到动态库）
 * ============================================================ */

/* 创建账户，返回账户ID，失败返回-1 */
ACCOUNT_API int      account_create(const char *name, double initial_balance);

/* 查找账户，返回账户指针，未找到返回NULL */
ACCOUNT_API Account* account_find(int id);

/* 存款，成功返回true */
ACCOUNT_API bool     account_deposit(int id, double amount);

/* 取款，成功返回true */
ACCOUNT_API bool     account_withdraw(int id, double amount);

/* 查询余额 */
ACCOUNT_API double   account_get_balance(int id);

/* 列出所有账户 */
ACCOUNT_API void     account_list_all(void);

/* 获取账户总数 */
ACCOUNT_API int      account_count(void);

#endif /* ACCOUNT_H */
