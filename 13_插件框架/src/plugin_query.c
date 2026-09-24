/*
 * ============================================================
 *  第13讲：插件框架架构
 *  plugin_query.c —— 内置插件：查询余额
 * ============================================================
 *
 *  【一个"只要读、不要写"的插件】
 *    它的 execute 忽略 amount 参数（用户输 0 即可）。
 *    为什么签名里还有 amount？因为 Plugin 接口是统一的：
 *    框架用同一句话调用所有插件，不能为某个插件开小灶。
 *    这就是"统一契约"的代价，也是它的价值。
 *
 *  【展示 user_data 的用法】
 *    查询次数存在 user_data 指向的堆内存里，
 *    在 init 中申请、cleanup 中释放——
 *    完整演示"谁申请、谁释放"的资源闭环。
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "framework.h"
#include "atm_state.h"
#include "plugins.h"

/* 私有数据结构：只有本插件知道它的存在 */
typedef struct {
    int query_count;    /* 本插件被调用了多少次 */
} QueryPrivate;

static int query_init(Plugin* self)
{
    /* init 阶段申请私有资源，挂在 user_data 上 */
    QueryPrivate* priv = (QueryPrivate*)malloc(sizeof(QueryPrivate));
    if (priv == NULL) {
        printf("  [%-6s] init    : 失败，内存不足\n", self->name);
        return -1;          /* 返回非 0 = 初始化失败 */
    }
    priv->query_count = 0;
    self->user_data = priv;

    printf("  [%-6s] init    : 分配私有数据 %d 字节，准备就绪\n",
           self->name, (int)sizeof(QueryPrivate));
    return 0;
}

static int query_start(Plugin* self)
{
    printf("  [%-6s] start   : 余额查询服务上线\n", self->name);
    return 0;
}

static int query_execute(Plugin* self, double amount)
{
    QueryPrivate* priv = (QueryPrivate*)self->user_data;

    (void)amount;   /* 查询不需要金额，显式忽略，避免编译警告 */

    if (priv != NULL) {
        priv->query_count++;
        printf("  [%-6s] 当前余额 %8.2f 元（第 %d 次查询）\n",
               self->name, atm_get_balance(), priv->query_count);
    } else {
        printf("  [%-6s] 当前余额 %8.2f 元\n",
               self->name, atm_get_balance());
    }
    return 0;
}

static int query_stop(Plugin* self)
{
    printf("  [%-6s] stop    : 余额查询服务下线\n", self->name);
    return 0;
}

static void query_cleanup(Plugin* self)
{
    /* cleanup 阶段释放 init 里申请的资源，防止内存泄漏 */
    if (self->user_data != NULL) {
        free(self->user_data);
        self->user_data = NULL;
        printf("  [%-6s] cleanup : 私有数据已释放\n", self->name);
    } else {
        printf("  [%-6s] cleanup : 无需释放\n", self->name);
    }
}

static Plugin query_plugin = {
    .name        = "查询余额",
    .version     = "1.1",
    .description = "查询账户当前余额",
    .menu_id     = 3,
    .menu_label  = "查询余额",
    .init        = query_init,
    .start       = query_start,
    .execute     = query_execute,
    .stop        = query_stop,
    .cleanup     = query_cleanup,
    .user_data   = NULL,
    .state       = PLUGIN_UNLOADED,
};

Plugin* create_query_plugin(void)
{
    return &query_plugin;
}
