/*
 * ============================================================
 *  account.h —— 账户模块头文件（接口）
 * ============================================================
 *
 *  这是整个多文件拆分最关键的模块！
 *
 *  在第3讲里，余额是全局变量 g_balance，所有函数都能直接改。
 *  这就像把钱放在走廊里，谁路过都能拿——不安全。
 *
 *  现在我们把余额藏进 account.c，用 static 修饰，
 *  让它只在本文件内可见（文件级 static）。
 *  其他文件想查余额？只能调用 account_get_balance()。
 *  其他文件想改余额？只能通过 account_deposit / account_withdraw。
 *
 *  这就是"信息隐藏"——把数据藏起来，只暴露操作的接口。
 *  你不能直接碰余额，你只能通过"存款""取款"来间接改变它。
 *  就像银行金库——你不能自己进去拿钱，得通过柜员。
 *
 *  头文件只声明"能做什么"（接口），不透露"怎么做的"（实现）。
 *  外部不需要知道余额存在哪、怎么管理——只需要知道能查、能存、能取。
 * ============================================================
 */

#ifndef ACCOUNT_H    /* 头文件保护 */
#define ACCOUNT_H

/*
 * account_query —— 查询余额
 * 显示当前账户余额
 */
void account_query(void);

/*
 * account_deposit —— 存款
 * 读取用户输入的金额，加到余额上
 */
void account_deposit(void);

/*
 * account_withdraw —— 取款
 * 读取用户输入的金额，从余额中扣除
 */
void account_withdraw(void);

/*
 * account_transfer —— 转账
 * 读取金额和对方账号，从余额中扣除
 */
void account_transfer(void);

/*
 * account_get_balance —— 获取当前余额
 *
 * 返回值：当前余额
 *
 * 这个函数是余额的"只读窗口"。
 * 其他模块（比如 utils 打印成功信息时）需要知道余额，
 * 但不能直接碰 s_balance（它藏在 account.c 里），
 * 所以提供这个函数，让外部能"读"但不能"写"。
 */
double account_get_balance(void);

#endif /* ACCOUNT_H */
