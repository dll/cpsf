/*
 * ============================================================
 *  第13讲：插件框架架构
 *  plugin_transfer.c —— 内置插件：转账
 * ============================================================
 *
 *  【演示"新插件零改动接入"】
 *    转账是本讲相对第12讲新增的功能。
 *    为了把它加进系统，我们改了什么？
 *      1. 新建 plugin_transfer.c（新文件）
 *      2. 在 plugins.h 里加一行函数声明
 *      3. 在 framework_start() 里加一行 manager_register()
 *    framework.c 的其它代码、menu_show()、menu_handle()、
 *    main.c —— 一行都没改！
 *
 *    这就是"对扩展开放、对修改关闭"（开闭原则）。
 *    第12讲想加个功能，得改 menu_handle 里的 switch，
 *    那叫"对修改开放"，越加越乱。
 * ============================================================
 */

#include <stdio.h>
#include "framework.h"
#include "atm_state.h"
#include "plugins.h"

static int transfer_init(Plugin* self)
{
    printf("  [%-6s] init    : 加载转账清算规则，准备就绪\n", self->name);
    return 0;
}

static int transfer_start(Plugin* self)
{
    printf("  [%-6s] start   : 转账通道开启\n", self->name);
    return 0;
}

static int transfer_execute(Plugin* self, double amount)
{
    int rc;

    if (amount <= 0) {
        printf("  [%-6s] 错误：转账金额必须大于 0\n", self->name);
        return -1;
    }

    rc = atm_transfer(amount);
    if (rc == -2) {
        printf("  [%-6s] 错误：余额不足！当前余额 %8.2f 元\n",
               self->name, atm_get_balance());
        return -2;
    }

    printf("  [%-6s] 转出 %8.2f 元，本账户余额 %8.2f 元，收款方累计 %8.2f 元\n",
           self->name, amount, atm_get_balance(), atm_get_target());
    return 0;
}

static int transfer_stop(Plugin* self)
{
    printf("  [%-6s] stop    : 转账通道关闭\n", self->name);
    return 0;
}

static void transfer_cleanup(Plugin* self)
{
    printf("  [%-6s] cleanup : 资源已释放\n", self->name);
}

static Plugin transfer_plugin = {
    .name        = "转账",
    .version     = "1.0",
    .description = "向他人账户转账",
    .menu_id     = 4,
    .menu_label  = "转账",
    .init        = transfer_init,
    .start       = transfer_start,
    .execute     = transfer_execute,
    .stop        = transfer_stop,
    .cleanup     = transfer_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED,
};

Plugin* create_transfer_plugin(void)
{
    return &transfer_plugin;
}
