/*
 * ============================================================
 *  account.c —— 账户模块源文件（实现）
 * ============================================================
 *
 *  ★ 本文件是第4讲的核心：演示 static 的"文件级"用法 ★
 *
 *  对比第3讲：
 *    第3讲：double g_balance = 1000.0;    ← 全局变量，全程序可见
 *    第4讲：static double s_balance = 1000.0;  ← 文件级，只在本文件可见
 *
 *  加了 static 之后，s_balance 只在 account.c 内有效。
 *  main.c、menu.c、utils.c 都看不到它，也改不了它。
 *  想动余额？只能通过本文件里的 account_deposit 等函数。
 *
 *  这就是"把全局变量关进笼子"——缩小可见范围，降低风险。
 *
 *  本文件还演示了 static 的另一种用法：
 *    static int validate_amount(double amount);
 *  这是"函数级 static"——函数加了 static，只在本文件内可调用。
 *  外部文件不能直接调用 validate_amount，只能通过 account_deposit 间接使用。
 *
 *  所以 static 在 C 语言中有两种含义：
 *    1. 修饰全局变量/函数 → 限制在本文件内（文件级 static）
 *    2. 修饰局部变量     → 延长生命周期到程序结束（函数级 static）
 *  本文件演示的是第1种用法。
 * ============================================================
 */

#include <stdio.h>
#include "account.h"   /* 包含自己的头文件 */
#include "utils.h"      /* 因为存款/取款要调用 print_success / print_error */

/*
 * s_balance —— 账户余额
 *
 * static 修饰的全局变量，只在 account.c 内可见。
 * 对比第3讲的 g_balance（非 static 全局变量，全程序可见）。
 *
 * s_ 前缀表示 static（静态），和第3讲的 g_（global）形成对比。
 */
static double s_balance = 1000.0;

/*
 * validate_amount —— 验证金额是否有效
 *
 * static 修饰的函数，只在 account.c 内可调用。
 * 外部文件（main.c 等）看不到这个函数，不能直接调用。
 * 它是 account.c 的"私有助手"。
 *
 * 为什么不放到头文件里？
 *   因为它是内部实现细节，不需要暴露给外部。
 *   外部只需要知道"能存款"，不需要知道"存款时怎么验证金额"。
 */
static int validate_amount(double amount)
{
    if (amount <= 0)
    {
        print_error("金额必须大于0！");
        return 0;   /* 验证失败 */
    }
    return 1;       /* 验证通过 */
}

/*
 * account_query 实现
 * 查询并显示当前余额
 */
void account_query(void)
{
    printf("【查询余额】\n");
    printf("您当前的账户余额为：%.2f 元\n", s_balance);
}

/*
 * account_deposit 实现
 * 读取金额，验证后加到余额上
 */
void account_deposit(void)
{
    double amount = 0.0;

    printf("【存款业务】\n");
    printf("请输入存款金额：");
    scanf("%lf", &amount);

    /* 调用 static 函数验证金额 */
    if (!validate_amount(amount))
    {
        return;     /* 验证失败，提前结束 */
    }

    s_balance = s_balance + amount;
    print_success("存入", amount, s_balance);
}

/*
 * account_withdraw 实现
 * 读取金额，验证余额后扣除
 */
void account_withdraw(void)
{
    double amount = 0.0;

    printf("【取款业务】\n");
    printf("请输入取款金额：");
    scanf("%lf", &amount);

    if (!validate_amount(amount))
    {
        return;
    }

    if (amount > s_balance)
    {
        print_error("余额不足！");
        return;
    }

    s_balance = s_balance - amount;
    print_success("取出", amount, s_balance);
}

/*
 * account_transfer 实现
 * 读取金额和对方账号，扣除余额
 */
void account_transfer(void)
{
    double amount = 0.0;
    int target_account = 0;

    printf("【转账业务】\n");
    printf("请输入转账金额：");
    scanf("%lf", &amount);

    if (!validate_amount(amount))
    {
        return;
    }

    if (amount > s_balance)
    {
        print_error("余额不足，无法转账！");
        return;
    }

    printf("请输入对方账号：");
    scanf("%d", &target_account);

    s_balance = s_balance - amount;
    printf("✅ 转账成功！向账号 %d 转出 %.2f 元\n", target_account, amount);
    printf("当前余额：%.2f 元\n", s_balance);
}

/*
 * account_get_balance 实现
 * 返回当前余额——外部读取余额的唯一途径
 *
 * 注意：这个函数只"读"不"写"。
 * 外部能查余额，但不能直接修改 s_balance。
 * 所有修改都必须经过 account_deposit / account_withdraw / account_transfer。
 */
double account_get_balance(void)
{
    return s_balance;
}

/*
 * ============================================================
 *  对比第3讲，我们做了什么？
 * ============================================================
 *
 *  ✅ 1. 余额从"全局变量"变成"文件级静态变量"
 *     第3讲：g_balance 谁都能改——不安全
 *     第4讲：s_balance 只有 account.c 能改——安全多了
 *
 *  ✅ 2. 验证逻辑抽成 static 函数
 *     validate_amount 只在 account.c 内部使用
 *     外部不需要知道我们怎么验证金额
 *
 *  ✅ 3. 提供了 account_get_balance 只读接口
 *     外部能查余额，但不能改——读写分离
 *
 *  ✅ 4. 接口与实现分离
 *     外部看 account.h（接口），不需要看 account.c（实现）
 *     实现可以随时改（比如以后余额改用数组存多个账户）
 *     只要接口不变，调用者不受影响
 * ============================================================
 */
