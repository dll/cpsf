/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  transaction.h —— 交易模块接口（链表记录流水，衔接第8讲）
 * ============================================================
 *
 *  【第8讲回顾】
 *    交易流水"数量不定、随时追加"，用数组怕溢出、用大数组又浪费，
 *    链表正好：来一笔 malloc 一个节点，挂到链尾，O(1) 追加。
 *
 *  【本讲用法】
 *    存款 / 取款 / 转账三个插件在完成账务操作后，
 *    调用 transaction_log() 记一笔流水；
 *    "查询"插件可以顺带打印流水。
 *    这些节点同样存放在 atmcore.dll 里，所有插件共享同一份流水。
 * ============================================================
 */

#ifndef TRANSACTION_H
#define TRANSACTION_H

#include <stdbool.h>
#include "account.h"   /* 复用 ATMCORE_API 导出宏，并声明依赖关系 */

/* 交易类型枚举 */
typedef enum {
    TRANS_DEPOSIT = 0,   /* 存款 */
    TRANS_WITHDRAW,      /* 取款 */
    TRANS_TRANSFER,      /* 转账 */
    TRANS_INQUIRE        /* 查询 */
} TransactionType;

/* ---- 交易流水（链表节点）---- */
typedef struct TransNode {
    int              account_id;   /* 所属账户 */
    TransactionType  type;         /* 交易类型 */
    double           amount;       /* 交易金额 */
    int              target_id;    /* 转账目标（无则 -1） */
    int              seq;          /* 流水号 */
    struct TransNode* next;        /* 指向下一条流水 */
} TransNode;

/* 交易类型转中文名 */
ATMCORE_API const char* transaction_type_name(TransactionType type);

/* 记录一笔流水（尾插法，O(1)） */
ATMCORE_API void transaction_log(int account_id, TransactionType type,
                                 double amount, int target_id);

/* 账户交易组合操作（内部会调用 account.h 的账户接口） */
ATMCORE_API double transaction_deposit(int account_id, double amount);
ATMCORE_API double transaction_withdraw(int account_id, double amount);
ATMCORE_API bool   transaction_transfer(int from_id, int to_id, double amount);

/* 打印指定账户的交易历史（遍历链表） */
ATMCORE_API void transaction_print_history(int account_id);

/* 打印全部交易历史 */
ATMCORE_API void transaction_print_all(void);

/* 流水总条数 */
ATMCORE_API int transaction_count(void);

/* 释放整条流水链表（由框架退出时调用） */
ATMCORE_API void transaction_destroy(void);

#endif /* TRANSACTION_H */
