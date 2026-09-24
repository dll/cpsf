/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  plugins/withdraw_plugin.c —— 取款插件
 * ============================================================
 *
 *  与存款插件结构完全一样，但业务逻辑不同：
 *    存款：金额必须 > 0
 *    取款：金额必须 > 0 且 不能超过余额
 *
 *  【要点】
 *    两个插件对框架而言"长得一模一样"（都是 Plugin 接口），
 *    框架用同一行 p->execute(p, amount) 调用它们，
 *    具体怎么做由插件自己的实现决定——这就是 C 语言的多态。
 * ============================================================
 */

#include "plugin.h"
#include "account.h"
#include "transaction.h"
#include "plugins.h"

#include <stdio.h>

static int withdraw_init(Plugin* self)
{
    (void)self;
    return 0;
}

static int withdraw_start(Plugin* self)
{
    (void)self;
    return 0;
}

static int withdraw_execute(Plugin* self, double amount)
{
    int id = account_current_id();
    double balance;

    if (amount <= 0) {
        printf("  [%s] 取款金额必须大于 0\n", self->name);
        return -1;
    }

    balance = transaction_withdraw(id, amount);
    if (balance < 0) {
        /* 账户模块已打印"余额不足"的具体原因 */
        printf("  [%s] 取款失败\n", self->name);
        return -2;
    }
    printf("  [%s] 取款成功，账户 %d 当前余额: %.2f\n", self->name, id, balance);
    return 0;
}

static int withdraw_stop(Plugin* self)
{
    (void)self;
    return 0;
}

static void withdraw_cleanup(Plugin* self)
{
    (void)self;
}

static Plugin g_withdraw_plugin = {
    .name        = "取款",
    .version     = "1.0",
    .description = "从当前账户取出现金",
    .menu_id     = 2,
    .menu_label  = "取款",
    .need_amount = 1,
    .init        = withdraw_init,
    .start       = withdraw_start,
    .execute     = withdraw_execute,
    .stop        = withdraw_stop,
    .cleanup     = withdraw_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED
};

Plugin* withdraw_plugin_create(void)
{
    return &g_withdraw_plugin;
}

#ifdef PLUGIN_DLL
PLUGIN_EXPORT Plugin* get_plugin(void)
{
    return &g_withdraw_plugin;
}
#endif
