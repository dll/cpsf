/**
 * transaction.c - ATM交易模块实现
 * 第9讲：静态库
 *
 * 交易模块依赖账户模块（调用 account_deposit 等函数）。
 * 编译后用 ar 与 account.o 一起打包进 libaccount.a。
 */
#include "transaction.h"
#include "account.h"
#include <stdio.h>

/* ---- 内部数据 ---- */
#define MAX_TRANSACTIONS 200

static Transaction transactions[MAX_TRANSACTIONS];
static int trans_count = 0;

/* ---- 内部辅助函数（文件级 static）---- */

/* 记录一笔交易 */
static void log_transaction(int account_id, TransactionType type,
                            double amount, int target_id)
{
    if (trans_count >= MAX_TRANSACTIONS) {
        fprintf(stderr, "[警告] 交易记录已满\n");
        return;
    }
    transactions[trans_count].account_id = account_id;
    transactions[trans_count].type = type;
    transactions[trans_count].amount = amount;
    transactions[trans_count].target_id = target_id;
    trans_count++;
}

/* ---- 接口实现 ---- */

double transaction_deposit(int account_id, double amount)
{
    if (account_deposit(account_id, amount)) {
        log_transaction(account_id, TRANS_DEPOSIT, amount, -1);
        return account_get_balance(account_id);
    }
    return -1.0;
}

double transaction_withdraw(int account_id, double amount)
{
    if (account_withdraw(account_id, amount)) {
        log_transaction(account_id, TRANS_WITHDRAW, amount, -1);
        return account_get_balance(account_id);
    }
    return -1.0;
}

bool transaction_transfer(int from_id, int to_id, double amount)
{
    if (!account_find(from_id) || !account_find(to_id)) {
        fprintf(stderr, "[错误] 账户不存在\n");
        return false;
    }
    if (!account_withdraw(from_id, amount)) {
        fprintf(stderr, "[错误] 转出失败\n");
        return false;
    }
    account_deposit(to_id, amount);
    log_transaction(from_id, TRANS_TRANSFER, amount, to_id);
    printf("[转账] %d -> %d  金额:%.2f\n", from_id, to_id, amount);
    return true;
}

void transaction_print_history(int account_id)
{
    int i;
    const char *type_names[] = {"存款", "取款", "转账", "查询"};

    printf("\n===== 账户 %d 交易记录 =====\n", account_id);
    printf("%-8s  %-8s  %-10s\n", "账户ID", "类型", "金额");
    printf("------------------------------\n");
    for (i = 0; i < trans_count; i++) {
        if (transactions[i].account_id == account_id) {
            printf("%-8d  %-8s  %-10.2f\n",
                   transactions[i].account_id,
                   type_names[transactions[i].type],
                   transactions[i].amount);
        }
    }
    printf("------------------------------\n\n");
}
