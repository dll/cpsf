/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  plugins/transfer_plugin.c —— 转账插件
 * ============================================================
 *
 *  【与前几个插件的不同点：参数不止一个】
 *    转账需要"目标账户 + 金额"两个参数，
 *    而框架统一只传一个 double。怎么办？两种思路：
 *
 *    思路A：把接口改成 execute(self, amount, target) ——
 *           所有插件都得改签名，接口变复杂。
 *    思路B：把 need_amount 设为 0，插件自己读它需要的输入 ——
 *           接口保持简单，多大参数都由插件自己负责。
 *
 *    本讲选 B：接口保持"最小公约数"，
 *    插件需要什么交互，就自己完成什么交互。
 *    这也是真实插件系统（如 VS Code 插件）的常见做法。
 * ============================================================
 */

#include "plugin.h"
#include "account.h"
#include "transaction.h"
#include "plugins.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int transfer_init(Plugin* self)
{
    (void)self;
    return 0;
}

static int transfer_start(Plugin* self)
{
    (void)self;
    return 0;
}

/* 转账：从当前账户转到指定账户 */
static int transfer_execute(Plugin* self, double amount)
{
    int from = account_current_id();
    int to;
    double amt;
    char line[64];

    (void)amount;   /* 转账需要的两个参数都由插件自己读取 */

    printf("  [%s] 从账户 %d 转出，请输入目标账户ID: ", self->name, from);
    if (fgets(line, sizeof(line), stdin) == NULL) {
        return -1;
    }
    to = atoi(line);

    printf("  [%s] 请输入转账金额: ", self->name);
    if (fgets(line, sizeof(line), stdin) == NULL) {
        return -1;
    }
    amt = atof(line);

    if (!transaction_transfer(from, to, amt)) {
        printf("  [%s] 转账失败\n", self->name);
        return -2;
    }
    printf("  [%s] 转账成功，账户 %d 当前余额: %.2f\n",
           self->name, from, account_get_balance(from));
    return 0;
}

static int transfer_stop(Plugin* self)
{
    (void)self;
    return 0;
}

static void transfer_cleanup(Plugin* self)
{
    (void)self;
}

static Plugin g_transfer_plugin = {
    .name        = "转账",
    .version     = "1.0",
    .description = "在当前账户与目标账户之间转账",
    .menu_id     = 4,
    .menu_label  = "转账",
    .need_amount = 0,   /* 参数自取：目标账户 + 金额 */
    .init        = transfer_init,
    .start       = transfer_start,
    .execute     = transfer_execute,
    .stop        = transfer_stop,
    .cleanup     = transfer_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED
};

Plugin* transfer_plugin_create(void)
{
    return &g_transfer_plugin;
}

#ifdef PLUGIN_DLL
PLUGIN_EXPORT Plugin* get_plugin(void)
{
    return &g_transfer_plugin;
}
#endif
