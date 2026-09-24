/*
 * ============================================================
 *  第3讲：函数封装 —— ATM 函数化版本
 *  给代码找个家：从"大杂烩"到"各归各位"
 * ============================================================
 *
 *  用函数重构第2讲的 ATM 程序，体验函数封装的好处
 *
 *  改造前的痛点：
 *    1. main 函数太长，所有代码堆在一起
 *    2. 存款/取款/转账逻辑重复，都是复制粘贴
 *    3. 想改一个功能，得在代码海里找半天
 *    4. 代码没法复用，另一个程序要用只能复制
 *
 *  改造后的样子：
 *    1. 每个功能一个函数，main 变得清爽
 *    2. 公共逻辑抽成函数，消除重复
 *    3. 想改哪个功能，直接找对应的函数
 *    4. 函数可以在其他程序中复用
 */

#include <stdio.h>

// ========== 全局变量 ==========
//
// 余额需要被多个函数使用，所以定义为全局变量
// （后面讲指针的时候，我们会学习更好的方式）
//
double g_balance = 1000.0;   // g_ 前缀表示 global（全局）

// ============================================================
//  函数声明（函数原型）
// ============================================================
//
// 告诉编译器："这些函数存在，定义在后面"
// 就像菜单——先告诉你有什么菜，菜的做法在后面
//
void show_welcome(void);      // 显示欢迎界面
void show_menu(void);         // 显示主菜单
void query_balance(void);     // 查询余额
void deposit(void);           // 存款
void withdraw(void);          // 取款
void transfer(void);          // 转账
void print_success(char* op, double amount);  // 打印成功信息
void print_error(char* msg);  // 打印错误信息

// ============================================================
//  主函数
// ============================================================
//
// 对比第2讲：main 函数变得非常清爽！
// 它只负责"调度"——显示菜单、读取选择、调用对应函数
// 具体的业务逻辑都封装在各个函数里
//
int main()
{
    int choice = 0;
    int running = 1;

    // 显示欢迎界面（调用函数）
    show_welcome();

    // 主循环
    while (running)
    {
        // 显示菜单（调用函数）
        show_menu();

        // 读取用户输入
        printf("请输入您的选择：");
        scanf("%d", &choice);
        printf("\n");

        // 根据选择调用不同的函数
        switch (choice)
        {
            case 1:
                query_balance();    // 查询余额
                break;
            case 2:
                deposit();          // 存款
                break;
            case 3:
                withdraw();         // 取款
                break;
            case 4:
                transfer();         // 转账
                break;
            case 0:
                printf("感谢使用 CCIT ATM 系统，再见！\n");
                running = 0;
                break;
            default:
                print_error("无效的选择，请重新输入！");
                break;
        }
    }

    return 0;
}

// ============================================================
//  函数定义
// ============================================================

// ---------- show_welcome：显示欢迎界面 ----------
//
// 功能：打印欢迎标题
// 参数：无（void 表示没有参数）
// 返回值：无（void 表示不返回值）
//
void show_welcome(void)
{
    printf("========================================\n");
    printf("       欢迎使用 CCIT ATM 系统\n");
    printf("========================================\n");
    printf("\n");
}

// ---------- show_menu：显示主菜单 ----------
//
// 功能：打印菜单选项
//
void show_menu(void)
{
    printf("\n-------- 主菜单 --------\n");
    printf("  1. 查询余额\n");
    printf("  2. 存款\n");
    printf("  3. 取款\n");
    printf("  4. 转账\n");
    printf("  0. 退出\n");
    printf("------------------------\n");
}

// ---------- query_balance：查询余额 ----------
//
// 功能：显示当前余额
//
void query_balance(void)
{
    printf("【查询余额】\n");
    printf("您当前的账户余额为：%.2f 元\n", g_balance);
}

// ---------- deposit：存款 ----------
//
// 功能：存入金额
//
void deposit(void)
{
    double amount = 0.0;

    printf("【存款业务】\n");
    printf("请输入存款金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("存款金额必须大于0！");
        return;     // return 可以提前结束函数
    }

    g_balance = g_balance + amount;
    print_success("存入", amount);
}

// ---------- withdraw：取款 ----------
//
// 功能：取出金额
//
void withdraw(void)
{
    double amount = 0.0;

    printf("【取款业务】\n");
    printf("请输入取款金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("取款金额必须大于0！");
        return;
    }

    if (amount > g_balance)
    {
        print_error("余额不足！");
        return;
    }

    g_balance = g_balance - amount;
    print_success("取出", amount);
}

// ---------- transfer：转账 ----------
//
// 功能：向其他账号转账
//
void transfer(void)
{
    double amount = 0.0;
    int target_account = 0;

    printf("【转账业务】\n");
    printf("请输入转账金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("转账金额必须大于0！");
        return;
    }

    if (amount > g_balance)
    {
        print_error("余额不足，无法转账！");
        return;
    }

    printf("请输入对方账号：");
    scanf("%d", &target_account);

    g_balance = g_balance - amount;

    printf("✅ 转账成功！向账号 %d 转出 %.2f 元\n", target_account, amount);
    printf("当前余额：%.2f 元\n", g_balance);
}

// ---------- print_success：打印成功信息 ----------
//
// 功能：统一的成功提示格式
// 参数：op - 操作名称（"存入"/"取出"等）
//       amount - 金额
//
// 为什么抽成函数？
//   因为存款、取款都要打印"操作成功 + 当前余额"，
//   代码几乎一模一样，抽成函数就不用重复写了。
//
void print_success(char* op, double amount)
{
    printf("✅ 操作成功！%s %.2f 元\n", op, amount);
    printf("当前余额：%.2f 元\n", g_balance);
}

// ---------- print_error：打印错误信息 ----------
//
// 功能：统一的错误提示格式
// 参数：msg - 错误信息
//
void print_error(char* msg)
{
    printf("❌ %s\n", msg);
}

/*
 * ============================================================
 *  对比第2讲，我们收获了什么？
 * ============================================================
 *
 *  ✅ 1. main 函数变清爽了
 *     原来：几十行代码堆在一起
 *     现在：只负责调度，一目了然
 *
 *  ✅ 2. 消除了代码重复
 *     原来：每个功能都自己写成功提示、错误提示
 *     现在：抽成 print_success / print_error，到处调用
 *
 *  ✅ 3. 代码更好找了
 *     原来：想改取款逻辑？在main里慢慢找
 *     现在：直接找 withdraw 函数
 *
 *  ✅ 4. 代码可以复用了
 *     原来：另一个程序要用存款功能？复制粘贴
 *     现在：直接把 deposit 函数拿过去用
 *
 *  ✅ 5. 职责更清晰了
 *     每个函数只做一件事（单一职责原则）
 *     show_welcome 只负责显示欢迎
 *     deposit 只负责存款逻辑
 *     print_success 只负责打印成功信息
 *
 * ============================================================
 *  思考：还有问题吗？
 * ============================================================
 *
 *  函数封装解决了很多问题，但新的问题也来了：
 *
 *  ❓ 1. 全局变量 g_balance 太危险了
 *     所有函数都能改它，改乱了怎么办？
 *     （后面用指针 + 参数传递来解决）
 *
 *  ❓ 2. 所有函数都在一个文件里
 *     函数越来越多，文件越来越长...
 *     （下一讲：多文件编程，拆分成多个文件）
 *
 *  ❓ 3. 如果有10个业务功能，switch里要写10个case？
 *     （后面用函数指针 + 插件机制来解决）
 *
 *  💡 每解决一个问题，就会遇到新的问题
 *     这就是技术演进的动力 —— 从函数到模块，从库到框架
 *
 * ============================================================
 */
