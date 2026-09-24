/*
 * ============================================================
 *  第11讲：运行时加载
 *  host.c —— ATM 插件宿主程序（扫描目录 → 加载 → 调用 → 卸载）
 * ============================================================
 *
 *  【本程序要演示的完整流程】
 *
 *     ┌───────────────┐
 *     │  扫描 plugins │  ① 打开目录，逐个读文件名，筛出 .dll/.so
 *     │     目录       │
 *     └───────┬───────┘
 *             ▼
 *     ┌───────────────┐
 *     │ dynlib_open   │  ② 运行时把动态库加载进本进程
 *     └───────┬───────┘
 *             ▼
 *     ┌───────────────┐
 *     │ dynlib_sym    │  ③ 按约定名字取出 plugin_name / plugin_execute
 *     └───────┬───────┘
 *             ▼
 *     ┌───────────────┐
 *     │  调用函数     │  ④ 把它当函数指针直接调用
 *     └───────┬───────┘
 *             ▼
 *     ┌───────────────┐
 *     │ dynlib_close  │  ⑤ 用完卸载，释放内存
 *     └───────────────┘
 *
 *  【和第10讲最大的区别】
 *    第10讲：exe 的导入表里写死了 account.dll，
 *            程序一启动操作系统就去找，找不到直接起不来。
 *    第11讲：exe 启动时不认识任何插件，
 *            是 main 里自己主动去"发现 → 加载 → 调用 → 卸载"。
 *            plugins 目录里放几个库，程序就加载几个；
 *            放一个新库进去，不用改一行代码，也不用重新编译！
 *
 *  【为什么这已经是"插件雏形"】
 *    因为宿主不再"认识"具体的插件了，它只认约定：
 *      只要某个动态库导出了 plugin_name + plugin_execute，
 *      宿主就能把它当插件加载并调用。
 *    新增功能 = 往 plugins 目录里丢一个 .dll，这就是插件系统的起点。
 *
 *  编译：
 *    Windows: gcc -Wall -Wextra -o host.exe host.c
 *    Linux  : gcc -Wall -Wextra -o host host.c -ldl
 * ============================================================
 */

#include "dynlib.h"
#include "plugin_api.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ------------------------------------------------------------
 *  平台相关的目录扫描准备
 * ------------------------------------------------------------
 *  Windows 用 <io.h> 里的 _findfirst / _findnext / _findclose
 *  Linux   用 <dirent.h> 里的 opendir  / readdir   / closedir
 *
 *  【对比】两套 API 干的是同一件事：枚举目录里的文件名。
 *    统一封装的意义，和 dynlib.h 是一样的——把平台的差异
 *    隔离在一个小角落里，其余逻辑只写一遍。
 */
#ifdef _WIN32
    #include <io.h>
    #define PLUGIN_DIR      "plugins"
    #define PLUGIN_SEP      '\\'
    #define PLUGIN_PATTERN  "plugins\\*.dll"    /* 只匹配 .dll */
    #define PLUGIN_EXT      ".dll"
#else
    #include <dirent.h>
    #include <unistd.h>
    #define PLUGIN_DIR      "plugins"
    #define PLUGIN_SEP      '/'
    #define PLUGIN_EXT      ".so"
#endif

#include "console_utf8.h"     /* 解决 Windows 控制台中文乱码（UTF-8） */

#define MAX_PLUGIN_FILES 64        /* 最多扫描多少个插件文件 */
#define MAX_PATH_LEN     512

/* ============================================================
 *  load_and_call —— 加载一个动态库，调用它的插件入口
 * ============================================================
 *
 *  返回 0 表示"成功当插件跑了一遍"，-1 表示跳过（已打印原因）。
 *
 *  注意这里的顺序：任何一步失败，都必须先 dlclose 再返回，
 *  否则加载成功的库会被"泄漏"在进程里一直不卸载。
 */
static int load_and_call(const char *path, double amount)
{
    dynlib_handle handle;
    plugin_name_fn    get_name;
    plugin_execute_fn execute;
    const char       *name;

    printf("  发现文件：%s\n", path);

    /* ---- ① 运行时加载动态库 ---- */
    handle = dynlib_open(path);
    if (handle == DYNLIB_INVALID) {
        printf("    ✗ 加载失败（已优雅跳过）：%s\n", dynlib_error());
        return -1;
    }

    /* ---- ② 按约定名字取符号 ---- */
    /* 先取 plugin_name（可选，只用来打印名字） */
    get_name = (plugin_name_fn)dynlib_sym(handle, PLUGIN_SYM_NAME);

    /* 再取 plugin_execute（必需，没有它就不是合格插件） */
    execute = (plugin_execute_fn)dynlib_sym(handle, PLUGIN_SYM_EXECUTE);

    if (execute == NULL) {
        /* 关键：取不到符号不是程序 bug，而是这个文件不合规。
           宿主必须把它当正常情况处理，优雅跳过，绝不能直接调用。 */
        printf("    ✗ 该文件缺少约定符号 \"%s\"，不是合法插件，已跳过\n",
               PLUGIN_SYM_EXECUTE);
        dynlib_close(handle);
        return -1;
    }

    /* ---- ③ 调用 ---- */
    name = (get_name != NULL) ? get_name() : "(未提供名字)";
    printf("    → 加载成功，插件名字：%s\n", name);
    printf("    → 调用 plugin_execute(%.2f)：\n", amount);
    execute(amount);                       /* 这里就是第5讲的函数指针调用 */

    /* ---- ④ 用完卸载 ---- */
    dynlib_close(handle);
    printf("    → 已卸载 %s\n", path);
    return 0;
}

/* ============================================================
 *  scan_and_load —— 扫描 plugins 目录，逐个加载调用
 * ============================================================
 *
 *  返回成功加载的插件个数。
 */
static int scan_and_load(double amount)
{
    char  files[MAX_PLUGIN_FILES][MAX_PATH_LEN];
    int   file_count = 0;
    int   i, j;
    int   ok_count = 0;

    printf("\n[步骤 1] 扫描插件目录：%s\n", PLUGIN_DIR);
    printf("------------------------------------------------------------\n");

#ifdef _WIN32
    /* ---------- Windows：_findfirst / _findnext ---------- */
    {
        struct _finddata_t fd;
        intptr_t hfile = _findfirst(PLUGIN_PATTERN, &fd);

        if (hfile == -1) {
            /* 目录不存在，或者目录里一个 .dll 都没有 */
            if (_access(PLUGIN_DIR, 0) != 0) {
                printf("  提示：目录 \"%s\" 不存在。\n", PLUGIN_DIR);
                printf("        请先运行 build.bat 生成插件，或手动创建该目录。\n");
            } else {
                printf("  提示：目录 \"%s\" 存在，但没有发现 %s 插件。\n",
                       PLUGIN_DIR, PLUGIN_EXT);
            }
            return 0;
        }

        do {
            if (!(fd.attrib & _A_SUBDIR) && file_count < MAX_PLUGIN_FILES) {
                snprintf(files[file_count], MAX_PATH_LEN,
                         "%s%c%s", PLUGIN_DIR, PLUGIN_SEP, fd.name);
                file_count++;
            }
        } while (_findnext(hfile, &fd) == 0);

        _findclose(hfile);
    }
#else
    /* ---------- Linux：opendir / readdir ---------- */
    {
        DIR           *dir;
        struct dirent *entry;
        size_t         ext_len = strlen(PLUGIN_EXT);

        dir = opendir(PLUGIN_DIR);
        if (dir == NULL) {
            printf("  提示：目录 \"%s\" 不存在。\n", PLUGIN_DIR);
            printf("        请先运行 make 生成插件，或手动创建该目录。\n");
            return 0;
        }

        while ((entry = readdir(dir)) != NULL) {
            size_t len = strlen(entry->d_name);
            if (len > ext_len &&
                strcmp(entry->d_name + (len - ext_len), PLUGIN_EXT) == 0) {
                if (file_count < MAX_PLUGIN_FILES) {
                    snprintf(files[file_count], MAX_PATH_LEN,
                             "%s%c%s", PLUGIN_DIR, PLUGIN_SEP, entry->d_name);
                    file_count++;
                }
            }
        }
        closedir(dir);
    }
#endif

    if (file_count == 0) {
        printf("  提示：目录 \"%s\" 里没有发现任何 %s 文件。\n",
               PLUGIN_DIR, PLUGIN_EXT);
        return 0;
    }

    /* 目录枚举顺序由操作系统决定，不稳定。
       这里按文件名排个序，保证每次运行输出一致，方便教学演示。 */
    for (i = 0; i < file_count - 1; i++) {
        for (j = 0; j < file_count - 1 - i; j++) {
            if (strcmp(files[j], files[j + 1]) > 0) {
                char tmp[MAX_PATH_LEN];
                memcpy(tmp, files[j], MAX_PATH_LEN);
                memcpy(files[j], files[j + 1], MAX_PATH_LEN);
                memcpy(files[j + 1], tmp, MAX_PATH_LEN);
            }
        }
    }

    printf("  共发现 %d 个候选插件文件\n\n", file_count);

    /* 逐个加载、调用、卸载 */
    for (i = 0; i < file_count; i++) {
        if (load_and_call(files[i], amount) == 0) {
            ok_count++;
        }
        printf("\n");
    }

    return ok_count;
}

/* ============================================================
 *  main —— 宿主程序主流程
 * ============================================================ */
int main(void)
{
    console_utf8_init();   /* 解决中文乱码：切换到 UTF-8 控制台 */
    double amount = 500.0;
    int    loaded;

#ifdef _WIN32
    /* Windows 控制台默认是 GBK 代码页，而本文件是 UTF-8 编码，
       不切换的话中文会显示成乱码。切到 UTF-8 代码页即可正常显示。 */
    SetConsoleOutputCP(65001);          /* 65001 = CP_UTF8 */
#endif

    printf("============================================================\n");
    printf("  第11讲：运行时加载 —— ATM 插件宿主程序\n");
    printf("============================================================\n");
    printf("  宿主启动时并不认识任何插件；\n");
    printf("  是下面的代码在运行中主动扫描、加载、调用、卸载。\n");
    printf("------------------------------------------------------------\n");

    /* ---------- 步骤 1：扫描目录，自动加载全部插件 ---------- */
    loaded = scan_and_load(amount);

    /* ---------- 步骤 2：演示错误处理——加载不存在的库 ---------- */
    printf("[步骤 2] 演示：故意加载一个不存在的库（看宿主怎么优雅报错）\n");
    printf("------------------------------------------------------------\n");
    {
        char bad_path[MAX_PATH_LEN];
        snprintf(bad_path, MAX_PATH_LEN,
                 "%s%c%s", PLUGIN_DIR, PLUGIN_SEP, "not_exist_plugin.dll");
        load_and_call(bad_path, amount);
    }
    printf("\n");

    /* ---------- 步骤 3：演示错误处理——找不到约定符号 ---------- */
    printf("[步骤 3] 演示：在正常库里查找一个不存在的符号\n");
    printf("------------------------------------------------------------\n");
    {
        char   good_path[MAX_PATH_LEN];
        dynlib_handle h;

        snprintf(good_path, MAX_PATH_LEN,
                 "%s%c%s", PLUGIN_DIR, PLUGIN_SEP, "deposit_plugin.dll");
        h = dynlib_open(good_path);
        if (h == DYNLIB_INVALID) {
            printf("  （跳过本演示：未找到 %s，请先构建插件）\n", good_path);
        } else {
            void *sym = dynlib_sym(h, "plugin_exectue"); /* 故意拼错 */
            printf("  在 %s 中查找符号 \"plugin_exectue\"（故意拼错）...\n",
                   good_path);
            if (sym == NULL) {
                printf("    ✗ 未找到（返回 NULL），宿主没有崩溃，正常继续。\n");
            } else {
                printf("    → 竟然找到了：%p\n", sym);
            }
            dynlib_close(h);
            printf("    → 已卸载\n");
        }
    }
    printf("\n");

    /* ---------- 收尾：打印统计 ---------- */
    printf("============================================================\n");
    printf("  运行结束：本轮成功加载并调用了 %d 个插件\n", loaded);
    printf("  所有插件都已卸载，宿主进程退出前不会留下任何库占用。\n");
    printf("============================================================\n");
    printf("\n");
    printf("  【本讲留下的新痛点】\n");
    printf("    宿主是靠字符串 \"plugin_execute(double)\" 硬编码去调用的：\n");
    printf("      - 查询插件根本不需要金额，却被迫接收 amount；\n");
    printf("      - 想加一个\"转账\"插件（要两个账户+金额），一个 double 不够；\n");
    printf("      - 每加一种能力，宿主都得改代码去认新的符号名。\n");
    printf("    → 只约定\"函数名\"还不够，还需要约定\"统一的接口\"。\n");
    printf("    → 这正是第12讲\"接口抽象\"要解决的问题。\n");
    printf("============================================================\n");

    return 0;
}
