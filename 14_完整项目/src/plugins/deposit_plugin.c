/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  plugins/deposit_plugin.c —— 存款插件
 * ============================================================
 *
 *  一个"标准插件"的完整写法：
 *    1. 实现五阶段生命周期（init/start/execute/stop/cleanup）
 *    2. 填好元数据（名称/版本/描述/菜单号/菜单文字/是否需要金额）
 *    3. 提供一个 create() 工厂函数 + 可选的 get_plugin 导出
 *
 *  插件内部只调用 atmcore.dll 暴露的账务接口，
 *  完全不接触 UI 和主循环——这就是"插件只关心自己的业务"。
 *
 *  编译成 DLL：gcc -shared -DPLUGIN_DLL ... （见 build.bat）
 * ============================================================
 */

#include "plugin.h"
#include "account.h"
#include "transaction.h"
#include "plugins.h"

#include <stdio.h>

/* ---- 生命周期：初始化（分配资源）---- */
static int deposit_init(Plugin* self)
{
    /* 存款插件没有额外资源，直接成功 */
    (void)self;
    return 0;
}

/* ---- 生命周期：启动（挂载服务/菜单）---- */
static int deposit_start(Plugin* self)
{
    (void)self;
    return 0;
}

/* ---- 核心业务：执行存款 ----
 *   框架按 need_amount=1 的约定，先把金额读进来再调用这里。
 */
static int deposit_execute(Plugin* self, double amount)
{
    int id = account_current_id();
    double balance;

    if (amount <= 0) {
        printf("  [%s] 存款金额必须大于 0\n", self->name);
        return -1;
    }

    /* 走交易模块：入账 + 记一笔流水 */
    balance = transaction_deposit(id, amount);
    if (balance < 0) {
        printf("  [%s] 存款失败\n", self->name);
        return -2;
    }
    printf("  [%s] 存款成功，账户 %d 当前余额: %.2f\n", self->name, id, balance);
    return 0;
}

/* ---- 生命周期：停止 ---- */
static int deposit_stop(Plugin* self)
{
    (void)self;
    return 0;
}

/* ---- 生命周期：清理 ---- */
static void deposit_cleanup(Plugin* self)
{
    (void)self;
}

/* ---- 插件实例（实现了 Plugin 接口）---- */
static Plugin g_deposit_plugin = {
    .name        = "存款",
    .version     = "1.0",
    .description = "向当前账户存入现金",
    .menu_id     = 1,
    .menu_label  = "存款",
    .need_amount = 1,
    .init        = deposit_init,
    .start       = deposit_start,
    .execute     = deposit_execute,
    .stop        = deposit_stop,
    .cleanup     = deposit_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED
};

/* 工厂函数：内置回退与动态库都用它拿到实例 */
Plugin* deposit_plugin_create(void)
{
    return &g_deposit_plugin;
}

/* 只有作为动态库编译时，才导出框架约定的入口符号 */
#ifdef PLUGIN_DLL
PLUGIN_EXPORT Plugin* get_plugin(void)
{
    return &g_deposit_plugin;
}
#endif
