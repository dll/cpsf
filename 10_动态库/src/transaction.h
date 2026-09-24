/**
 * transaction.h - ATM交易模块接口（动态库版）
 * 第10讲：动态库
 *
 * 交易模块依赖账户模块：转账要先转出再转入，所以内部会调用 account.h 的接口。
 *
 * 导出宏 TRANSACTION_API 的写法与 account.h 中的 ACCOUNT_API 完全对称：
 *   编译动态库时加 -DTRANSACTION_EXPORTS → 导出
 *   使用库的程序不加宏                  → 导入
 */
#ifndef TRANSACTION_H
#define TRANSACTION_H

#include <stdbool.h>

/* 交易模块内部要调用账户接口，因此需要包含 account.h */
#include "account.h"

/* ============================================================
 * 跨平台导出 / 导入宏（与 account.h 的 ACCOUNT_API 对称）
 * ============================================================ */
#if defined(_WIN32) || defined(_MSC_VER)
    /* Windows 平台：用 __declspec 声明导出或导入 */
    #ifdef TRANSACTION_EXPORTS
        #define TRANSACTION_API __declspec(dllexport)
    #else
        #define TRANSACTION_API __declspec(dllimport)
    #endif
#else
    /* Linux / macOS 平台：默认可见性即导出 */
    #define TRANSACTION_API __attribute__((visibility("default")))
#endif

/* ============================================================
 * 交易类型与交易记录结构体
 * ============================================================ */
typedef enum {
    TRANS_DEPOSIT,     /* 存款 */
    TRANS_WITHDRAW,    /* 取款 */
    TRANS_TRANSFER,    /* 转账 */
    TRANS_INQUIRE      /* 查询 */
} TransactionType;

typedef struct {
    int             account_id;  /* 本笔交易所属账户 */
    TransactionType type;        /* 交易类型         */
    double          amount;      /* 交易金额         */
    int             target_id;   /* 转账对手方账户，非转账为 -1 */
} Transaction;

/* ============================================================
 * 交易接口（均带 TRANSACTION_API，会被导出到动态库）
 * ============================================================ */

/* 存款（带交易记录），返回交易后余额，失败返回-1.0 */
TRANSACTION_API double transaction_deposit(int account_id, double amount);

/* 取款（带交易记录），返回交易后余额，失败返回-1.0 */
TRANSACTION_API double transaction_withdraw(int account_id, double amount);

/* 转账，成功返回true */
TRANSACTION_API bool   transaction_transfer(int from_id, int to_id, double amount);

/* 打印某账户的交易记录 */
TRANSACTION_API void   transaction_print_history(int account_id);

#endif /* TRANSACTION_H */
