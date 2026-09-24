/*
 * ============================================================
 *  第11讲：运行时加载
 *  dynlib.h —— 跨平台动态库加载封装（Linux 用 dlfcn.h）
 * ============================================================
 *
 *  【本讲要解决什么问题】
 *    第10讲的动态库是"加载时链接"：程序一启动，
 *    操作系统就必须把所有依赖的 .dll/.so 找齐，
 *    找不到就直接报错，程序根本起不来。
 *
 *    这种"死依赖"太不灵活了——我们想要的是：
 *    程序跑着跑着，需要某个功能时才去加载对应的库，
 *    用完还能把它从内存里卸载出去。
 *
 *    这就是"运行时加载"（run-time loading）：
 *    ★ 什么时候加载？——程序自己决定，不是操作系统开机就加载
 *    ★ 加载哪一个？——程序运行时按名字去挑
 *    ★ 用完怎么办？——可以直接卸载，内存释放
 *
 *  【核心 API 对照】（两套平台，一套心思）
 *    ┌───────────────┬──────────────────────┬───────────────────────────────┐
 *    │ 作用          │ Linux（dlfcn.h）      │ Windows（windows.h）           │
 *    ├───────────────┼──────────────────────┼───────────────────────────────┤
 *    │ 打开动态库    │ dlopen(path, RTLD_*) │ LoadLibraryA(path)            │
 *    │ 按名找符号    │ dlsym(handle, name)  │ GetProcAddress(handle, name)  │
 *    │ 关闭/卸载     │ dlclose(handle)      │ FreeLibrary(handle)           │
 *    │ 取错误信息    │ dlerror()            │ GetLastError() + FormatMessage│
 *    └───────────────┴──────────────────────┴───────────────────────────────┘
 *
 *    一句话：Linux 的 dlopen 就是 Windows 的 LoadLibrary，
 *            dlsym 就是 GetProcAddress，dlclose 就是 FreeLibrary。
 *
 *  【为什么要有这个头文件？】
 *    如果直接把两套 API 写进 host.c，代码里就到处是 #ifdef，
 *    既难读又难维护。所以我们把平台差异"关"在 dynlib.h 里，
 *    对外只暴露 dynlib_open / dynlib_sym / dynlib_close 三个函数——
 *    业务代码看起来就是一套统一的接口，无需关心底层是哪个平台。
 *
 *    这正是"封装"思想：把变化的部分隔离在最小的范围内。
 *
 *  【对比第10讲】
 *    第10讲：链接时把 dll 登记在 exe 的导入表里（死依赖）
 *    第11讲：运行中随时 dlopen/LoadLibrary（活依赖、可插拔）
 *
 *  【使用方式】
 *    #include "dynlib.h"
 *    dynlib_handle h = dynlib_open("plugins/deposit_plugin.dll");
 *    plugin_execute_fn f = (plugin_execute_fn)dynlib_sym(h, "plugin_execute");
 *    f(500.0);
 *    dynlib_close(h);
 * ============================================================
 */

#ifndef DYNLIB_H
#define DYNLIB_H

/* ============================================================
 *  一、平台头文件与句柄类型
 * ============================================================
 *
 *  【什么是"句柄"（handle）？】
 *    它其实就是"操作系统给你的一张提货单"。
 *    你调用 dlopen/LoadLibrary 打开一个动态库时，
 *    操作系统把这块库在内存里的信息登记好，
 *    然后给你一个不透明的编号（句柄）。
 *
 *    你拿着这个句柄，就能：
 *      - 用它去 dlsym/GetProcAddress 查函数
 *      - 最后用它去 dlclose/FreeLibrary 归还资源
 *
 *    句柄的具体内容你不需要知道（它可能是指针、可能是下标），
 *    只需要"拿着它办事"就行。这跟第7讲的文件指针 FILE*、
 *    第5讲的指针本质是相通的——都是"代表某个资源的凭证"。
 *
 *    Linux：dlopen 返回 void*（一个指向内部结构体的指针）
 *    Windows：LoadLibrary 返回 HMODULE（本质也是 void*）
 *    所以我们用 typedef 统一成 dynlib_handle。
 */
#ifdef _WIN32
    /* ---- Windows 平台 ---- */
    #include <windows.h>
    typedef HMODULE dynlib_handle;          /* LoadLibrary 返回的模块句柄 */
    #define DYNLIB_INVALID NULL             /* 打开失败时返回 NULL */
#else
    /* ---- Linux / macOS 平台 ---- */
    #include <dlfcn.h>
    typedef void *dynlib_handle;            /* dlopen 返回的不透明指针 */
    #define DYNLIB_INVALID NULL             /* 打开失败时返回 NULL */
#endif

#include <stdio.h>

/* ============================================================
 *  二、dynlib_open —— 打开（加载）动态库
 * ============================================================
 *
 *  原始写法对照：
 *
 *    Linux:
 *      void *h = dlopen("libaccount.so", RTLD_LAZY);
 *      // RTLD_LAZY：用到符号时才解析（默认，快）
 *      // RTLD_NOW ：立刻解析全部符号（严格，能早发现问题）
 *      // RTLD_GLOBAL：该库的符号可以被后续加载的库共享
 *      if (h == NULL) fprintf(stderr, "%s\n", dlerror());
 *
 *    Windows:
 *      HMODULE h = LoadLibraryA("account.dll");
 *      // 传的路径可以只有文件名，此时会去 exe 所在目录
 *      // 和系统 PATH 里找；传全路径最保险。
 *      if (h == NULL) { ... }        // 可用 GetLastError() 取错误码
 *
 *  参数 path：动态库的路径（如 "plugins/deposit_plugin.dll"）
 *  返回     ：成功返回句柄，失败返回 NULL（可调 dynlib_error 看原因）
 */
static inline dynlib_handle dynlib_open(const char *path)
{
#ifdef _WIN32
    return LoadLibraryA(path);
#else
    /* RTLD_LAZY：延迟解析符号，加载更快；插件场景够用 */
    return dlopen(path, RTLD_LAZY);
#endif
}

/* ============================================================
 *  三、dynlib_sym —— 按名字查找函数（符号）
 * ============================================================
 *
 *  【为什么能"按名字找函数"？】
 *    动态库被编译出来时，里面除了机器指令，还带一张"符号表"
 *    （就是我们第9讲用 nm 看的那种 T 开头的符号）。
 *    每导出（export）一个函数，符号表里就登记一条：
 *      "名字 plugin_execute" → "代码在库里的偏移地址"
 *
 *    dlsym/GetProcAddress 就是拿名字去查这张表，
 *    查到就返回该函数在内存中的入口地址（函数指针）。
 *
 *    所以我们才能先加载库、再按名字"捞"出函数，
 *    然后在 C 语言里把它当函数指针直接调用。
 *
 *  原始写法对照：
 *    Linux:
 *      void (*f)(double) = (void (*)(double))dlsym(h, "plugin_execute");
 *      // 注意：dlsym 返回 void*，要转成正确的函数指针类型
 *
 *    Windows:
 *      FARPROC p = GetProcAddress(h, "plugin_execute");
 *      // FARPROC 是函数指针，需要再转成具体的函数指针类型
 *
 *  参数 handle：dynlib_open 返回的句柄
 *  参数 name  ：符号（函数）名字，区分大小写
 *  返回      ：成功返回符号地址（需转换成函数指针），失败返回 NULL
 *
 *  【重要提醒】
 *    C 语言的函数名默认就是符号名；但如果编译器加了前缀（如
 *    Windows 32 位下的下划线 _），或者用 C++ 编译（名字被
 *    mangle 成一长串），名字就对不上了。所以插件必须约定
 *    用 C 编译、用固定的函数名（详见 plugin_api.h）。
 */
static inline void *dynlib_sym(dynlib_handle handle, const char *name)
{
#ifdef _WIN32
    /* GetProcAddress 返回 FARPROC（函数指针），转成 void* 返回 */
    return (void *)GetProcAddress(handle, name);
#else
    return dlsym(handle, name);
#endif
}

/* ============================================================
 *  四、dynlib_close —— 关闭（卸载）动态库
 * ============================================================
 *
 *  【为什么这里能"卸载"，而第10讲的 dll 不能？】
 *    因为加载时链接的库，是程序启动就由操作系统加载的，
 *    它的生命周期跟着整个进程，程序不退出就一直占着。
 *    而运行时加载的库是我们自己动手加载的，
 *    我们就能自己动手把它卸载——引用计数减到 0，内存就还回去。
 *
 *    注意：卸载前必须确保不再调用库里任何函数，
 *    否则那些函数的代码已被移出内存，调用就是野指针——
 *    程序会直接崩溃（访问违规 Access Violation / 段错误 Segfault）。
 *
 *  原始写法对照：
 *    Linux:   dlclose(handle);
 *    Windows: FreeLibrary(handle);
 */
static inline void dynlib_close(dynlib_handle handle)
{
    if (handle == DYNLIB_INVALID) {
        return;                         /* 空句柄直接忽略，防止误关 */
    }
#ifdef _WIN32
    FreeLibrary(handle);
#else
    dlclose(handle);
#endif
}

/* ============================================================
 *  五、dynlib_error —— 取最近的错误信息
 * ============================================================
 *
 *  打开库失败、找符号失败时，平台各自有一套错误记录机制：
 *    - Linux  ：dlerror() 返回一条人类可读的字符串
 *    - Windows：GetLastError() 返回一个错误码，
 *               需要用 FormatMessage 把它翻译成文字
 *
 *  注意：dlerror() 是"取完之后就清空"的，只能调用一次，
 *        所以要立刻拿去打印。这里做了统一封装。
 *
 *  【一个编码小坑】
 *    Windows 的 FormatMessageA 返回的是"本地 ANSI 编码"
 *    （简体中文 Windows 上是 GBK），而本程序其它输出都是
 *    UTF-8，混在一起会花屏。所以这里改用宽字符版本
 *    FormatMessageW 拿到宽字符串，再转成 UTF-8 返回，
 *    保证整个程序的输出编码统一。
 *
 *  返回：指向静态缓冲区的错误描述字符串（不要 free）
 */
static inline const char *dynlib_error(void)
{
#ifdef _WIN32
    static char    buf[512];
    wchar_t        wbuf[256];
    DWORD          code = GetLastError();
    DWORD          len  = FormatMessageW(
        FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL, code, 0, wbuf, (DWORD)(sizeof(wbuf) / sizeof(wbuf[0])) - 1, NULL);

    if (len == 0) {
        /* 系统没给出描述，退化为打印错误码 */
        snprintf(buf, sizeof(buf), "系统错误码 %lu", (unsigned long)code);
        return buf;
    }

    /* 去掉系统消息结尾多余的换行符 */
    while (len > 0 && (wbuf[len - 1] == L'\r' || wbuf[len - 1] == L'\n')) {
        wbuf[--len] = L'\0';
    }

    /* 宽字符（UTF-16）→ UTF-8，与程序其它输出保持一致 */
    if (WideCharToMultiByte(CP_UTF8, 0, wbuf, -1,
                            buf, (int)sizeof(buf), NULL, NULL) == 0) {
        snprintf(buf, sizeof(buf), "系统错误码 %lu", (unsigned long)code);
    }
    return buf;
#else
    const char *err = dlerror();        /* 取一次即清空 */
    return (err != NULL) ? err : "（无更多错误信息）";
#endif
}

#endif /* DYNLIB_H */
