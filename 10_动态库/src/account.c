/**
 * account.c - ATM账户管理模块实现（动态库版）
 * 第10讲：动态库
 *
 * 编译本文件时需定义 ACCOUNT_EXPORTS 宏，使 ACCOUNT_API 展开为
 * __declspec(dllexport)，函数才会被导出到 account.dll 中。
 *
 * 编译命令（Windows/MinGW）：
 *   gcc -Wall -Wextra -shared -o account.dll account.c transaction.c \
 *       -Wl,--out-implib,libaccount.dll.a -DACCOUNT_EXPORTS -DTRANSACTION_EXPORTS
 */
#include "account.h"
#include <stdio.h>
#include <string.h>

/* ============================================================
 * 内部数据（文件级 static，符号不导出，外部无法直接访问）
 * ------------------------------------------------------------
 * 这正是动态库封装性的体现：外部只能通过导出函数操作数据，
 * 看不到也改不了这几个数组和变量。
 * ============================================================ */
static Account accounts[MAX_ACCOUNTS];   /* 账户数组      */
static int     next_id = 1001;           /* 下一个账户ID  */
static int     account_count_val = 0;    /* 当前账户数量  */

/* ============================================================
 * 开户
 * ============================================================ */
ACCOUNT_API int account_create(const char *name, double initial_balance)
{
    Account *acc;

    if (account_count_val >= MAX_ACCOUNTS) {
        fprintf(stderr, "[错误] 账户数量已达上限 %d\n", MAX_ACCOUNTS);
        return -1;
    }
    if (initial_balance < 0) {
        fprintf(stderr, "[错误] 初始余额不能为负\n");
        return -1;
    }

    acc = &accounts[account_count_val];
    acc->id = next_id++;
    strncpy(acc->name, name, MAX_NAME_LEN - 1);
    acc->name[MAX_NAME_LEN - 1] = '\0';   /* 确保字符串以 '\0' 结尾 */
    acc->balance = initial_balance;
    acc->active = true;
    account_count_val++;

    printf("[开户] ID:%d  户名:%s  余额:%.2f\n",
           acc->id, acc->name, acc->balance);
    return acc->id;
}

/* ============================================================
 * 查找账户（按ID线性查找）
 * ============================================================ */
ACCOUNT_API Account* account_find(int id)
{
    int i;
    for (i = 0; i < account_count_val; i++) {
        if (accounts[i].id == id && accounts[i].active)
            return &accounts[i];
    }
    return NULL;
}

/* ============================================================
 * 存款
 * ============================================================ */
ACCOUNT_API bool account_deposit(int id, double amount)
{
    Account *acc = account_find(id);

    if (!acc) {
        fprintf(stderr, "[错误] 账户 %d 不存在\n", id);
        return false;
    }
    if (amount <= 0) {
        fprintf(stderr, "[错误] 存款金额必须大于0\n");
        return false;
    }

    acc->balance += amount;
    printf("[存款] 账户:%d  金额:%.2f  余额:%.2f\n", id, amount, acc->balance);
    return true;
}

/* ============================================================
 * 取款
 * ============================================================ */
ACCOUNT_API bool account_withdraw(int id, double amount)
{
    Account *acc = account_find(id);

    if (!acc) {
        fprintf(stderr, "[错误] 账户 %d 不存在\n", id);
        return false;
    }
    if (amount <= 0) {
        fprintf(stderr, "[错误] 取款金额必须大于0\n");
        return false;
    }
    if (acc->balance < amount) {
        fprintf(stderr, "[错误] 余额不足！当前余额:%.2f\n", acc->balance);
        return false;
    }

    acc->balance -= amount;
    printf("[取款] 账户:%d  金额:%.2f  余额:%.2f\n", id, amount, acc->balance);
    return true;
}

/* ============================================================
 * 查询余额
 * ============================================================ */
ACCOUNT_API double account_get_balance(int id)
{
    Account *acc = account_find(id);

    if (!acc) {
        fprintf(stderr, "[错误] 账户 %d 不存在\n", id);
        return -1.0;
    }
    return acc->balance;
}

/* ============================================================
 * 列出所有账户
 * ============================================================ */
ACCOUNT_API void account_list_all(void)
{
    int i;

    printf("\n======== 账户列表 ========\n");
    printf("%-8s %-20s %-12s %-6s\n", "ID", "户名", "余额", "状态");
    printf("--------------------------------------------\n");
    for (i = 0; i < account_count_val; i++) {
        printf("%-8d %-20s %-12.2f %-6s\n",
               accounts[i].id,
               accounts[i].name,
               accounts[i].balance,
               accounts[i].active ? "活跃" : "冻结");
    }
    printf("--------------------------------------------\n");
    printf("总计: %d 个账户\n\n", account_count_val);
}

/* ============================================================
 * 账户总数
 * ============================================================ */
ACCOUNT_API int account_count(void)
{
    return account_count_val;
}
