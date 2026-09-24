/**
 * transaction.c - ATM交易模块实现（动态库版）
 * 第10讲：动态库
 *
 * 编译本文件时需定义 TRANSACTION_EXPORTS 宏，使 TRANSACTION_API 展开为
 * __declspec(dllexport)，函数才会被导出到 account.dll 中。
 *
 * 注意：交易模块是"调用方"——它内部调用 account.c 的账户接口。
 * 因为 account.c 与 transaction.c 被编进同一个 dll，编译时同时定义了
 * ACCOUNT_EXPORTS，所以这里的 account_deposit() 等调用是库内的直接调用，
 * 不走导入表，效率与静态库一致。
 */
#include "transaction.h"
#include "account.h"
#include <stdio.h>

/* ============================================================
 * 内部数据与内部函数（不导出）
 * ============================================================ */
#define MAX_TRANSACTIONS 200

static Transaction transactions[MAX_TRANSACTIONS];  /* 交易记录数组 */
static int         trans_count = 0;                 /* 交易记录条数 */

/* 记录一笔交易（static 内部函数，不对外导出） */
static void log_transaction(int account_id, TransactionType type,
                            double amount, int target_id)
{
    if (trans_count >= MAX_TRANSACTIONS) {
        fprintf(stderr, "[警告] 交易记录已满\n");
        return;
    }
    transactions[trans_count].account_id = account_id;
    transactions[trans_count].type       = type;
    transactions[trans_count].amount     = amount;
    transactions[trans_count].target_id  = target_id;
    trans_count++;
}

/* ============================================================
 * 存款（调用账户接口 + 记录流水）
 * ============================================================ */
TRANSACTION_API double transaction_deposit(int account_id, double amount)
{
    if (account_deposit(account_id, amount)) {
        log_transaction(account_id, TRANS_DEPOSIT, amount, -1);
        return account_get_balance(account_id);
    }
    return -1.0;
}

/* ============================================================
 * 取款（调用账户接口 + 记录流水）
 * ============================================================ */
TRANSACTION_API double transaction_withdraw(int account_id, double amount)
{
    if (account_withdraw(account_id, amount)) {
        log_transaction(account_id, TRANS_WITHDRAW, amount, -1);
        return account_get_balance(account_id);
    }
    return -1.0;
}

/* ============================================================
 * 转账（先转出、再转入、记录流水）
 * ============================================================ */
TRANSACTION_API bool transaction_transfer(int from_id, int to_id, double amount)
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

/* ============================================================
 * 打印某账户的交易记录
 * ============================================================ */
TRANSACTION_API void transaction_print_history(int account_id)
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
