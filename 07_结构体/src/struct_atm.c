/*
 * ============================================================
 *  第7讲：结构体 —— 把相关数据打包到一起
 *  ATM 结构体版本：从"平行数组"到"数据封装"
 * ============================================================
 *
 *  目标：用结构体把账户信息打包在一起，演示数据封装思想
 *
 *  第6讲的成果：
 *    用数组管理了 5 个账户和 10 笔交易记录
 *    但——用了三个"平行数组"，改一个要同步改三个
 *
 *  第7讲的进步：
 *    1. 用结构体把账户信息（ID + 姓名 + 余额）打包成一个整体
 *    2. 用结构体把交易记录（类型 + 金额 + 对方账户）打包
 *    3. 用 typedef 给结构体起"短名字"
 *    4. 用结构体数组替代平行数组
 *    5. 用结构体指针操作（衔接第5讲指针）
 *    6. 演示结构体作函数参数：值传递 vs 指针传递
 *
 *  对比前几讲：
 *    第6讲：int ids[5]; char names[5][20]; double balances[5];  // 平行数组
 *    第7讲：Account accounts[5];  // 结构体数组，一个搞定！
 *
 *  数据封装思想：
 *    结构体 = 数据打包（把相关数据绑在一起）
 *    函数   = 行为打包（把操作逻辑绑在一起）
 *    两者结合 → 面向对象编程的雏形（类 = 数据 + 行为）
 *
 *  编译运行：
 *    gcc -Wall -o struct_atm struct_atm.c && ./struct_atm
 * ============================================================
 */

#include <stdio.h>
#include <string.h>

/* ============================================================
 *  常量定义
 * ============================================================
 *  与第6讲一样，用 #define 定义常量，避免"魔法数字"
 */
#define MAX_TRANSACTIONS 10    /* 最多记录 10 笔交易 */
#define MAX_ACCOUNTS     5     /* 最多管理 5 个账户   */
#define NAME_LEN          20   /* 账户名最大长度      */

/* ============================================================
 *  结构体定义 —— 数据封装的核心
 * ============================================================
 *
 *  【对比第6讲】第6讲用三个"平行数组"分别存储账户信息：
 *    int    account_ids[5];        // 账户ID
 *    char   account_names[5][20];  // 账户姓名
 *    double account_balances[5];  // 账户余额
 *
 *  三个数组通过"同一个索引"关联：ids[i]、names[i]、balances[i]
 *  痛点：改一个要同步改三个，一不小心就忘了，数据对不上
 *
 *  【第7讲】用结构体把三个字段打包成一个整体：
 *    struct Account {
 *        int    id;          // 账户ID
 *        char   name[20];    // 账户姓名
 *        double balance;     // 账户余额
 *    };
 *
 *  一个结构体 = 一张名片，上面印着这个账户的所有信息
 *  结构体数组 = 一盒名片，整齐排列，不会散落
 */

/* ---------- 账户结构体 ---------- */
/*
 * 【知识点】struct 关键字
 *   struct 是 C 语言的关键字，用来定义"自定义类型"
 *   花括号里的变量叫"成员"（member），也叫"字段"（field）
 *
 * 【比喻】结构体就像一张名片
 *   名片上有：姓名、电话、邮箱 —— 它们是一个整体
 *   结构体有：ID、姓名、余额 —— 它们也是一个整体
 */
struct Account {
    int    id;              /* 账户ID           */
    char   name[NAME_LEN];  /* 账户姓名（字符数组）*/
    double balance;          /* 账户余额          */
};

/* ---------- 交易记录结构体 ---------- */
/*
 * 【对比第6讲】第6讲的交易记录也是平行数组：
 *    double trans_amounts[10];  // 金额
 *    int    trans_types[10];    // 类型
 *
 * 【第7讲】用结构体把交易信息打包：
 *    type（类型字符串）+ amount（金额）+ target_account（对方账户）
 *
 * 新增了 target_account 字段，记录转账时的对方账户
 * 平行数组想加字段要再加一个数组，结构体只要加一个成员
 */
struct Transaction {
    char   type[10];        /* 交易类型："存款"/"取款"/"转账" */
    double amount;          /* 交易金额                       */
    int    target_account;  /* 对方账户ID（转账用，0表示无）   */
};

/* ============================================================
 *  typedef 类型重定义 —— 给结构体起"短名字"
 * ============================================================
 *
 *  【没有 typedef】每次使用都要写 struct：
 *    struct Account acc1;           // 声明变量时要加 struct
 *    void func(struct Account* p);  // 函数参数也要加 struct
 *
 *  【有 typedef】起个短名字，用起来更简洁：
 *    typedef struct Account Account;
 *    Account acc1;                  // 不用加 struct 了！
 *    void func(Account* p);        // 更简洁
 *
 *  【原理】typedef 不是创建新类型，只是给已有类型起"别名"
 *    就像"张三"可以叫"老张"——人还是那个人，名字短了
 *
 *  【更简洁的写法】定义结构体的同时 typedef：
 *    typedef struct {
 *        int id;
 *        char name[20];
 *        double balance;
 *    } Account;
 *  但这种写法不能在结构体内部自引用（如链表节点需要指向自己）
 *  所以链表等场景还是用"先 struct 再 typedef"的方式
 */
typedef struct Account Account;              /* 账户类型短名 */
typedef struct Transaction Transaction;      /* 交易类型短名 */

/* ============================================================
 *  全局数据 —— 结构体数组
 * ============================================================
 *
 *  【对比第6讲】第6讲的平行数组：
 *    int    account_ids[5]       = {1001, 1002, ...};
 *    char   account_names[5][20] = {"张三", "李四", ...};
 *    double account_balances[5]  = {1000.0, 2000.0, ...};
 *    // 三个数组，三组初始化，改一处要同步改三处
 *
 *  【第7讲】结构体数组，初始化更清晰：
 *    Account accounts[5] = {
 *        {1001, "张三", 1000.0},   // 第0个账户的所有信息
 *        {1002, "李四", 2000.0},   // 第1个账户的所有信息
 *        ...
 *    };
 *    // 一个数组，每行是一个账户的完整信息，一目了然
 */

/* 多账户数据（结构体数组） */
Account accounts[MAX_ACCOUNTS] = {
    {1001, "张三", 1000.0},
    {1002, "李四", 2000.0},
    {1003, "王五", 500.0},
    {1004, "赵六", 3000.0},
    {1005, "钱七", 1500.0}
};

/* 交易记录数组（结构体数组 + 循环缓冲区） */
Transaction transactions[MAX_TRANSACTIONS];
int trans_count = 0;    /* 已记录的交易总数 */

/* 当前操作的账户索引（0 ~ MAX_ACCOUNTS-1） */
int current_account = 0;

/* ============================================================
 *  函数声明
 * ============================================================
 *
 *  【知识点】结构体作为函数参数有两种方式：
 *
 *  方式1：值传递（复制整个结构体）
 *    void print_account(Account acc);
 *    // 把整个结构体复制一份传进去，函数内修改不影响原数据
 *    // 结构体大时浪费内存和时间（要复制所有成员）
 *
 *  方式2：指针传递（只传地址）
 *    void deposit(Account* pAcc, double amount);
 *    // 只传结构体的地址（4或8字节），函数内可以修改原数据
 *    // 高效！这也是第5讲指针的核心应用
 *
 *  【选择原则】
 *    只读不改 → 可以值传递（小结构体）或 const 指针（大结构体）
 *    需要修改 → 必须用指针传递
 */
void show_welcome(void);
void show_menu(void);
int  select_account(void);
int  find_account_by_id(int id);
void query_balance(void);
void deposit(void);
void withdraw(void);
void transfer(void);
void add_transaction(const char* type, double amount, int target);
void show_transactions(void);
void show_all_accounts(void);
void print_account_value(Account acc);         /* 值传递演示 */
void print_account_ptr(const Account* p);      /* 指针传递演示 */
void print_success(const char* op, double amount);
void print_error(const char* msg);

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
    printf("   欢迎使用 CCIT ATM 系统（结构体版）\n");
    printf("========================================\n");
    printf("  支持 %d 个账户 | 记录最近 %d 笔交易\n",
           MAX_ACCOUNTS, MAX_TRANSACTIONS);
    printf("  数据封装：账户信息打包为结构体\n");
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
    printf("  5. 查看交易记录\n");
    printf("  6. 查看所有账户\n");
    printf("  0. 退出\n");
    printf("------------------------\n");
}

/* ---------- select_account：选择账户 ---------- */
/*
 * 遍历结构体数组展示所有账户，用户输入 ID 选择
 * 返回账户在数组中的索引（找不到返回 -1）
 *
 * 【对比第6讲】第6讲要同时遍历三个平行数组：
 *    printf("ID: %d  姓名: %s  余额: %.2f",
 *           account_ids[i], account_names[i], account_balances[i]);
 *
 * 【第7讲】只需访问一个结构体数组的成员：
 *    printf("ID: %d  姓名: %s  余额: %.2f",
 *           accounts[i].id, accounts[i].name, accounts[i].balance);
 *
 * 【知识点】结构体成员访问（点号 .）
 *    用 变量名.成员名 访问结构体的成员
 *    accounts[i].id      → 第i个账户的ID
 *    accounts[i].name    → 第i个账户的姓名
 *    accounts[i].balance → 第i个账户的余额
 */
int select_account(void)
{
    int input_id = 0;

    printf("【选择账户】\n");
    printf("可用账户列表：\n");

    /*
     * 遍历结构体数组
     * 【对比】第6讲：三个数组 ids[i]、names[i]、balances[i]
     * 【现在】一个结构体 accounts[i].id、.name、.balance
     */
    for (int i = 0; i < MAX_ACCOUNTS; i++)
    {
        printf("  账户ID: %d  姓名: %s  余额: %.2f\n",
               accounts[i].id, accounts[i].name, accounts[i].balance);
    }

    printf("\n请输入您的账户ID：");
    scanf("%d", &input_id);

    /* 调用查找函数 */
    int idx = find_account_by_id(input_id);
    if (idx >= 0)
    {
        printf("登录成功！欢迎，%s\n\n", accounts[idx].name);
    }
    else
    {
        print_error("账户ID不存在！");
    }

    return idx;
}

/* ---------- find_account_by_id：按ID查找账户 ---------- */
/*
 * 遍历结构体数组查找匹配的 ID
 * 返回找到的索引，找不到返回 -1
 *
 * 【知识点】结构体成员访问
 *    accounts[i].id 就是访问第i个结构体的id成员
 *    这比平行数组的 account_ids[i] 更直观——数据属于同一个账户
 */
int find_account_by_id(int id)
{
    for (int i = 0; i < MAX_ACCOUNTS; i++)
    {
        if (accounts[i].id == id)
        {
            return i;  /* 找到了，返回索引 */
        }
    }
    return -1;  /* 全部找完都没找到 */
}

/* ---------- query_balance：查询余额 ---------- */
/*
 * 【对比第6讲】第6讲：account_balances[current_account]
 * 【第7讲】accounts[current_account].balance
 *
 * 【知识点】. 运算符的优先级高于 &
 *    &accounts[i].balance 等价于 &(accounts[i].balance)
 *    先取成员，再取地址
 */
void query_balance(void)
{
    printf("【查询余额】\n");
    printf("账户名：%s\n", accounts[current_account].name);
    printf("您当前的账户余额为：%.2f 元\n",
           accounts[current_account].balance);
}

/* ---------- deposit：存款 ---------- */
/*
 * 存款操作：修改结构体成员
 *
 * 【对比第6讲】第6讲：account_balances[current_account] += amount;
 * 【第7讲】accounts[current_account].balance += amount;
 *
 * 【知识点】结构体成员可以被赋值/修改
 *    accounts[i].balance = 999.0;     // 直接赋值
 *    accounts[i].balance += 100.0;    // 复合赋值
 *    strcpy(accounts[i].name, "新名"); // 修改字符数组成员
 */
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

    /* 通过结构体成员访问修改余额 */
    accounts[current_account].balance += amount;

    /* 记录这笔交易 */
    add_transaction("存款", amount, 0);

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

    if (amount > accounts[current_account].balance)
    {
        print_error("余额不足！");
        return;
    }

    accounts[current_account].balance -= amount;

    add_transaction("取款", amount, 0);

    print_success("取出", amount);
}

/* ---------- transfer：转账 ---------- */
/*
 * 转账操作：同时修改两个结构体的余额
 *
 * 【对比第6讲】第6讲要同时操作两个平行数组：
 *    account_balances[current_account] -= amount;
 *    account_balances[target_idx] += amount;
 *
 * 【第7讲】操作两个结构体成员：
 *    accounts[current_account].balance -= amount;
 *    accounts[target_idx].balance += amount;
 *
 * 数据属于同一个账户，修改时不会"改错数组"
 */
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

    if (amount > accounts[current_account].balance)
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

    /* 扣减当前账户，增加目标账户——操作结构体成员 */
    accounts[current_account].balance -= amount;
    accounts[target_idx].balance += amount;

    /* 记录交易，包含对方账户ID */
    add_transaction("转账", amount, accounts[target_idx].id);

    printf("转账成功！向 %s 转出 %.2f 元\n",
           accounts[target_idx].name, amount);
    printf("当前余额：%.2f 元\n",
           accounts[current_account].balance);
}

/* ---------- add_transaction：记录交易到结构体数组 ---------- */
/*
 * 把一笔交易存入 Transaction 结构体数组
 *
 * 【对比第6讲】第6讲要同时写两个数组：
 *    trans_amounts[slot] = amount;
 *    trans_types[slot]   = type;
 *
 * 【第7讲】一次操作一个结构体的所有成员：
 *    strcpy(transactions[slot].type, type);     // 写类型
 *    transactions[slot].amount = amount;         // 写金额
 *    transactions[slot].target_account = target; // 写对方账户
 *
 * 结构体把相关数据绑在一起，写入时不会漏掉某个字段
 */
void add_transaction(const char* type, double amount, int target)
{
    int slot = trans_count % MAX_TRANSACTIONS;  /* 循环取模 */

    /*
     * 给结构体成员逐一赋值
     * 【知识点】strcpy 用于给字符数组成员赋值（不能用 = 赋值字符串）
     */
    strcpy(transactions[slot].type, type);
    transactions[slot].amount = amount;
    transactions[slot].target_account = target;

    trans_count++;
}

/* ---------- show_transactions：查看交易记录 ---------- */
/*
 * 遍历 Transaction 结构体数组，展示交易历史
 *
 * 【对比第6讲】第6讲从两个平行数组分别读取：
 *    double amt = trans_amounts[idx];
 *    int   typ = trans_types[idx];
 *    printf("%s %.2f", trans_type_name(typ), amt);
 *
 * 【第7讲】从一个结构体读取所有信息：
 *    printf("%s %.2f", transactions[idx].type, transactions[idx].amount);
 *    if (transactions[idx].target_account > 0)
 *        printf(" -> 账户%d", transactions[idx].target_account);
 *
 * 结构体让交易记录的信息更丰富，也更容易管理
 */
void show_transactions(void)
{
    printf("【交易记录】（最近 %d 笔）\n", MAX_TRANSACTIONS);

    int display_count = (trans_count < MAX_TRANSACTIONS)
                        ? trans_count : MAX_TRANSACTIONS;

    if (display_count == 0)
    {
        printf("暂无交易记录。\n");
        return;
    }

    int start = (trans_count <= MAX_TRANSACTIONS)
                ? 0 : (trans_count % MAX_TRANSACTIONS);

    printf("%-6s %-8s %-10s %-12s\n", "序号", "类型", "金额", "对方账户");
    printf("------------------------------------------\n");

    for (int i = 0; i < display_count; i++)
    {
        int idx = (start + i) % MAX_TRANSACTIONS;

        /*
         * 从结构体读取交易信息
         * 【知识点】. 运算符访问结构体成员
         */
        printf("%-6d %-8s %-10.2f",
               i + 1,
               transactions[idx].type,
               transactions[idx].amount);

        /* 如果有对方账户（转账），显示对方ID */
        if (transactions[idx].target_account > 0)
        {
            printf(" -> %d", transactions[idx].target_account);
        }
        printf("\n");
    }
}

/* ---------- show_all_accounts：查看所有账户 ---------- */
/*
 * 【核心知识点】用结构体指针遍历结构体数组
 *
 * 【衔接第5讲指针】
 *    第5讲：用指针遍历 int 数组  → int* p = arr; p++; *p
 *    第7讲：用指针遍历结构体数组 → Account* p = accounts; p++; (*p).id
 *
 * 【知识点】-> 运算符（箭头运算符）
 *    当用指针访问结构体成员时，有两种等价写法：
 *      写法1：(*p).id      ← 先解引用，再用 . 访问成员
 *      写法2：p->id        ← 箭头运算符，等价于 (*p).id，更简洁
 *
 *    【记忆口诀】
 *      变量用点（.）   →  acc.id
 *      指针用箭头（->） →  p->id
 *
 * 【对比第6讲】第6讲用三个指针分别遍历三个平行数组：
 *    int    *pid  = account_ids;
 *    double *pbal = account_balances;
 *    // 三个指针，同步递增，一不小心就对不齐
 *
 * 【第7讲】一个指针遍历结构体数组：
 *    Account *p = accounts;
 *    // 一个指针，一次递增，信息完整
 */
void show_all_accounts(void)
{
    printf("【所有账户信息】\n");
    printf("%-8s %-8s %-12s\n", "账户ID", "姓名", "余额");
    printf("------------------------------------\n");

    /*
     * 【结构体指针遍历法】
     * p 指向结构体数组的首元素
     * p++ 让指针前进一步，指向下一个结构体
     * 步长 = sizeof(Account)（自动适应）
     *
     * 【对比】第6讲要三个指针同步递增，这里只要一个
     */
    Account *p = accounts;  /* 结构体指针，指向数组首元素 */

    for (int i = 0; i < MAX_ACCOUNTS; i++)
    {
        /*
         * 【知识点】-> 箭头运算符
         * p->id   等价于 (*p).id
         * p->name 等价于 (*p).name
         * p->balance 等价于 (*p).balance
         *
         * 写法更简洁，这是 C 语言为结构体指针专门设计的语法糖
         */
        printf("%-8d %-8s %-12.2f\n",
               p->id, p->name, p->balance);

        /* 指针递增，指向下一个结构体 */
        p++;
    }

    /*
     * 【演示】结构体大小
     * sizeof(Account) 包含所有成员的大小（可能有对齐填充）
     */
    printf("\nAccount 结构体大小：%d 字节\n", (int)sizeof(Account));
    printf("  int id:        %d 字节\n", (int)sizeof(int));
    printf("  char name[20]: %d 字节\n", NAME_LEN);
    printf("  double balance: %d 字节\n", (int)sizeof(double));
    printf("  （实际可能因内存对齐而略有不同）\n");
}

/* ============================================================
 *  结构体作为函数参数：值传递 vs 指针传递
 * ============================================================
 *
 *  下面两个函数演示结构体作为函数参数的两种方式
 *  这是本讲的重点之一——理解什么时候用值传递，什么时候用指针
 */

/* ---------- print_account_value：值传递演示 ---------- */
/*
 * 【值传递】把整个结构体复制一份传给函数
 *
 * 特点：
 *   ✅ 函数内修改不影响原数据（安全）
 *   ✅ 代码简单直观
 *   ❌ 复制整个结构体，浪费内存和时间（结构体大时明显）
 *   ❌ 函数内修改不会被调用者看到
 *
 * 适用场景：
 *   - 结构体较小（几个基本类型成员）
 *   - 只需要读取数据，不需要修改
 *   - 想保护原数据不被修改
 *
 * 【对比】就像复印一张名片给别人——
 *   别人在复印件上涂改，不影响你的原件
 *   但复印名片需要时间和纸张
 */
void print_account_value(Account acc)
{
    printf("[值传递] 账户ID: %d  姓名: %s  余额: %.2f\n",
           acc.id, acc.name, acc.balance);

    /* 函数内修改——但修改的是副本，不影响原数据 */
    acc.balance = 0.0;
    printf("[值传递] 函数内把余额改为：%.2f（不影响原数据）\n", acc.balance);
}

/* ---------- print_account_ptr：指针传递演示 ---------- */
/*
 * 【指针传递】只传结构体的地址（4或8字节），不复制数据
 *
 * 特点：
 *   ✅ 高效！只传地址，不复制数据
 *   ✅ 函数内修改直接影响原数据
 *   ✅ 适合大结构体和需要修改的场景
 *   ❌ 函数内修改会影响原数据（如果不加 const）
 *
 * 【const 保护】参数声明为 const Account* p
 *   表示"通过这个指针不能修改原数据"——只读模式
 *   如果函数只需要读取数据，加上 const 是好习惯
 *   编译器会帮你检查：如果函数内试图修改 p->balance，编译报错
 *
 * 【对比】就像把名片的原件交给别人看——
 *   别人直接看原件，不用复印，高效
 *   加了 const 就像说"只准看，不准改"
 *
 * 【衔接第5讲】指针传递就是第5讲的核心应用
 *   第5讲：void deposit(double* balance)  // 传基本类型指针
 *   第7讲：void func(Account* p)           // 传结构体指针
 *   本质一样——传地址，让函数能操作原数据
 */
void print_account_ptr(const Account* p)
{
    /*
     * 【知识点】-> 箭头运算符
     * 指针访问结构体成员用 ->，不能用 .
     * p->id  ✅  正确
     * p.id   ❌  错误：p 是指针，不是结构体变量
     *
     * (*p).id  ✅  也正确，但写起来麻烦
     * p->id    ✅  简洁，推荐使用
     */
    printf("[指针传递] 账户ID: %d  姓名: %s  余额: %.2f\n",
           p->id, p->name, p->balance);

    /* const 保护：以下代码会编译报错——不能修改 const 指针的数据 */
    /* p->balance = 0.0;  // 取消注释会报错！ */

    printf("[指针传递] 使用 const 保护，只读不可改\n");
}

/* ---------- print_success：打印成功信息 ---------- */
void print_success(const char* op, double amount)
{
    printf("操作成功！%s %.2f 元\n", op, amount);
    printf("当前余额：%.2f 元\n",
           accounts[current_account].balance);
}

/* ---------- print_error：打印错误信息 ---------- */
void print_error(const char* msg)
{
    printf("错误：%s\n", msg);
}

/*
 * ============================================================
 *  对比第6讲，我们收获了什么？
 * ============================================================
 *
 *  1. 数据封装：相关数据打包到一起
 *     第6讲：ids[5] + names[5][20] + balances[5]  三个平行数组
 *     第7讲：Account accounts[5]                   一个结构体数组
 *     好处：改一个账户的信息，只需操作一个结构体，不会"改错数组"
 *
 *  2. 代码更清晰：一眼看出数据归属
 *     第6讲：account_ids[i] 和 account_balances[i] 看不出关联
 *     第7讲：accounts[i].id 和 accounts[i].balance 一看就是同一账户
 *
 *  3. 扩展更容易：加字段只需加一个成员
 *     第6讲：想加"开户日期"？再加一个数组 date[5][20]
 *     第7讲：在 Account 里加一个成员 char date[20]，搞定
 *
 *  4. 指针更简洁：一个指针遍历所有信息
 *     第6讲：三个指针同步递增，容易出错
 *     第7讲：一个 Account* 指针，p->id、p->name、p->balance
 *
 *  5. 函数参数更清晰
 *     第6讲：void func(int ids[], char names[][20], double bals[], int n) // 四个参数
 *     第7讲：void func(Account* accs, int n)  // 两个参数
 *
 *  6. 数据封装思想萌芽
 *     结构体 = 数据打包 → 将来演变成类的"属性"
 *     函数   = 行为打包 → 将来演变成类的"方法"
 *     结构体 + 操作函数 = 面向对象编程的雏形
 *
 * ============================================================
 *  思考：还有问题吗？
 * ============================================================
 *
 *  1. 结构体大小固定，数组大小也固定
 *     MAX_ACCOUNTS=5，想加第6个账户？改代码重新编译
 *     （第8讲：链表 + 动态内存，大小随时变）
 *
 *  2. 结构体只是数据容器，没有"行为"
 *     存款、取款逻辑散落在各函数中，与数据分离
 *     （面向对象编程：把数据和行为绑在一起 = 类）
 *
 *  3. 结构体赋值是浅拷贝
 *     Account a = accounts[0]; 复制了所有成员，包括字符数组
 *     但如果成员是指针，只复制地址，不复制指向的数据
 *     （动态内存管理时要注意深拷贝 vs 浅拷贝）
 *
 *  4. 内存对齐：结构体大小可能大于各成员大小之和
 *     sizeof(Account) 可能不是 4+20+8=32，而是有填充字节
 *     （编译器为了提高访问效率，会做内存对齐）
 *
 *  结构体是从"散落数据"到"封装数据"的关键一步
 *  它解决了数据归属问题，为面向对象和插件框架打下基础
 *
 * ============================================================
 */
