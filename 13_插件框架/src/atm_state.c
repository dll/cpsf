/*
 * ============================================================
 *  第13讲：插件框架架构
 *  atm_state.c —— ATM 共享账户状态的实现
 * ============================================================
 *
 *  用 static 全局变量保存状态，对外只暴露函数——
 *  这就是第9讲学过的"接口与实现分离"：
 *    调用方只能通过 atm_get_balance() 读余额，
 *    无法直接改 g_balance，数据被保护起来了。
 *
 *  （类比 C++：static 变量 = private 成员，
 *    暴露的函数 = public 方法）
 * ============================================================
 */

#include "atm_state.h"

/* 账户余额（初始 10000 元，方便演示） */
static double g_balance = 10000.0;

/* 转账收款方累计金额（用于演示"钱转到哪里去了"） */
static double g_target = 0.0;

void atm_reset(double initial_balance)
{
    g_balance = initial_balance;
    g_target = 0.0;
}

double atm_get_balance(void)
{
    return g_balance;
}

double atm_get_target(void)
{
    return g_target;
}

int atm_deposit(double amount)
{
    if (amount <= 0) {
        return -1;          /* 金额非法：由调用方决定怎么提示 */
    }
    g_balance += amount;
    return 0;
}

int atm_withdraw(double amount)
{
    if (amount <= 0) {
        return -1;
    }
    if (amount > g_balance) {
        return -2;          /* 余额不足 */
    }
    g_balance -= amount;
    return 0;
}

int atm_transfer(double amount)
{
    if (amount <= 0) {
        return -1;
    }
    if (amount > g_balance) {
        return -2;
    }
    g_balance -= amount;    /* 本方账户扣款 */
    g_target += amount;     /* 对方账户入账 */
    return 0;
}
