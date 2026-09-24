/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  plugins/query_plugin.c —— 查询余额插件
 * ============================================================
 *
 *  【与前两个插件的不同点：need_amount = 0】
 *    查询不需要金额。插件通过把 need_amount 设为 0 来"告诉框架"：
 *      "别替我读金额，我自己不需要参数。"
 *    框架据此跳过金额输入，菜单和输入协议因此完全由插件声明。
 *
 *  这一个小小的元数据字段，体现了配置化的价值：
 *    框架不需要 switch(插件类型) 去判断谁需要什么参数。
 * ============================================================
 */

#include "plugin.h"
#include "account.h"
#include "transaction.h"
#include "plugins.h"

#include <stdio.h>

static int query_init(Plugin* self)
{
    (void)self;
    return 0;
}

static int query_start(Plugin* self)
{
    (void)self;
    return 0;
}

/* 查询：打印当前账户余额、全部账户、并回放当前账户流水 */
static int query_execute(Plugin* self, double amount)
{
    int id = account_current_id();
    double balance;

    (void)amount;   /* 查询不使用金额参数 */

    balance = account_get_balance(id);
    if (balance < 0) {
        printf("  [%s] 当前账户无效\n", self->name);
        return -1;
    }

    printf("  [%s] 当前账户 ID=%d，余额: %.2f 元\n", self->name, id, balance);
    account_list_all();
    transaction_print_history(id);
    return 0;
}

static int query_stop(Plugin* self)
{
    (void)self;
    return 0;
}

static void query_cleanup(Plugin* self)
{
    (void)self;
}

static Plugin g_query_plugin = {
    .name        = "查询",
    .version     = "1.0",
    .description = "查询余额与交易流水",
    .menu_id     = 3,
    .menu_label  = "查询余额",
    .need_amount = 0,
    .init        = query_init,
    .start       = query_start,
    .execute     = query_execute,
    .stop        = query_stop,
    .cleanup     = query_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED
};

Plugin* query_plugin_create(void)
{
    return &g_query_plugin;
}

#ifdef PLUGIN_DLL
PLUGIN_EXPORT Plugin* get_plugin(void)
{
    return &g_query_plugin;
}
#endif
