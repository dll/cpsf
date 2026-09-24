/**
 * transaction.h - ATM交易模块接口
 * 第9讲：静态库
 *
 * 交易模块也打包进 libaccount.a，与账户模块一起提供给主程序。
 */
#ifndef TRANSACTION_H
#define TRANSACTION_H

#include <stdbool.h>

/* 交易类型枚举 */
typedef enum {
    TRANS_DEPOSIT,     /* 存款 */
    TRANS_WITHDRAW,    /* 取款 */
    TRANS_TRANSFER,    /* 转账 */
    TRANS_INQUIRE      /* 查询 */
} TransactionType;

/* 交易记录结构体 */
typedef struct {
    int             account_id;    /* 账户ID */
    TransactionType type;          /* 交易类型 */
    double          amount;        /* 交易金额 */
    int             target_id;     /* 转账目标ID（无则-1） */
} Transaction;

/* 存款交易，返回交易后余额 */
double transaction_deposit(int account_id, double amount);

/* 取款交易，返回交易后余额 */
double transaction_withdraw(int account_id, double amount);

/* 转账交易，成功返回true */
bool transaction_transfer(int from_id, int to_id, double amount);

/* 打印指定账户的交易历史 */
void transaction_print_history(int account_id);

#endif /* TRANSACTION_H */
