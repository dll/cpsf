/*
 * ============================================================
 *  第8讲：链表 —— 动态数据的灵活管理
 *  ATM 链表化版本：从"固定数组"到"动态链表"
 * ============================================================
 *
 *  目标：用单链表管理 ATM 的交易记录和账户列表
 *
 *  第7讲的成果：
 *    用结构体把账户信息（ID + 名称 + 余额）打包到一起
 *    但——交易记录用固定数组存储，最多只能记10笔
 *         账户列表也是固定大小，想加第6个账户？改代码重新编译
 *
 *  第8讲的进步：
 *    1. 用单链表存储交易记录（动态增长，想记多少记多少）
 *    2. 用单链表管理账户列表（随时添加/删除账户）
 *    3. 用 malloc/free 实现动态内存管理（衔接第5讲的内存模型）
 *    4. 实现完整的链表操作：创建、插入、删除、遍历、销毁
 *    5. 演示链表在插件框架中的关键应用（插件链表管理、配置化菜单）
 *
 *  对比前几讲：
 *    第6讲：double trans[10];                    // 固定数组，最多10笔
 *           Account accounts[5];                  // 固定大小，最多5个账户
 *    第8讲：TransactionNode* trans_head;         // 链表头指针，无限增长
 *           AccountNode* acct_head;              // 链表头指针，随时增删
 *
 *  编译运行：
 *    gcc -Wall -o linked_atm linked_atm.c && ./linked_atm
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>   /* malloc / free / exit 所需头文件 */
#include <string.h>   /* strcpy / strcmp 所需头文件 */

/* ============================================================
 *  常量定义
 * ============================================================
 *  对比第6讲：不再需要 MAX_TRANSACTIONS 和 MAX_ACCOUNTS
 *  链表的大小是动态的，不需要预先定义上限
 */
#define NAME_LEN 20   /* 账户名最大长度（字符数组仍需固定大小） */
#define DESC_LEN 40   /* 交易描述最大长度 */

/* 交易类型常量（与第6讲保持一致） */
#define TRANS_DEPOSIT  1    /* 存款 */
#define TRANS_WITHDRAW 2    /* 取款 */
#define TRANS_TRANSFER 3    /* 转账 */

/* ============================================================
 *  结构体定义 —— 链表的"车厢"
 * ============================================================
 *
 *  【对比第7讲】第7讲的 Account 结构体只有数据，没有指针
 *  【现在】每个节点除了数据，还多了一个 next 指针——
 *         指向下一个节点，就像火车车厢之间的挂钩
 *
 *  链表节点 = 数据域 + 指针域
 *  数据域：存储实际信息（交易金额、类型等）
 *  指针域：存储下一个节点的地址（"挂钩"）
 */

/*
 * 交易记录节点
 *
 * 数据域：amount（金额）+ type（类型）+ desc（描述）
 * 指针域：next（指向下一个交易记录节点）
 *
 * 【比喻】每个交易记录就是一节火车车厢
 *         里面装着货物（金额/类型），后面挂钩连着下一节车厢
 */
typedef struct TransactionNode {
    double amount;                  /* 交易金额 */
    int    type;                    /* 交易类型 */
    char   desc[DESC_LEN];          /* 交易描述（如"存款 500.00"） */
    struct TransactionNode* next;  /* 指向下一个交易记录 */
} TransactionNode;

/*
 * 账户节点
 *
 * 数据域：id + name + balance（第7讲已学）
 * 指针域：next（指向下一个账户节点）
 *
 * 【对比第7讲】第7讲用 Account accounts[5] 固定数组存储账户
 *              想加第6个？改 MAX_ACCOUNTS 重新编译
 * 【现在】用链表，想加几个加几个，随时增删
 */
typedef struct AccountNode {
    int    id;                     /* 账户ID */
    char   name[NAME_LEN];         /* 账户名 */
    double balance;                /* 账户余额 */
    struct AccountNode* next;      /* 指向下一个账户 */
} AccountNode;

/* ============================================================
 *  全局变量 —— 链表头指针
 * ============================================================
 *
 *  【对比第6讲】
 *    第6讲：double trans_amounts[10];  （数组，编译时就分配好内存）
 *           Account accounts[5];         （数组，固定大小）
 *    第8讲：TransactionNode* trans_head = NULL;  （指针，运行时动态分配）
 *           AccountNode* acct_head = NULL;       （指针，链表头）
 *
 *  链表头指针是整个链表的"入口"
 *  有了头指针，就能顺着 next 找到所有节点——就像火车头
 *  如果头指针是 NULL，说明链表为空（没有任何车厢）
 */
TransactionNode* trans_head = NULL;  /* 交易记录链表头指针 */
AccountNode*     acct_head  = NULL;  /* 账户链表头指针 */
AccountNode*     current_acct = NULL; /* 当前操作的账户指针 */

/* ============================================================
 *  链表操作函数声明 —— 交易记录链表
 * ============================================================
 */
TransactionNode* create_trans_node(double amount, int type, const char* desc);
void  trans_insert_head(double amount, int type, const char* desc);
void  trans_insert_tail(double amount, int type, const char* desc);
void  trans_delete_by_amount(double amount);
void  trans_traverse(void);
void  trans_destroy(void);

/* ============================================================
 *  链表操作函数声明 —— 账户链表
 * ============================================================
 */
AccountNode* create_acct_node(int id, const char* name, double balance);
void  acct_insert_tail(int id, const char* name, double balance);
AccountNode* acct_find_by_id(int id);
void  acct_delete_by_id(int id);
void  acct_traverse(void);
void  acct_destroy(void);

/* ============================================================
 *  ATM 业务函数声明
 * ============================================================
 */
void show_welcome(void);
void show_menu(void);
void select_account(void);
void query_balance(void);
void deposit(void);
void withdraw(void);
void transfer(void);
void show_transactions(void);
void show_all_accounts(void);
void demo_plugin_list(void);
const char* trans_type_name(int type);
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

    /* 初始化：用链表添加初始账户 */
    /*
     * 【对比第6讲】第6讲用数组初始化：
     *   int ids[5] = {1001, 1002, ...};
     *   double balances[5] = {1000.0, 2000.0, ...};
     *
     * 【现在】用链表尾部插入逐个添加账户
     * 每个节点都是 malloc 动态分配的，不需要预先定义大小
     */
    acct_insert_tail(1001, "张三", 1000.0);
    acct_insert_tail(1002, "李四", 2000.0);
    acct_insert_tail(1003, "王五", 500.0);
    acct_insert_tail(1004, "赵六", 3000.0);
    acct_insert_tail(1005, "钱七", 1500.0);

    printf("已用链表加载 %d 个账户。\n\n", 5);

    /* 选择账户（链表查找） */
    select_account();
    if (current_acct == NULL) {
        printf("未找到账户，程序退出。\n");
        /* 退出前销毁链表，释放内存 */
        trans_destroy();
        acct_destroy();
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
            case 7:
                demo_plugin_list();
                break;
            case 0:
                printf("感谢使用 CCIT ATM 系统（链表版），再见！\n");
                running = 0;
                break;
            default:
                print_error("无效的选择，请重新输入！");
                break;
        }
    }

    /* ============================================================
     *  程序退出前：销毁链表，释放所有动态分配的内存
     * ============================================================
     *  【关键】malloc 分配的内存不会自动释放！
     *  如果不 free，就会造成"内存泄漏"（Memory Leak）
     *
     *  这就像你借了一堆火车车厢，用完不还——
     *  停车场（内存）越来越满，最终系统崩溃
     *
     *  好习惯：每个 malloc 都要有对应的 free
     *  在程序结束时统一销毁链表，逐个 free 每个节点
     */
    trans_destroy();
    acct_destroy();
    printf("（链表已销毁，内存已释放）\n");

    return 0;
}

/* ============================================================
 *  交易记录链表操作实现
 * ============================================================ */

/* ---------- create_trans_node：创建一个新节点 ---------- */
/*
 * 【核心操作】用 malloc 在堆上分配一个新节点的内存
 *
 * 步骤：
 *   1. malloc 分配 sizeof(TransactionNode) 字节的内存
 *   2. 填充数据域（金额、类型、描述）
 *   3. 指针域 next 设为 NULL（新节点还没有后继）
 *   4. 返回新节点的指针
 *
 * 【对比第6讲】第6讲直接写 trans_amounts[i] = amount;
 *              数组在编译时就分配好内存，不需要 malloc
 * 【现在】每个节点都是运行时动态分配的
 *
 * 【内存模型】衔接第5讲：
 *   栈（Stack）：局部变量、函数参数，自动分配释放
 *   堆（Heap） ：malloc 分配的内存，手动管理（malloc/free）
 *   链表节点存在堆上——所以能动态增长！
 */
TransactionNode* create_trans_node(double amount, int type, const char* desc)
{
    /* malloc 分配内存 */
    TransactionNode* node = (TransactionNode*)malloc(sizeof(TransactionNode));

    /* 检查 malloc 是否成功（分配失败返回 NULL） */
    if (node == NULL) {
        printf("错误：内存分配失败！\n");
        return NULL;
    }

    /* 填充数据域 */
    node->amount = amount;
    node->type = type;
    strncpy(node->desc, desc, DESC_LEN - 1);
    node->desc[DESC_LEN - 1] = '\0';  /* 确保字符串以 \0 结尾 */

    /* 指针域设为 NULL（新节点的后继暂时为空） */
    node->next = NULL;

    return node;
}

/* ---------- trans_insert_head：头部插入 ---------- */
/*
 * 在链表头部插入新节点（新的交易记录插到最前面）
 *
 * 头部插入步骤：
 *   1. 创建新节点
 *   2. 新节点的 next 指向原来的头节点
 *   3. 头指针指向新节点
 *
 * 【时间复杂度】O(1) —— 只改两个指针，不需要遍历
 * 【对比】数组头部插入需要把所有元素后移，O(n)
 *
 * 【比喻】火车头前面加一节新车厢——
 *         把新车厢挂在火车头上，原来的车厢接在新车厢后面
 *
 *    插入前：  head -> A -> B -> C -> NULL
 *    插入后：  head -> NEW -> A -> B -> C -> NULL
 */
void trans_insert_head(double amount, int type, const char* desc)
{
    TransactionNode* node = create_trans_node(amount, type, desc);
    if (node == NULL) return;

    /* 新节点的 next 指向原来的头节点 */
    node->next = trans_head;

    /* 头指针指向新节点 */
    trans_head = node;
}

/* ---------- trans_insert_tail：尾部插入 ---------- */
/*
 * 在链表尾部插入新节点（新的交易记录追加到最后面）
 *
 * 尾部插入步骤：
 *   1. 创建新节点
 *   2. 如果链表为空（头指针是 NULL），直接让头指针指向新节点
 *   3. 否则，遍历到最后一个节点，让它指向新节点
 *
 * 【时间复杂度】O(n) —— 需要遍历到链表末尾
 *   （优化方案：维护一个尾指针，可达 O(1)，这里暂不优化）
 *
 * 【比喻】在火车最后加一节车厢——
 *         要先走到最后一节车厢，才能把新车厢挂上去
 *
 *    插入前：  head -> A -> B -> C -> NULL
 *    插入后：  head -> A -> B -> C -> NEW -> NULL
 */
void trans_insert_tail(double amount, int type, const char* desc)
{
    TransactionNode* node = create_trans_node(amount, type, desc);
    if (node == NULL) return;

    /* 情况1：链表为空，新节点就是头节点 */
    if (trans_head == NULL) {
        trans_head = node;
        return;
    }

    /* 情况2：链表非空，遍历到最后一个节点 */
    TransactionNode* cur = trans_head;
    while (cur->next != NULL) {
        cur = cur->next;
    }

    /* cur 现在指向最后一个节点，让它指向新节点 */
    cur->next = node;
}

/* ---------- trans_delete_by_amount：按值删除 ---------- */
/*
 * 删除链表中第一个金额匹配的交易记录
 *
 * 按值删除步骤：
 *   1. 链表为空，直接返回
 *   2. 要删的是头节点：头指针后移，free 旧头节点
 *   3. 要删的是中间/末尾节点：找到前驱节点，修改指针跳过被删节点
 *   4. free 被删节点的内存
 *
 * 【关键】删除链表节点需要保存"前驱节点"的指针
 *         因为要修改前驱的 next 指针，让它跳过被删节点
 *
 * 【时间复杂度】O(n) —— 需要遍历查找
 *
 * 【比喻】从火车中摘掉一节车厢——
 *         要把前后两节车厢重新挂钩，然后运走被摘的车厢
 *
 *    删除前：  head -> A -> B -> C -> NULL  （删B）
 *    删除后：  head -> A -> C -> NULL
 *              B 被 free 回收
 */
void trans_delete_by_amount(double amount)
{
    /* 链表为空 */
    if (trans_head == NULL) {
        print_error("交易记录为空，无内容可删。");
        return;
    }

    /* 情况1：要删的是头节点 */
    if (trans_head->amount == amount) {
        TransactionNode* tmp = trans_head;   /* 保存旧头节点 */
        trans_head = trans_head->next;       /* 头指针后移 */
        printf("已删除交易：%.2f 元\n", tmp->amount);
        free(tmp);                            /* 释放内存 */
        return;
    }

    /* 情况2：要删的是中间或末尾节点 */
    TransactionNode* prev = trans_head;       /* 前驱节点 */
    TransactionNode* cur  = trans_head->next;  /* 当前节点 */

    while (cur != NULL) {
        if (cur->amount == amount) {
            /* 找到了！让前驱的 next 跳过当前节点 */
            prev->next = cur->next;
            printf("已删除交易：%.2f 元\n", cur->amount);
            free(cur);  /* 释放被删节点的内存 */
            return;
        }
        prev = cur;
        cur = cur->next;
    }

    /* 遍历完都没找到 */
    printf("未找到金额为 %.2f 元的交易记录。\n", amount);
}

/* ---------- trans_traverse：遍历链表 ---------- */
/*
 * 从头到尾遍历交易记录链表，打印每一条记录
 *
 * 遍历步骤：
 *   1. 从头指针开始
 *   2. 当前节点不为 NULL 时，处理当前节点
 *   3. 移动到下一个节点：cur = cur->next
 *   4. 重复直到 cur == NULL
 *
 * 【对比第6讲】
 *   第6讲：for (int i = 0; i < 10; i++) printf("%f", trans[i]);
 *          数组遍历用索引 i，从 0 到 N-1
 *   第8讲：for (cur = head; cur != NULL; cur = cur->next) ...
 *          链表遍历用指针，从头到 NULL
 *
 * 【时间复杂度】O(n)
 *
 * 【比喻】列车长从火车头出发，逐节车厢检查——
 *         每检查完一节，走到下一节，直到最后一节（next 为 NULL）
 */
void trans_traverse(void)
{
    printf("【交易记录】（链表存储，动态增长）\n");

    if (trans_head == NULL) {
        printf("暂无交易记录。\n");
        return;
    }

    printf("%-6s %-8s %-10s %-20s\n", "序号", "类型", "金额", "描述");
    printf("--------------------------------------------------\n");

    int index = 1;
    TransactionNode* cur = trans_head;

    /* 遍历链表：从 head 开始，直到 NULL */
    while (cur != NULL) {
        printf("%-6d %-8s %-10.2f %-20s\n",
               index,
               trans_type_name(cur->type),
               cur->amount,
               cur->desc);
        cur = cur->next;   /* 移动到下一个节点 */
        index++;
    }

    printf("--------------------------------------------------\n");
    printf("共 %d 条交易记录（链表节点数）\n", index - 1);
}

/* ---------- trans_destroy：销毁链表 ---------- */
/*
 * 销毁整个交易记录链表，释放所有节点的内存
 *
 * 销毁步骤：
 *   1. 从头节点开始
 *   2. 保存当前节点指针
 *   3. 头指针后移到下一个节点
 *   4. free 当前节点
 *   5. 重复直到头指针为 NULL
 *
 * 【关键易错点】不能先 free 再访问 next！
 *   错误写法：
 *     free(cur);
 *     cur = cur->next;  // 错误！cur 已经被释放，访问 next 是未定义行为
 *
 *   正确写法：先保存 next，再 free
 *     TransactionNode* tmp = cur;
 *     cur = cur->next;
 *     free(tmp);
 *
 * 【为什么必须销毁？】
 *   malloc 分配的内存在堆上，程序退出前如果不 free，
 *   操作系统虽然会回收，但这是不良习惯。
 *   在长期运行的程序中，不 free 会导致内存泄漏——
 *   内存越用越少，最终系统崩溃。
 */
void trans_destroy(void)
{
    TransactionNode* cur = trans_head;

    while (cur != NULL) {
        TransactionNode* tmp = cur;   /* 保存当前节点 */
        cur = cur->next;              /* 先移到下一个 */
        free(tmp);                    /* 再释放当前的 */
    }

    trans_head = NULL;  /* 头指针置空 */
}

/* ============================================================
 *  账户链表操作实现
 * ============================================================ */

/* ---------- create_acct_node：创建账户节点 ---------- */
/*
 * 和 create_trans_node 类似，创建一个账户节点
 * 用 malloc 分配内存，填充数据，next 设为 NULL
 */
AccountNode* create_acct_node(int id, const char* name, double balance)
{
    AccountNode* node = (AccountNode*)malloc(sizeof(AccountNode));

    if (node == NULL) {
        printf("错误：内存分配失败！\n");
        return NULL;
    }

    node->id = id;
    strncpy(node->name, name, NAME_LEN - 1);
    node->name[NAME_LEN - 1] = '\0';
    node->balance = balance;
    node->next = NULL;

    return node;
}

/* ---------- acct_insert_tail：尾部插入账户 ---------- */
/*
 * 在账户链表尾部添加新账户
 *
 * 【对比第6讲】第6讲用固定数组，只能存 MAX_ACCOUNTS 个
 * 【现在】链表尾部插入，想加几个加几个
 */
void acct_insert_tail(int id, const char* name, double balance)
{
    AccountNode* node = create_acct_node(id, name, balance);
    if (node == NULL) return;

    if (acct_head == NULL) {
        acct_head = node;
        return;
    }

    AccountNode* cur = acct_head;
    while (cur->next != NULL) {
        cur = cur->next;
    }
    cur->next = node;
}

/* ---------- acct_find_by_id：按ID查找账户 ---------- */
/*
 * 遍历链表查找指定 ID 的账户
 *
 * 【对比第6讲】第6讲用 for 循环遍历数组
 *   int find_account_by_id(int id) {
 *       for (int i = 0; i < 5; i++)
 *           if (ids[i] == id) return i;
 *       return -1;
 *   }
 *
 * 【现在】遍历链表，返回节点指针（而不是索引）
 *
 * 返回值：找到返回节点指针，找不到返回 NULL
 */
AccountNode* acct_find_by_id(int id)
{
    AccountNode* cur = acct_head;

    while (cur != NULL) {
        if (cur->id == id) {
            return cur;  /* 找到了 */
        }
        cur = cur->next;
    }

    return NULL;  /* 没找到 */
}

/* ---------- acct_delete_by_id：按ID删除账户 ---------- */
/*
 * 从账户链表中删除指定 ID 的账户
 *
 * 逻辑和 trans_delete_by_amount 一样：
 *   1. 处理头节点的情况
 *   2. 处理中间/末尾节点（需要保存前驱）
 *   3. free 被删节点
 */
void acct_delete_by_id(int id)
{
    if (acct_head == NULL) {
        print_error("账户列表为空。");
        return;
    }

    /* 删头节点 */
    if (acct_head->id == id) {
        AccountNode* tmp = acct_head;
        acct_head = acct_head->next;
        printf("已删除账户：%d %s\n", tmp->id, tmp->name);
        free(tmp);
        return;
    }

    /* 删中间/末尾节点 */
    AccountNode* prev = acct_head;
    AccountNode* cur  = acct_head->next;

    while (cur != NULL) {
        if (cur->id == id) {
            prev->next = cur->next;
            printf("已删除账户：%d %s\n", cur->id, cur->name);
            free(cur);
            return;
        }
        prev = cur;
        cur = cur->next;
    }

    printf("未找到账户ID：%d\n", id);
}

/* ---------- acct_traverse：遍历所有账户 ---------- */
/*
 * 遍历账户链表，打印所有账户信息
 */
void acct_traverse(void)
{
    AccountNode* cur = acct_head;

    printf("%-8s %-10s %-12s\n", "账户ID", "姓名", "余额");
    printf("------------------------------------\n");

    while (cur != NULL) {
        printf("%-8d %-10s %-12.2f\n", cur->id, cur->name, cur->balance);
        cur = cur->next;
    }
}

/* ---------- acct_destroy：销毁账户链表 ---------- */
/*
 * 释放所有账户节点的内存
 * 逻辑和 trans_destroy 一样
 */
void acct_destroy(void)
{
    AccountNode* cur = acct_head;

    while (cur != NULL) {
        AccountNode* tmp = cur;
        cur = cur->next;
        free(tmp);
    }

    acct_head = NULL;
}

/* ============================================================
 *  ATM 业务函数实现
 * ============================================================ */

/* ---------- show_welcome：显示欢迎界面 ---------- */
void show_welcome(void)
{
    printf("========================================\n");
    printf("   欢迎使用 CCIT ATM 系统（链表版）\n");
    printf("========================================\n");
    printf("  动态交易记录 | 动态账户管理 | 无上限\n");
    printf("\n");
}

/* ---------- show_menu：显示主菜单 ---------- */
/*
 * 【架构预告】这个菜单现在是写死的（固定选项）
 * 第13讲会用链表实现"配置化菜单"——
 * 每个菜单项是一个链表节点，可以动态增删
 * 这就是链表在插件框架中的核心应用之一！
 */
void show_menu(void)
{
    printf("\n-------- 主菜单 --------\n");
    printf("  1. 查询余额\n");
    printf("  2. 存款\n");
    printf("  3. 取款\n");
    printf("  4. 转账\n");
    printf("  5. 查看交易记录（链表）\n");
    printf("  6. 查看所有账户（链表）\n");
    printf("  7. 插件链表管理演示\n");   /* 新功能：演示插件框架中的链表应用 */
    printf("  0. 退出\n");
    printf("------------------------\n");
}

/* ---------- select_account：选择账户 ---------- */
/*
 * 【对比第6讲】第6讲用数组索引选择账户
 * 【现在】用链表遍历展示，用指针查找账户
 */
void select_account(void)
{
    int input_id = 0;

    printf("【选择账户】\n");
    printf("可用账户列表：\n");

    /* 遍历链表展示所有账户 */
    acct_traverse();

    printf("\n请输入您的账户ID：");
    scanf("%d", &input_id);

    /* 在链表中查找账户 */
    current_acct = acct_find_by_id(input_id);
    if (current_acct != NULL) {
        printf("登录成功！欢迎，%s\n\n", current_acct->name);
    } else {
        print_error("账户ID不存在！");
    }
}

/* ---------- query_balance：查询余额 ---------- */
void query_balance(void)
{
    printf("【查询余额】\n");
    printf("账户名：%s\n", current_acct->name);
    printf("您当前的账户余额为：%.2f 元\n", current_acct->balance);
}

/* ---------- deposit：存款 ---------- */
/*
 * 【对比第6讲】第6讲：account_balances[current_account] += amount;
 *                 需要维护 current_account 索引
 * 【现在】current_acct->balance += amount;
 *        直接通过指针操作节点数据，更直观
 */
void deposit(void)
{
    double amount = 0.0;
    char desc[DESC_LEN];

    printf("【存款业务】\n");
    printf("请输入存款金额：");
    scanf("%lf", &amount);

    if (amount <= 0) {
        print_error("存款金额必须大于0！");
        return;
    }

    current_acct->balance += amount;

    /* 构造交易描述 */
    snprintf(desc, DESC_LEN, "%s 存入 %.2f", current_acct->name, amount);

    /*
     * 用链表尾部插入记录交易
     * 【对比第6讲】第6讲用循环数组覆盖最旧的记录
     * 【现在】链表追加，永远不会丢失记录！
     */
    trans_insert_tail(amount, TRANS_DEPOSIT, desc);

    print_success("存入", amount);
}

/* ---------- withdraw：取款 ---------- */
void withdraw(void)
{
    double amount = 0.0;
    char desc[DESC_LEN];

    printf("【取款业务】\n");
    printf("请输入取款金额：");
    scanf("%lf", &amount);

    if (amount <= 0) {
        print_error("取款金额必须大于0！");
        return;
    }

    if (amount > current_acct->balance) {
        print_error("余额不足！");
        return;
    }

    current_acct->balance -= amount;

    snprintf(desc, DESC_LEN, "%s 取出 %.2f", current_acct->name, amount);
    trans_insert_tail(amount, TRANS_WITHDRAW, desc);

    print_success("取出", amount);
}

/* ---------- transfer：转账 ---------- */
void transfer(void)
{
    double amount = 0.0;
    int target_id = 0;
    char desc[DESC_LEN];

    printf("【转账业务】\n");
    printf("请输入转账金额：");
    scanf("%lf", &amount);

    if (amount <= 0) {
        print_error("转账金额必须大于0！");
        return;
    }

    if (amount > current_acct->balance) {
        print_error("余额不足，无法转账！");
        return;
    }

    printf("请输入对方账户ID：");
    scanf("%d", &target_id);

    /* 在链表中查找目标账户 */
    AccountNode* target = acct_find_by_id(target_id);
    if (target == NULL) {
        print_error("对方账户不存在！");
        return;
    }

    if (target == current_acct) {
        print_error("不能给自己转账！");
        return;
    }

    /* 扣减当前账户，增加目标账户 */
    current_acct->balance -= amount;
    target->balance += amount;

    snprintf(desc, DESC_LEN, "%s 向 %s 转出 %.2f",
             current_acct->name, target->name, amount);
    trans_insert_tail(amount, TRANS_TRANSFER, desc);

    printf("转账成功！向 %s 转出 %.2f 元\n", target->name, amount);
    printf("当前余额：%.2f 元\n", current_acct->balance);
}

/* ---------- show_transactions：查看交易记录 ---------- */
/*
 * 调用链表遍历函数展示所有交易记录
 * 链表可以无限增长，不会像数组那样覆盖旧记录
 */
void show_transactions(void)
{
    trans_traverse();
}

/* ---------- show_all_accounts：查看所有账户 ---------- */
void show_all_accounts(void)
{
    printf("【所有账户信息】（链表存储）\n");
    acct_traverse();

    /* 统计链表长度 */
    int count = 0;
    AccountNode* cur = acct_head;
    while (cur != NULL) {
        count++;
        cur = cur->next;
    }
    printf("\n共 %d 个账户（链表节点数，无上限）\n", count);
}

/* ============================================================
 *  插件链表管理演示
 * ============================================================
 *
 *  【架构预告】这是链表在插件框架中的核心应用演示
 *
 *  在第12-13讲的插件框架中，每加载一个插件就创建一个节点，
 *  挂到插件链表上。框架通过遍历链表来调用每个插件的功能。
 *
 *  本函数用一个简化的"插件"结构体来演示：
 *    - 每个插件有名字和功能描述
 *    - 用链表管理所有已加载的插件
 *    - 遍历链表"执行"每个插件
 *
 *  这就是"插件链表管理"的雏形！
 */

/* 简化版插件结构体（第12讲会扩展为包含函数指针的接口） */
typedef struct PluginNode {
    char name[NAME_LEN];           /* 插件名称 */
    char feature[DESC_LEN];        /* 插件功能描述 */
    struct PluginNode* next;       /* 指向下一个插件 */
} PluginNode;

void demo_plugin_list(void)
{
    printf("【插件链表管理演示】\n");
    printf("----------------------------------------\n");
    printf("在插件框架中，每个插件都是一个链表节点。\n");
    printf("框架通过遍历链表来管理和调用所有插件。\n\n");

    /* 创建插件链表（头部插入） */
    PluginNode* plugin_head = NULL;

    /* 模拟加载3个插件（每个插件就是一个链表节点） */
    char* plugins[][2] = {
        {"汇率查询", "查询实时汇率"},
        {"积分兑换", "积分兑换礼品"},
        {"电子发票", "生成电子发票"}
    };

    for (int i = 0; i < 3; i++) {
        PluginNode* p = (PluginNode*)malloc(sizeof(PluginNode));
        if (p == NULL) continue;
        strncpy(p->name, plugins[i][0], NAME_LEN - 1);
        p->name[NAME_LEN - 1] = '\0';
        strncpy(p->feature, plugins[i][1], DESC_LEN - 1);
        p->feature[DESC_LEN - 1] = '\0';

        /* 头部插入：新插件挂到链表头部 */
        p->next = plugin_head;
        plugin_head = p;
    }

    /* 遍历插件链表，"执行"每个插件 */
    printf("已加载插件列表（遍历链表）：\n");
    PluginNode* cur = plugin_head;
    int idx = 1;
    while (cur != NULL) {
        printf("  [%d] 插件名：%s  |  功能：%s\n",
               idx, cur->name, cur->feature);
        cur = cur->next;
        idx++;
    }

    printf("\n这就是插件框架的核心机制！\n");
    printf("第12讲将扩展为：插件结构体包含函数指针\n");
    printf("第13讲将实现：配置化菜单（用链表动态管理菜单项）\n");

    /* 销毁插件链表 */
    cur = plugin_head;
    while (cur != NULL) {
        PluginNode* tmp = cur;
        cur = cur->next;
        free(tmp);
    }
}

/* ---------- trans_type_name：交易类型转中文名 ---------- */
const char* trans_type_name(int type)
{
    switch (type) {
        case TRANS_DEPOSIT:  return "存款";
        case TRANS_WITHDRAW: return "取款";
        case TRANS_TRANSFER: return "转账";
        default:             return "未知";
    }
}

/* ---------- print_success：打印成功信息 ---------- */
void print_success(const char* op, double amount)
{
    printf("操作成功！%s %.2f 元\n", op, amount);
    printf("当前余额：%.2f 元\n", current_acct->balance);
}

/* ---------- print_error：打印错误信息 ---------- */
void print_error(const char* msg)
{
    printf("错误：%s\n", msg);
}

/*
 * ============================================================
 *  对比前几讲，我们收获了什么？
 * ============================================================
 *
 *  1. 动态大小，不受限制
 *     第6讲：trans[10]，最多10笔交易，超过就覆盖
 *     第8讲：链表动态增长，想记多少记多少
 *
 *  2. 随时增删
 *     第6讲：accounts[5]，固定5个账户，改代码才能扩展
 *     第8讲：链表随时添加/删除账户，运行时动态管理
 *
 *  3. 内存按需分配
 *     第6讲：数组编译时就分配全部内存，不管用不用
 *     第8讲：malloc 按需分配，用多少分配多少
 *
 *  4. 指针的实战应用
 *     第5讲学了指针的概念，第8讲用指针串联链表
 *     next 指针就是链表的灵魂——没有指针就没有链表
 *
 *  5. 插件框架的基石
 *     插件管理 = 链表 + 函数指针（第12讲）
 *     配置化菜单 = 链表动态管理菜单项（第13讲）
 *     链表是从"数据结构"到"软件架构"的关键桥梁
 *
 * ============================================================
 *  思考：链表完美了吗？
 * ============================================================
 *
 *  链表解决了数组的固定大小问题，但也带来了新问题：
 *
 *  1. 不能随机访问
 *     数组：arr[5] 一步到位，O(1)
 *     链表：必须从头遍历，O(n)
 *
 *  2. 额外内存开销
 *     每个节点多一个 next 指针（4或8字节）
 *
 *  3. 内存管理负担
 *     malloc/free 容易出错（忘记free=内存泄漏，free两次=双重释放）
 *
 *  4. 缓存不友好
 *     数组连续内存，CPU缓存命中率高
 *     链表节点分散，缓存命中率低
 *
 *  没有完美的数据结构，只有适合场景的选择！
 *
 * ============================================================
 *  从程序员到架构师：链表的战略意义
 * ============================================================
 *
 *  链表不仅仅是一种数据结构，更是架构设计的基石：
 *
 *  - 插件链表管理（第12讲）：每加载一个插件就挂一个节点
 *  - 配置化菜单（第13讲）：菜单项用链表管理，动态增删
 *  - 事件回调链（架构模式）：回调函数用链表串联
 *  - 对象池管理（架构模式）：对象用链表管理生命周期
 *
 *  学好链表，就是从"写代码"到"做架构"的第一步！
 *
 * ============================================================
 */
