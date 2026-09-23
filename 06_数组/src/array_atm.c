/*
 * ============================================================
 *  第6讲：数组 —— 批量数据的存储和操作
 *  ATM 数组化版本：从"单变量"到"批量管理"
 * ============================================================
 *
 *  目标：用数组管理 ATM 的交易记录和多账户
 *
 *  第5讲的成果：
 *    用指针解决了全局变量问题，balance 通过指针传递
 *    但——只能管理一个账户、只记住当前一笔交易
 *
 *  第6讲的进步：
 *    1. 用数组存储最近 10 笔交易记录（金额 + 类型）
 *    2. 用数组存储多个账户（ID + 名称 + 余额）
 *    3. 用字符数组存储账户名（字符串）
 *    4. 用 for 循环遍历数组（衔接第2讲的循环）
 *    5. 用指针操作数组（衔接第5讲的指针）
 *
 *  对比前几讲：
 *    第3讲：double g_balance = 1000.0;      // 一个全局余额
 *    第5讲：void deposit(double* balance);    // 指针传余额
 *    第6讲：double balances[5];               // 数组管理多账户余额
 *           double trans[10];                 // 数组存交易记录
 *
 *  编译运行：
 *    gcc -o array_atm array_atm.c && ./array_atm
 * ============================================================
 */

#include <stdio.h>
#include <string.h>

/* ============================================================
 *  常量定义
 * ============================================================
 *  用 #define 定义常量，方便统一修改大小
 *  这也是"魔法数字"的最佳实践——不要在代码里到处写 10、5
 */
#define MAX_TRANSACTIONS 10    /* 最多记录 10 笔交易 */
#define MAX_ACCOUNTS     5     /* 最多管理 5 个账户   */
#define NAME_LEN          20   /* 账户名最大长度      */

/* 交易类型常量 */
#define TRANS_DEPOSIT  1    /* 存款 */
#define TRANS_WITHDRAW 2   /* 取款 */
#define TRANS_TRANSFER 3   /* 转账 */

/* ============================================================
 *  数组定义 —— 批量数据的存储
 * ============================================================
 *
 *  【对比】前几讲只有单个变量：
 *    double g_balance = 1000.0;   // 一个余额
 *    char* account_name = "张三";  // 一个名字
 *
 *  【现在】用数组管理多个数据：
 *    多个账户的 ID、名称、余额分别存入三个平行数组
 *    交易记录也用数组存储，最多 10 笔
 *
 *  【为什么用"平行数组"？】
 *    我们还没学结构体（第7讲），所以用多个数组分别存储
 *    同一索引对应的账户信息：ids[i]、names[i]、balances[i]
 *    学了结构体后，可以合并成一个结构体数组（第7讲预告）
 */

/* 多账户数据（平行数组） */
int    account_ids[MAX_ACCOUNTS]       = {1001, 1002, 1003, 1004, 1005};
char   account_names[MAX_ACCOUNTS][NAME_LEN] = {"张三", "李四", "王五", "赵六", "钱七"};
double account_balances[MAX_ACCOUNTS]  = {1000.0, 2000.0, 500.0, 3000.0, 1500.0};

/*
 * 交易记录数组（循环缓冲区）
 *
 * 【对比】前几讲：每次交易后只打印一下，关掉程序就没了
 * 【现在】用数组把最近 10 笔交易存下来，随时可以查看
 *
 * trans_amounts[10]  —— 每笔交易的金额
 * trans_types[10]    —— 每笔交易的类型（存/取/转）
 *
 * 用 trans_count 记录已存了多少笔（超过 10 就循环覆盖最早的）
 */
double trans_amounts[MAX_TRANSACTIONS];  /* 交易金额数组 */
int    trans_types[MAX_TRANSACTIONS];    /* 交易类型数组 */
int    trans_count = 0;                   /* 已记录的交易总数 */

/* 当前操作的账户索引（0 ~ MAX_ACCOUNTS-1） */
int current_account = 0;

/* ============================================================
 *  函数声明
 * ============================================================
 */
void show_welcome(void);
void show_menu(void);
int  select_account(void);
int  find_account_by_id(int id);
void query_balance(void);
void deposit(void);
void withdraw(void);
void transfer(void);
void add_transaction(double amount, int type);
void show_transactions(void);
void show_all_accounts(void);
void print_success(const char* op, double amount);
void print_error(const char* msg);
const char* trans_type_name(int type);

/* ============================================================
 *  主函数
 * ============================================================ */
int main(void)
{
    int choice = 0;
    int running = 1;

    show_welcome();

    /* 选择账户（多账户管理） */
    current_account = select_account();
    if (current_account < 0) {
        printf("未找到账户，程序退出。\n");
        return 1;
    }

    while (running)
    {
        show_menu();
        printf("请输入您的选择：");
        scanf("%d", &choice);
        printf("\n");

        switch (choice)
        {
            case 1:
                query_balance();
                break;
            case 2:
                deposit();
                break;
            case 3:
                withdraw();
                break;
            case 4:
                transfer();
                break;
            case 5:
                show_transactions();
                break;
            case 6:
                show_all_accounts();
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

/* ============================================================
 *  函数定义
 * ============================================================ */

/* ---------- show_welcome：显示欢迎界面 ---------- */
void show_welcome(void)
{
    printf("========================================\n");
    printf("     欢迎使用 CCIT ATM 系统（数组版）\n");
    printf("========================================\n");
    printf("  支持 %d 个账户 | 记录最近 %d 笔交易\n",
           MAX_ACCOUNTS, MAX_TRANSACTIONS);
    printf("\n");
}

/* ---------- show_menu：显示主菜单 ---------- */
void show_menu(void)
{
    printf("\n-------- 主菜单 --------\n");
    printf("  1. 查询余额\n");
    printf("  2. 存款\n");
    printf("  3. 取款\n");
    printf("  4. 转账\n");
    printf("  5. 查看交易记录\n");     /* 新功能：查看历史 */
    printf("  6. 查看所有账户\n");     /* 新功能：多账户管理 */
    printf("  0. 退出\n");
    printf("------------------------\n");
}

/* ---------- select_account：选择账户 ---------- */
/*
 * 【对比】前几讲：只有一个账户，不需要选择
 * 【现在】有多个账户，需要让用户选择操作哪个
 *
 * 遍历数组展示所有账户，用户输入 ID 选择
 * 返回账户在数组中的索引（找不到返回 -1）
 */
int select_account(void)
{
    int input_id = 0;

    printf("【选择账户】\n");
    printf("可用账户列表：\n");

    /*
     * 用 for 循环遍历数组（衔接第2讲的循环！）
     * i 从 0 到 MAX_ACCOUNTS-1，逐个访问数组元素
     */
    for (int i = 0; i < MAX_ACCOUNTS; i++)
    {
        printf("  账户ID: %d  姓名: %s  余额: %.2f\n",
               account_ids[i], account_names[i], account_balances[i]);
    }

    printf("\n请输入您的账户ID：");
    scanf("%d", &input_id);

    /* 调用查找函数 */
    int idx = find_account_by_id(input_id);
    if (idx >= 0)
    {
        printf("✅ 登录成功！欢迎，%s\n\n", account_names[idx]);
    }
    else
    {
        print_error("账户ID不存在！");
    }

    return idx;
}

/* ---------- find_account_by_id：按ID查找账户 ---------- */
/*
 * 遍历数组查找匹配的 ID
 * 返回找到的索引，找不到返回 -1
 *
 * 【知识点】线性查找：最简单的数组搜索算法
 * 逐个比较，找到就返回；全部比较完都没找到，返回 -1
 */
int find_account_by_id(int id)
{
    for (int i = 0; i < MAX_ACCOUNTS; i++)
    {
        if (account_ids[i] == id)
        {
            return i;  /* 找到了，返回索引 */
        }
    }
    return -1;  /* 全部找完都没找到 */
}

/* ---------- query_balance：查询余额 ---------- */
void query_balance(void)
{
    printf("【查询余额】\n");
    printf("账户名：%s\n", account_names[current_account]);
    printf("您当前的账户余额为：%.2f 元\n",
           account_balances[current_account]);
}

/* ---------- deposit：存款 ---------- */
void deposit(void)
{
    double amount = 0.0;

    printf("【存款业务】\n");
    printf("请输入存款金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("存款金额必须大于0！");
        return;
    }

    /*
     * 【对比】前几讲：g_balance = g_balance + amount;
     * 【现在】用数组索引操作对应账户的余额
     */
    account_balances[current_account] += amount;

    /* 记录这笔交易到数组 */
    add_transaction(amount, TRANS_DEPOSIT);

    print_success("存入", amount);
}

/* ---------- withdraw：取款 ---------- */
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

    if (amount > account_balances[current_account])
    {
        print_error("余额不足！");
        return;
    }

    account_balances[current_account] -= amount;

    /* 记录这笔交易到数组 */
    add_transaction(amount, TRANS_WITHDRAW);

    print_success("取出", amount);
}

/* ---------- transfer：转账 ---------- */
void transfer(void)
{
    double amount = 0.0;
    int target_id = 0;

    printf("【转账业务】\n");
    printf("请输入转账金额：");
    scanf("%lf", &amount);

    if (amount <= 0)
    {
        print_error("转账金额必须大于0！");
        return;
    }

    if (amount > account_balances[current_account])
    {
        print_error("余额不足，无法转账！");
        return;
    }

    printf("请输入对方账户ID：");
    scanf("%d", &target_id);

    int target_idx = find_account_by_id(target_id);
    if (target_idx < 0)
    {
        print_error("对方账户不存在！");
        return;
    }

    if (target_idx == current_account)
    {
        print_error("不能给自己转账！");
        return;
    }

    /* 扣减当前账户，增加目标账户 */
    account_balances[current_account] -= amount;
    account_balances[target_idx] += amount;

    /* 记录这笔交易到数组 */
    add_transaction(amount, TRANS_TRANSFER);

    printf("✅ 转账成功！向 %s 转出 %.2f 元\n",
           account_names[target_idx], amount);
    printf("当前余额：%.2f 元\n",
           account_balances[current_account]);
}

/* ---------- add_transaction：记录交易到数组 ---------- */
/*
 * 把一笔交易存入 trans_amounts 和 trans_types 数组
 *
 * 【知识点】循环缓冲区（Circular Buffer）
 * 当交易超过 10 笔时，新的会覆盖最旧的
 * 用取模运算 % 实现循环：trans_count % MAX_TRANSACTIONS
 *
 * 【对比】前几讲：交易完就忘了，查不到历史
 * 【现在】用数组保存历史，随时可以回顾
 */
void add_transaction(double amount, int type)
{
    int slot = trans_count % MAX_TRANSACTIONS;  /* 循环取模 */
    trans_amounts[slot] = amount;
    trans_types[slot]   = type;
    trans_count++;
}

/* ---------- show_transactions：查看交易记录 ---------- */
/*
 * 【核心】用 for 循环遍历数组，展示交易历史
 *
 * 两种情况：
 *   1. 交易总数 <= 10：从第 0 笔遍历到第 trans_count-1 笔
 *   2. 交易总数 > 10：最早的交易在 trans_count % 10 的位置
 *      需要从那个位置开始，遍历 10 笔
 *
 * 【知识点】数组遍历 + 取模运算 = 循环缓冲区读取
 */
void show_transactions(void)
{
    printf("【交易记录】（最近 %d 笔）\n", MAX_TRANSACTIONS);

    /* 实际需要显示的记录数 */
    int display_count = (trans_count < MAX_TRANSACTIONS)
                        ? trans_count : MAX_TRANSACTIONS;

    if (display_count == 0)
    {
        printf("暂无交易记录。\n");
        return;
    }

    /* 最早交易的起始位置（循环缓冲区） */
    int start = (trans_count <= MAX_TRANSACTIONS)
                ? 0 : (trans_count % MAX_TRANSACTIONS);

    /*
     * 用 for 循环遍历交易数组
     * 【衔接第2讲】for 循环 + 数组 = 天作之合
     * 【衔接第5讲】用指针遍历：*(trans_amounts + idx)
     */
    printf("%-6s %-10s %-8s\n", "序号", "类型", "金额");
    printf("------------------------------\n");

    for (int i = 0; i < display_count; i++)
    {
        int idx = (start + i) % MAX_TRANSACTIONS;  /* 循环索引 */

        /*
         * 【指针操作数组】衔接第5讲
         * trans_amounts[idx] 等价于 *(trans_amounts + idx)
         * 数组名就是首元素地址，加偏移量就是对应元素地址
         */
        double amt = *(trans_amounts + idx);  /* 指针方式访问 */
        int   typ = *(trans_types + idx);    /* 指针方式访问 */

        printf("%-6d %-10s %-8.2f\n",
               i + 1, trans_type_name(typ), amt);
    }
}

/* ---------- show_all_accounts：查看所有账户 ---------- */
/*
 * 用指针遍历数组，展示所有账户信息
 *
 * 【衔接第5讲指针】演示指针遍历数组的两种写法：
 *   写法1：用数组下标 account_balances[i]
 *   写法2：用指针 *(p + i)
 *
 * 【知识点】数组名就是首元素地址
 *   account_ids 就是 &account_ids[0]
 *   account_ids + i 就是 &account_ids[i]
 *   *(account_ids + i) 就是 account_ids[i]
 */
void show_all_accounts(void)
{
    printf("【所有账户信息】\n");
    printf("%-8s %-8s %-12s\n", "账户ID", "姓名", "余额");
    printf("------------------------------------\n");

    /*
     * 指针遍历法：用指针变量指向数组首元素，然后递增
     *
     * 【衔接第5讲】指针 + 数组的关系
     *   p 指向数组首元素
     *   p++ 让指针前进一步，指向下一个元素
     *   步长自动适应类型（int 步长4字节，double 步长8字节）
     */
    int    *pid = account_ids;          /* 指向 ids 数组首元素 */
    char   (*pname)[NAME_LEN] = account_names;  /* 指向 names 数组首元素 */
    double *pbal = account_balances;    /* 指向 balances 数组首元素 */

    for (int i = 0; i < MAX_ACCOUNTS; i++)
    {
        /*
         * 两种访问方式对比：
         *   数组下标法：account_ids[i]
         *   指针偏移法：*(pid + i)  或  pid[i]
         *   指针递增法：*pid++（每次循环后指针前进一步）
         */
        printf("%-8d %-8s %-12.2f\n",
               *pid, *pname, *pbal);

        /* 指针递增，指向下一个元素 */
        pid++;
        pbal++;
        pname++;
    }

    /*
     * 【知识点】数组名 vs 指针的区别（思考题1预告）
     *   sizeof(account_ids)  = 20（整个数组的大小 5*4）
     *   sizeof(int*)         = 4 或 8（指针本身的大小）
     *   数组名不能自增（account_ids++ 会报错），指针可以
     */
    printf("\n数组总大小：%d 字节（%d 个 int × %d 字节）\n",
           (int)sizeof(account_ids),
           MAX_ACCOUNTS,
           (int)sizeof(int));
}

/* ---------- trans_type_name：交易类型转中文名 ---------- */
/*
 * 返回交易类型的中文名称字符串
 * 用 switch 返回静态字符串，方便格式化输出
 */
const char* trans_type_name(int type)
{
    switch (type)
    {
        case TRANS_DEPOSIT:  return "存款";
        case TRANS_WITHDRAW: return "取款";
        case TRANS_TRANSFER: return "转账";
        default:             return "未知";
    }
}

/* ---------- print_success：打印成功信息 ---------- */
void print_success(const char* op, double amount)
{
    printf("✅ 操作成功！%s %.2f 元\n", op, amount);
    printf("当前余额：%.2f 元\n",
           account_balances[current_account]);
}

/* ---------- print_error：打印错误信息 ---------- */
void print_error(const char* msg)
{
    printf("❌ %s\n", msg);
}

/*
 * ============================================================
 *  对比前几讲，我们收获了什么？
 * ============================================================
 *
 *  ✅ 1. 批量数据管理
 *     原来：一个 balance 变量，只管一个账户
 *     现在：account_balances[5]，同时管理 5 个账户
 *
 *  ✅ 2. 交易历史可追溯
 *     原来：交易完就忘了，关掉程序什么都没留下
 *     现在：trans_amounts[10] + trans_types[10]，记住最近10笔
 *
 *  ✅ 3. 字符串有了"容器"
 *     原来：没有账户名的概念（只有一个数字 ID）
 *     现在：account_names[5][20] 字符数组，每个账户有名字
 *
 *  ✅ 4. for 循环有了用武之地
 *     原来：for 循环主要用来打印菜单和计数
 *     现在：for 循环遍历数组——这才是 for 循环的主场！
 *
 *  ✅ 5. 指针和数组无缝衔接
 *     原来：指针主要用来传变量的地址
 *     现在：指针遍历数组，数组名就是指针，两者完美结合
 *
 * ============================================================
 *  思考：还有问题吗？
 * ============================================================
 *
 *  ❓ 1. 平行数组太散了
 *     ids、names、balances 三个数组，改一个要同步改三个
 *     （下一讲：结构体把相关数据打包到一起）
 *
 *  ❓ 2. 数组大小是固定的
 *     MAX_ACCOUNTS=5，想加第6个账户？改代码重新编译
 *     （第8讲：链表 + 动态内存，大小随时变）
 *
 *  ❓ 3. 没有越界保护
 *     如果访问 account_balances[100]？C语言不会报错，但会读乱码
 *     （这就是为什么数组越界是经典 bug 来源）
 *
 *  ❓ 4. 交易记录只存金额和类型
 *     想存时间、对方账户？平行数组会越来越乱
 *     （结构体 + 链表 = 完美方案）
 *
 *  💡 数组是从"单变量"到"数据结构"的第一步
 *     它解决了批量存储的问题，但带来了固定大小的局限
 *     这正是下一讲结构体、再下一讲链表的演进动力
 *
 * ============================================================
 */
