/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  transaction.c —— 交易模块实现（链表记录流水）
 * ============================================================
 *
 *  【链表三件套（第8讲）】
 *    head（头）/ tail（尾）/ count（计数）
 *    尾插 → O(1) 追加
 *    遍历 → 打印/统计
 *    销毁 → 逐个 free，防止内存泄漏
 *
 *  【为什么放在 atmcore.dll 里？】
 *    流水也是共享状态。存取转账由不同插件发起，
 *    但流水必须汇到同一条链表，才能完整回放账户历史。
 * ============================================================
 */

#include "transaction.h"
#include "account.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---- 内部数据：流水链表的头、尾与计数 ---- */
static TransNode *trans_head = NULL;
static TransNode *trans_tail = NULL;
static int trans_total = 0;
static int trans_seq = 0;

const char* transaction_type_name(TransactionType type)
{
    switch (type) {
        case TRANS_DEPOSIT:  return "存款";
        case TRANS_WITHDRAW: return "取款";
        case TRANS_TRANSFER: return "转账";
        case TRANS_INQUIRE:  return "查询";
        default:             return "未知";
    }
}

/* 记录一笔流水（尾插法） */
void transaction_log(int account_id, TransactionType type,
                     double amount, int target_id)
{
    TransNode *node = (TransNode*)malloc(sizeof(TransNode));
    if (node == NULL) {
        fprintf(stderr, "[警告] 流水节点分配失败，本次不记录\n");
        return;
    }
    node->account_id = account_id;
    node->type       = type;
    node->amount     = amount;
    node->target_id  = target_id;
    node->seq        = ++trans_seq;
    node->next       = NULL;

    /* 尾插：链表为空则头尾都指向它，否则挂到尾部 */
    if (trans_head == NULL) {
        trans_head = node;
        trans_tail = node;
    } else {
        trans_tail->next = node;
        trans_tail = node;
    }
    trans_total++;
}

double transaction_deposit(int account_id, double amount)
{
    if (account_deposit(account_id, amount)) {
        transaction_log(account_id, TRANS_DEPOSIT, amount, -1);
        return account_get_balance(account_id);
    }
    return -1.0;
}

double transaction_withdraw(int account_id, double amount)
{
    if (account_withdraw(account_id, amount)) {
        transaction_log(account_id, TRANS_WITHDRAW, amount, -1);
        return account_get_balance(account_id);
    }
    return -1.0;
}

bool transaction_transfer(int from_id, int to_id, double amount)
{
    if (account_find(from_id) == NULL || account_find(to_id) == NULL) {
        fprintf(stderr, "[错误] 账户不存在\n");
        return false;
    }
    if (from_id == to_id) {
        fprintf(stderr, "[错误] 不能给自己转账\n");
        return false;
    }
    /* 先扣款再入账；扣款失败（余额不足）则整体回滚 */
    if (!account_withdraw(from_id, amount)) {
        fprintf(stderr, "[错误] 转账失败：余额不足\n");
        return false;
    }
    account_deposit(to_id, amount);
    transaction_log(from_id, TRANS_TRANSFER, amount, to_id);
    printf("  [转账] %d -> %d  金额:%.2f\n", from_id, to_id, amount);
    return true;
}

/* 打印指定账户的交易历史（遍历链表） */
void transaction_print_history(int account_id)
{
    TransNode *cur = trans_head;
    int found = 0;

    printf("\n  ===== 账户 %d 交易流水 =====\n", account_id);
    printf("  %-6s %-6s %-12s %-10s\n", "流水", "类型", "金额", "对手");
    printf("  ----------------------------------------\n");
    while (cur != NULL) {
        if (cur->account_id == account_id) {
            if (cur->target_id >= 0) {
                printf("  %-6d %-6s %-12.2f ->%d\n",
                       cur->seq, transaction_type_name(cur->type),
                       cur->amount, cur->target_id);
            } else {
                printf("  %-6d %-6s %-12.2f %-10s\n",
                       cur->seq, transaction_type_name(cur->type),
                       cur->amount, "-");
            }
            found++;
        }
        cur = cur->next;
    }
    printf("  ----------------------------------------\n");
    printf("  共 %d 条流水\n", found);
}

/* 打印全部交易历史 */
void transaction_print_all(void)
{
    TransNode *cur = trans_head;
    printf("\n  ===== 全部交易流水（共 %d 条）=====\n", trans_total);
    printf("  %-6s %-8s %-6s %-12s %-8s\n", "流水", "账户", "类型", "金额", "对手");
    printf("  ----------------------------------------\n");
    while (cur != NULL) {
        if (cur->target_id >= 0) {
            printf("  %-6d %-8d %-6s %-12.2f ->%d\n",
                   cur->seq, cur->account_id,
                   transaction_type_name(cur->type), cur->amount, cur->target_id);
        } else {
            printf("  %-6d %-8d %-6s %-12.2f %-8s\n",
                   cur->seq, cur->account_id,
                   transaction_type_name(cur->type), cur->amount, "-");
        }
        cur = cur->next;
    }
    printf("  ----------------------------------------\n");
}

int transaction_count(void)
{
    return trans_total;
}

/* 释放整条流水链表：先存 next，再 free 当前（第8讲的标准姿势） */
void transaction_destroy(void)
{
    TransNode *cur = trans_head;
    int freed = 0;
    while (cur != NULL) {
        TransNode *tmp = cur;
        cur = cur->next;
        free(tmp);
        freed++;
    }
    trans_head = NULL;
    trans_tail = NULL;
    trans_total = 0;
    trans_seq = 0;
    printf("  [交易模块] 已释放 %d 条流水节点\n", freed);
}
