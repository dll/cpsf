/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  plugin.h —— 统一插件接口（整合第12 / 13讲成果）
 * ============================================================
 *
 *  【本讲定位】
 *    这是全系列的收官之讲。前面 13 讲我们用 ATM 银行系统一路演进：
 *      表达式 → 控制结构 → 函数 → 多文件 → 指针 → 数组 →
 *      结构体 → 链表 → 静态库 → 动态库 → 运行时加载 →
 *      接口抽象 → 插件框架
 *    本讲把这一切"拼装"成一个真正能编译、能运行的完整工程。
 *
 *  【本文件的作用】
 *    它是框架与所有插件之间的"契约"（第12讲的结构体接口），
 *    同时带上第13讲的五阶段生命周期与运行时状态。
 *    主程序和每一个插件 DLL 都 #include 本文件，
 *    保证双方对 Plugin 结构体的内存布局理解完全一致。
 *
 *  【一个关键约定】
 *    插件动态库必须导出一个 C 风格符号：get_plugin
 *    它不接受参数，返回一个 Plugin* 指针。
 *    框架通过它拿到插件实例——这就是"接口统一"的落点。
 *
 *  编译：由 build.bat / Makefile 统一驱动
 * ============================================================
 */

#ifndef PLUGIN_H
#define PLUGIN_H

/*
 * 导出宏：
 *   Windows 下动态库里的符号默认不对外可见，必须显式 dllexport。
 *   Linux 下用 visibility("default") 打开（编译加 -fvisibility=hidden 时才有意义）。
 *   注意这里必须是 C 风格符号名，避免 C++ name mangling——
 *   框架用 GetProcAddress / dlsym 按名字查找，名字错了就找不到。
 */
#ifdef _WIN32
    #define PLUGIN_EXPORT __declspec(dllexport)
#else
    #define PLUGIN_EXPORT __attribute__((visibility("default")))
#endif

/*
 * ============================================================
 *  插件运行时状态（对应第13讲的状态机）
 * ============================================================
 *  UNLOADED → LOADED → INITIALIZED → STARTED → STOPPED → CLEANED
 *  每成功走完一个阶段，状态前进一格；框架据此判断能否调用下一步。
 */
typedef enum {
    PLUGIN_UNLOADED = 0,     /* 未加载 */
    PLUGIN_LOADED,           /* 已加载（DLL 已进入进程） */
    PLUGIN_INITIALIZED,      /* 已初始化（init 成功） */
    PLUGIN_STARTED,          /* 已启动（start 成功，菜单已挂上） */
    PLUGIN_STOPPED,          /* 已停止（stop 成功） */
    PLUGIN_CLEANED           /* 已清理（cleanup 成功） */
} PluginState;

/*
 * ============================================================
 *  插件接口 —— C 语言的"接口"
 * ============================================================
 *
 *  【对比第12讲】
 *    第12讲是三阶段：init / execute / cleanup
 *    本讲合并第13讲，扩展为五阶段：
 *      init → start → execute(可多次) → stop → cleanup
 *
 *  【对比第7讲结构体】
 *    第7讲结构体打包"数据"，本结构体打包"行为"（函数指针）。
 *
 *  【对比 Java / C#】
 *    interface IPlugin { void init(); void start(); int execute(double); ... }
 *    在 C 里就是"结构体 + 函数指针"——手写的一张虚函数表（vtable）。
 *
 *  【关于 need_amount 字段】
 *    这是本讲为"完整工程"补充的一处整合性扩展：
 *      1 = 框架先向用户读取金额，再调用 execute(self, amount)
 *      0 = 插件自行处理输入（如"查询"无需金额、"转账"需要目标账户）
 *    它让菜单/输入协议可以完全由插件自己声明，
 *    框架不需要为任何一个具体插件写死逻辑。
 */
typedef struct Plugin {
    /* ---- 元数据 ---- */
    char name[32];              /* 插件名称（唯一标识） */
    char version[16];           /* 版本号 */
    char description[64];       /* 功能描述 */
    int  menu_id;               /* 菜单编号（0 表示不挂菜单） */
    char menu_label[40];        /* 菜单显示文字 */
    int  need_amount;           /* 1=框架先读取金额；0=插件自己读 */

    /* ---- 生命周期方法（函数指针 = 行为） ---- */
    int  (*init)(struct Plugin* self);                     /* 初始化：分配资源 */
    int  (*start)(struct Plugin* self);                    /* 启动：挂菜单/开服务 */
    int  (*execute)(struct Plugin* self, double amount);   /* 执行：核心业务 */
    int  (*stop)(struct Plugin* self);                     /* 停止：摘菜单/停服务 */
    void (*cleanup)(struct Plugin* self);                  /* 清理：释放资源 */

    /* ---- 私有数据（类比 C++ 的 private 成员） ---- */
    void* user_data;

    /* ---- 运行时状态 ---- */
    PluginState state;

} Plugin;

/*
 * ============================================================
 *  插件节点 —— 用链表管理插件（衔接第8讲链表 / 第12讲插件发现）
 * ============================================================
 *
 *  【对比第8讲】
 *    第8讲链表节点：数据域(amount...) + 指针域(next)
 *    本讲插件节点：接口指针(Plugin*) + 指针域(next)
 *    结构一模一样，只是"管理的数据"升级成了"管理的行为"。
 */
typedef struct PluginNode {
    Plugin* plugin;                 /* 指向插件接口 */
    struct PluginNode* next;        /* 下一个插件节点 */
} PluginNode;

/*
 * ============================================================
 *  插件入口函数原型
 * ============================================================
 *  动态库必须导出下面这个 C 符号（名字固定为 get_plugin）：
 *
 *      PLUGIN_EXPORT Plugin* get_plugin(void);
 *
 *  框架动态加载时：
 *      handle = LoadLibrary("plugins/deposit_plugin.dll");
 *      entry  = GetProcAddress(handle, "get_plugin");
 *      Plugin* p = entry();
 *
 *  这样一来，框架只依赖"名字 + 返回值类型"这一条约定，
 *  插件内部怎么写、叫什么函数，框架完全不需要知道。
 */
typedef struct Plugin* (*PluginEntry)(void);

#define PLUGIN_ENTRY_NAME "get_plugin"

#endif /* PLUGIN_H */
