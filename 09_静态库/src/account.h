/**
 * account.h - ATM账户管理模块接口
 * 第9讲：静态库
 *
 * 这是静态库 libaccount.a 对外暴露的接口头文件。
 * 主程序只需 #include 此文件即可使用库中的函数。
 */
#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <stdbool.h>

#define MAX_NAME_LEN   50    /* 户名最大长度 */
#define MAX_ACCOUNTS   100   /* 最大账户数 */

/* 账户结构体 */
typedef struct {
    int    id;                    /* 账户ID */
    char   name[MAX_NAME_LEN];   /* 户名 */
    double balance;              /* 账户余额 */
    bool   active;                /* 是否活跃 */
} Account;

/* 创建账户，返回账户ID，失败返回-1 */
int account_create(const char *name, double initial_balance);

/* 查找账户，返回账户指针，未找到返回NULL */
Account* account_find(int id);

/* 存款，成功返回true */
bool account_deposit(int id, double amount);

/* 取款，成功返回true */
bool account_withdraw(int id, double amount);

/* 查询余额 */
double account_get_balance(int id);

/* 列出所有账户 */
void account_list_all(void);

/* 获取账户总数 */
int account_count(void);

#endif /* ACCOUNT_H */
