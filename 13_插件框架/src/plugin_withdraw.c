/*
 * ============================================================
 *  第13讲：插件框架架构
 *  plugin_withdraw.c —— 内置插件：取款
 * ============================================================
 *
 *  【和第12讲的差异】
 *    第12讲只有 init/execute/cleanup，连"余额不足"都只能靠返回值约定。
 *    本讲多了 start/stop 两个阶段，插件可以表达：
 *      "我已初始化，但还没开始对外服务"
 *      "我已停止服务，但资源还没释放"
 *
 *  【注意】插件内部完全不需要知道框架的存在，
 *    它只实现 5 个函数指针，剩下的事交给管理器。
 *    这就是"依赖倒置"：框架和插件都依赖 Plugin 接口，
 *    谁都不依赖谁的具体实现。
 * ============================================================
 */

#include <stdio.h>
#include "framework.h"
#include "atm_state.h"
#include "plugins.h"

static int withdraw_init(Plugin* self)
{
    printf("  [%-6s] init    : 分配资源，准备就绪\n", self->name);
    return 0;
}

static int withdraw_start(Plugin* self)
{
    printf("  [%-6s] start   : 开始受理取款请求\n", self->name);
    return 0;
}

static int withdraw_execute(Plugin* self, double amount)
{
    int rc;

    if (amount <= 0) {
        printf("  [%-6s] 错误：取款金额必须大于 0\n", self->name);
        return -1;
    }

    rc = atm_withdraw(amount);
    if (rc == -2) {
        printf("  [%-6s] 错误：余额不足！当前余额 %8.2f 元\n",
               self->name, atm_get_balance());
        return -2;
    }

    printf("  [%-6s] 取出 %8.2f 元，余额 %8.2f 元\n",
           self->name, amount, atm_get_balance());
    return 0;
}

static int withdraw_stop(Plugin* self)
{
    printf("  [%-6s] stop    : 停止受理取款请求\n", self->name);
    return 0;
}

static void withdraw_cleanup(Plugin* self)
{
    printf("  [%-6s] cleanup : 资源已释放\n", self->name);
}

static Plugin withdraw_plugin = {
    .name        = "取款",
    .version     = "1.1",
    .description = "从账户取出现金",
    .menu_id     = 2,
    .menu_label  = "取款",
    .init        = withdraw_init,
    .start       = withdraw_start,
    .execute     = withdraw_execute,
    .stop        = withdraw_stop,
    .cleanup     = withdraw_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED,
};

Plugin* create_withdraw_plugin(void)
{
    return &withdraw_plugin;
}
