/**
 * main.c - ATM主程序
 * 第9讲：静态库
 *
 * 主程序只需要 #include 头文件，不需要自己实现账户和交易功能。
 * 编译链接时用 -L. -laccount 指定静态库，链接器会从
 * libaccount.a 中复制需要的代码到最终可执行文件。
 *
 * 编译流程：
 *   1. gcc -c account.c       -> account.o
 *   2. gcc -c transaction.c   -> transaction.o
 *   3. ar rcs libaccount.a account.o transaction.o
 *   4. gcc -c main.c          -> main.o
 *   5. gcc -o atm_static main.o -L. -laccount   (链接静态库)
 */
#include "account.h"
#include "transaction.h"
#include <stdio.h>
#include <stdlib.h>

/* 显示菜单 */
static void show_menu(void)
{
    printf("\n");
    printf("  +============================+\n");
    printf("  |     ATM 银行系统           |\n");
    printf("  |    (静态库版本)            |\n");
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

int main(void)
{
    int choice;

    /* 初始化测试数据 */
    printf("=== ATM静态库版初始化 ===\n");
    int id1 = account_create("张三", 1000.0);
    int id2 = account_create("李四", 2000.0);
    int id3 = account_create("王五", 500.0);

    /* 演示几笔交易 */
    transaction_deposit(id1, 500.0);
    transaction_withdraw(id2, 200.0);
    transaction_transfer(id1, id3, 300.0);
    printf("=== 初始化完成 ===\n");

    /* 主循环 */
    while (1) {
        show_menu();
        if (scanf("%d", &choice) != 1)
            break;

        switch (choice) {
        case 1: {
            char name[MAX_NAME_LEN];
            double balance;
            printf("输入户名: ");
            scanf("%s", name);
            printf("输入初始余额: ");
            scanf("%lf", &balance);
            account_create(name, balance);
            break;
        }
        case 2: {
            int id;
            double amt;
            printf("输入账户ID: ");
            scanf("%d", &id);
            printf("输入存款金额: ");
            scanf("%lf", &amt);
            transaction_deposit(id, amt);
            break;
        }
        case 3: {
            int id;
            double amt;
            printf("输入账户ID: ");
            scanf("%d", &id);
            printf("输入取款金额: ");
            scanf("%lf", &amt);
            transaction_withdraw(id, amt);
            break;
        }
        case 4: {
            int from, to;
            double amt;
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
            printf("感谢使用ATM静态库版，再见！\n");
            return 0;
        default:
            printf("无效选择，请重试\n");
        }
    }

    return 0;
}
