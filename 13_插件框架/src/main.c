/*
 * ============================================================
 *  第13讲：插件框架架构
 *  main.c —— 框架入口（主程序）
 * ============================================================
 *
 *  【请仔细看这个文件：它小得可疑】
 *
 *    三行搞定一切：
 *      framework_start();   ← 初始化 + 注册 + init + start
 *      framework_run();     ← 显示菜单 + 交互循环
 *      framework_stop();    ← stop + cleanup + destroy
 *
 *    通篇没有出现"存款""取款""查询余额""转账"，
 *    没有 printf("1. 存款")，没有 switch(choice) 分发。
 *
 *    这就是"框架 vs 库"最直观的体现：
 *      库：主程序是导演，一步步调用库函数（你调用它）
 *      框架：主程序只是"启动器"，剩下的时机由框架决定
 *            （它调用你）——控制反转 IoC。
 *
 *  编译运行（Windows）：
 *    build.bat
 *  编译运行（Linux / MinGW）：
 *    make
 *    make run
 *  手工编译：
 *    gcc -Wall -o plugin_framework.exe framework.c atm_state.c \
 *        plugin_deposit.c plugin_withdraw.c plugin_query.c \
 *        plugin_transfer.c main.c
 * ============================================================
 */

#include <stdio.h>
#include "framework.h"

int main(void)
{
    /* ① 启动框架：管理器 + 菜单 + 注册插件 + init + start */
    if (framework_start() != 0) {
        printf("\n[main] 框架启动失败，程序退出\n");
        return 1;
    }

    /* ② 运行框架：框架负责显示菜单、读输入、回调插件 */
    framework_run();

    /* ③ 停止框架：stop + cleanup + destroy，资源全部回收 */
    framework_stop();

    /* ---------- 本讲核心收获 ---------- */
    printf("\n==============================================\n");
    printf("            第13讲 核心收获\n");
    printf("==============================================\n");
    printf("  1. 生命周期：UNLOADED -> LOADED -> INITIALIZED\n");
    printf("               -> STARTED -> STOPPED -> CLEANED -> UNLOADED\n");
    printf("  2. 插件管理器：链表 + 批量 init/start/stop/cleanup\n");
    printf("  3. 扩展点：菜单项 / 命令 / 事件，都由插件动态挂载\n");
    printf("  4. 配置化菜单：菜单项 = 链表节点（第8讲链表的实战）\n");
    printf("  5. 开闭原则：新增插件零改动主程序\n");
    printf("  6. 框架 vs 库：库是你调用它，框架是它调用你（IoC）\n");
    printf("==============================================\n");

    return 0;
}
