/**
 * main.c - ATM主程序（动态库版 · 加载时链接）
 * 第10讲：动态库
 *
 * 本程序在启动时由操作系统自动加载动态库，这种方式叫"加载时链接"。
 *
 * 源码与第9讲静态库版的 main.c 几乎一模一样，调用方式完全相同：
 *   - 仍然只 #include "account.h" 和 "transaction.h"
 *   - 仍然直接调用 account_create() / transaction_deposit()
 * 区别只在于"链接方式"和背后的运行机制：
 *   静态库: 代码被复制进 exe，运行时不需要 .a 文件
 *   动态库: exe 里只留下"导入表(IAT)"，记录需要哪个 dll 的哪个函数；
 *           程序启动时由 OS 加载器把 account.dll 映射进进程地址空间，
 *           再把导入表里的指针填好，之后函数调用才能正确跳转。
 *
 * 编译链接：
 *   Windows: gcc -Wall -Wextra -o atm_dynamic.exe main.c -L. -laccount
 *            (链接导入库 libaccount.dll.a，运行时需要 account.dll)
 *   Linux:   gcc -Wall -Wextra -o atm_dynamic main.c -L. -laccount \
 *                -Wl,-rpath,. -Wl,-rpath,'$ORIGIN'
 *            (链接 libaccount.so，运行时按 rpath 找到它)
 */
#include "account.h"
#include "transaction.h"
#include <stdio.h>

/* ============================================================
 * 显示主菜单
 * ============================================================ */
static void show_menu(void)
{
    printf("\n");
    printf("  +============================+\n");
    printf("  |     ATM 银行系统           |\n");
    printf("  |     （动态库版本）          |\n");
    printf("  +============================+\n");
    printf("  | 1. 开户                    |\n");
    printf("  | 2. 存款                    |\n");
    printf("  | 3. 取款                    |\n");
    printf("  | 4. 转账                    |\n");
    printf("  | 5. 查询余额                |\n");
    printf("  | 6. 列出所有账户            |\n");
    printf("  | 7. 交易记录                |\n");
    printf("  | 0. 退出                    |\n");
    printf("  +============================+\n");
    printf("  请选择: ");
}

/* ============================================================
 * 主函数
 * ============================================================ */
int main(void)
{
    int choice;
    int id1, id2, id3;

    printf("=== ATM动态库版初始化 ===\n");

    /* 下面这些函数都来自 account.dll，调用方式与静态库版完全一致 */
    id1 = account_create("张三", 1000.0);
    id2 = account_create("李四", 2000.0);
    id3 = account_create("王五", 500.0);

    /* 演示几笔交易 */
    transaction_deposit(id1, 500.0);
    transaction_withdraw(id2, 200.0);
    transaction_transfer(id1, id3, 300.0);

    printf("=== 初始化完成 ===\n");

    while (1) {
        show_menu();
        if (scanf("%d", &choice) != 1)
            break;

        switch (choice) {
        case 1: {
            char name[MAX_NAME_LEN];
            double balance;
            printf("输入户名: ");
            scanf("%49s", name);
            printf("输入初始余额: ");
            scanf("%lf", &balance);
            account_create(name, balance);
            break;
        }
        case 2: {
            int id; double amt;
            printf("输入账户ID: ");
            scanf("%d", &id);
            printf("输入存款金额: ");
            scanf("%lf", &amt);
            transaction_deposit(id, amt);
            break;
        }
        case 3: {
            int id; double amt;
            printf("输入账户ID: ");
            scanf("%d", &id);
            printf("输入取款金额: ");
            scanf("%lf", &amt);
            transaction_withdraw(id, amt);
            break;
        }
        case 4: {
            int from, to; double amt;
            printf("输入转出账户ID: ");
            scanf("%d", &from);
            printf("输入转入账户ID: ");
            scanf("%d", &to);
            printf("输入转账金额: ");
            scanf("%lf", &amt);
            transaction_transfer(from, to, amt);
            break;
        }
        case 5: {
            int id;
            printf("输入账户ID: ");
            scanf("%d", &id);
            printf("余额: %.2f\n", account_get_balance(id));
            break;
        }
        case 6:
            account_list_all();
            break;
        case 7: {
            int id;
            printf("输入账户ID: ");
            scanf("%d", &id);
            transaction_print_history(id);
            break;
        }
        case 0:
            printf("感谢使用ATM动态库版，再见！\n");
            return 0;
        default:
            printf("无效选择，请重试\n");
        }
    }

    return 0;
}
