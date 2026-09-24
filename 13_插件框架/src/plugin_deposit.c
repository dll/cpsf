/*
 * ============================================================
 *  第13讲：插件框架架构
 *  plugin_deposit.c —— 内置插件：存款
 * ============================================================
 *
 *  【插件模板：五阶段生命周期】
 *    init()    : 分配资源、准备数据（但还没对外服务）
 *    start()   : 开始提供服务（本讲由框架在 start_all 阶段调用）
 *    execute() : 真正的业务功能，可被反复调用
 *    stop()    : 停止服务（不再受理新请求）
 *    cleanup() : 释放资源，回到"干净"状态
 *
 *  对比第12讲：只有 init/execute/cleanup 三步，
 *  没法表达"已就绪但尚未对外服务"这个中间态。
 *
 *  【关键教学点】
 *    这个文件里没有一行"菜单"代码！
 *    菜单项由 menu_id / menu_label 描述，
 *    由框架在注册时自动挂到链表上。
 * ============================================================
 */

#include <stdio.h>
#include "framework.h"
#include "atm_state.h"
#include "plugins.h"

/* ---------- 生命周期实现 ---------- */

static int deposit_init(Plugin* self)
{
    /* init：只做"准备"，不做"服务" */
    printf("  [%-6s] init    : 分配资源，准备就绪\n", self->name);
    return 0;
}

static int deposit_start(Plugin* self)
{
    /* start：开始提供服务（菜单项已在注册阶段由框架挂载） */
    printf("  [%-6s] start   : 开始受理存款请求\n", self->name);
    return 0;
}

static int deposit_execute(Plugin* self, double amount)
{
    if (amount <= 0) {
        printf("  [%-6s] 错误：存款金额必须大于 0\n", self->name);
        return -1;
    }
    atm_deposit(amount);
    printf("  [%-6s] 存入 %8.2f 元，余额 %8.2f 元\n",
           self->name, amount, atm_get_balance());
    return 0;
}

static int deposit_stop(Plugin* self)
{
    printf("  [%-6s] stop    : 停止受理存款请求\n", self->name);
    return 0;
}

static void deposit_cleanup(Plugin* self)
{
    printf("  [%-6s] cleanup : 资源已释放\n", self->name);
}

/* ---------- 插件实例（实现 Plugin 接口） ---------- */

static Plugin deposit_plugin = {
    .name        = "存款",
    .version     = "1.1",
    .description = "向账户存入现金",
    .menu_id     = 1,
    .menu_label  = "存款",
    .init        = deposit_init,
    .start       = deposit_start,
    .execute     = deposit_execute,
    .stop        = deposit_stop,
    .cleanup     = deposit_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED,
};

/* ---------- 工厂函数 ---------- */

Plugin* create_deposit_plugin(void)
{
    return &deposit_plugin;
}
