/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  main.c —— 框架入口（全系列知识的总装车间）
 * ============================================================
 *
 *  【全系列的终点，就在这三行里】
 *
 *      framework_start();   // 加载 + 注册 + init + start
 *      framework_run();     // 菜单交互循环
 *      framework_stop();    // stop + cleanup + 卸载
 *
 *  注意：main() 里没有任何一处写着"存款/取款/查询/转账"。
 *  业务功能全部来自插件，加一个新功能只需要：
 *      往 plugins/ 里丢一个实现了 Plugin 接口的 DLL，
 *      主程序一行都不用改。
 *  这就是"开闭原则"：对扩展开放，对修改关闭。
 *
 *  【控制反转（IoC）在这里落地】
 *     不是 main 调用业务代码，而是 main 把控制权交给框架，
 *     再由框架回调插件。控制权反转，是框架与库的分水岭。
 * ============================================================
 */

#include <stdio.h>

#include "framework.h"
#include "plugins.h"

int main(void)
{
    /*
     * 登记"内置回退插件"。
     * 正常情况下，它们会被 plugins/ 目录里的同名 DLL 取代；
     * 一旦某个 DLL 缺失或加载失败，框架自动启用这里的实现，
     * 并打印一行 [降级] 说明——课堂上可以故意删掉一个 DLL 来演示。
     */
    Plugin* builtins[4];
    builtins[0] = deposit_plugin_create();
    builtins[1] = withdraw_plugin_create();
    builtins[2] = query_plugin_create();
    builtins[3] = transfer_plugin_create();
    framework_set_builtins(builtins, 4);

    /* 框架三段式：启动 → 运行 → 停止 */
    framework_start();
    framework_run();
    framework_stop();

    return 0;
}
