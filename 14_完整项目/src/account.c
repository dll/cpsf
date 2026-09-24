/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  account.c —— 账户模块实现（编译进共享库 atmcore.dll）
 * ============================================================
 *
 *  【第9讲回顾】
 *    数据用 static 修饰，外部只能通过接口函数操作——
 *    这就是"数据封装"：把数据藏在文件内部，只暴露行为。
 *
 *  【一个细节】
 *    这里的 static 变量属于 atmcore.dll 的全局数据段。
 *    只要主程序和所有插件都链接同一个 atmcore.dll，
 *    它们看到的就是同一份 accounts[] 数组。
 * ============================================================
 */

#include "account.h"
#include <stdio.h>
#include <string.h>

/* ---- 内部数据（文件级 static，仅本模块可见）---- */
static Account accounts[MAX_ACCOUNTS];
static int next_id = 1001;          /* 下一个账户ID */
static int account_total = 0;       /* 当前账户数量 */
static int current_id = 0;          /* 当前账户ID（模拟插卡） */

/* ---- 内部辅助：安全拷贝户名（避免 strncpy 截断告警）---- */
static void copy_name(char *dst, const char *src, size_t dst_size)
{
    if (dst_size == 0) {
        return;
    }
    snprintf(dst, dst_size, "%s", src);
}

/* ---- 生命周期 ---- */

void account_init_demo(void)
{
    account_total = 0;
    next_id = 1001;
    current_id = 0;
    memset(accounts, 0, sizeof(accounts));

    int a = account_create("张三", 10000.0);
    account_create("李四", 5000.0);
    current_id = a;   /* 默认"插入"张三的卡 */

    printf("  [账务模块] 演示账户就绪，当前账户 ID=%d\n", current_id);
}

/* ---- 接口实现 ---- */

int account_create(const char *name, double initial_balance)
{
    if (account_total >= MAX_ACCOUNTS) {
        fprintf(stderr, "[错误] 账户数量已达上限 %d\n", MAX_ACCOUNTS);
        return -1;
    }
    if (initial_balance < 0) {
        fprintf(stderr, "[错误] 初始余额不能为负\n");
        return -1;
    }

    Account *acc = &accounts[account_total];
    acc->id = next_id++;
    copy_name(acc->name, name, MAX_NAME_LEN);
    acc->balance = initial_balance;
    acc->active = true;
    account_total++;

    printf("  [开户] ID:%d  户名:%s  余额:%.2f\n",
           acc->id, acc->name, acc->balance);
    return acc->id;
}

Account* account_find(int id)
{
    int i;
    for (i = 0; i < account_total; i++) {
        if (accounts[i].id == id && accounts[i].active) {
            return &accounts[i];
        }
    }
    return NULL;
}

bool account_deposit(int id, double amount)
{
    Account *acc = account_find(id);
    if (acc == NULL) {
        fprintf(stderr, "[错误] 账户 %d 不存在\n", id);
        return false;
    }
    if (amount <= 0) {
        fprintf(stderr, "[错误] 存款金额必须大于0\n");
        return false;
    }
    acc->balance += amount;
    printf("  [存款] 账户:%d(%s)  金额:%.2f  余额:%.2f\n",
           id, acc->name, amount, acc->balance);
    return true;
}

bool account_withdraw(int id, double amount)
{
    Account *acc = account_find(id);
    if (acc == NULL) {
        fprintf(stderr, "[错误] 账户 %d 不存在\n", id);
        return false;
    }
    if (amount <= 0) {
        fprintf(stderr, "[错误] 取款金额必须大于0\n");
        return false;
    }
    if (acc->balance < amount) {
        fprintf(stderr, "[错误] 余额不足！当前余额:%.2f\n", acc->balance);
        return false;
    }
    acc->balance -= amount;
    printf("  [取款] 账户:%d(%s)  金额:%.2f  余额:%.2f\n",
           id, acc->name, amount, acc->balance);
    return true;
}

double account_get_balance(int id)
{
    Account *acc = account_find(id);
    if (acc == NULL) {
        fprintf(stderr, "[错误] 账户 %d 不存在\n", id);
        return -1.0;
    }
    return acc->balance;
}

void account_list_all(void)
{
    int i;
    printf("\n  ======== 账户列表 ========\n");
    printf("  %-8s %-16s %-12s %-6s\n", "ID", "户名", "余额", "状态");
    printf("  ----------------------------------------\n");
    for (i = 0; i < account_total; i++) {
        printf("  %-8d %-16s %-12.2f %-6s\n",
               accounts[i].id,
               accounts[i].name,
               accounts[i].balance,
               accounts[i].active ? "活跃" : "冻结");
    }
    printf("  ----------------------------------------\n");
    printf("  总计: %d 个账户\n", account_total);
}

int account_count(void)
{
    return account_total;
}

int account_current_id(void)
{
    return current_id;
}

void account_set_current(int id)
{
    current_id = id;
}
