/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  dynamic_loader.h —— 运行时动态加载封装（跨平台）
 * ============================================================
 *
 *  【第11讲回顾】
 *    Linux 用 dlopen / dlsym / dlclose，
 *    Windows 用 LoadLibrary / GetProcAddress / FreeLibrary。
 *    两者的 API 名字不同、错误处理方式不同，
 *    如果直接散落在业务代码里，可移植性很差。
 *
 *  【本讲做法】
 *    用一层薄薄的封装把平台差异"关"在这两个文件里：
 *      dll_load()   加载动态库
 *      dll_symbol() 取符号地址
 *      dll_unload() 卸载动态库
 *      dll_scan_dir() 扫描目录（发现插件文件）
 *    上层框架只认这几个函数，不关心自己跑在哪个操作系统上。
 *
 *  【这就是"接口抽象"的又一次应用】
 *    平台是"实现"，封装后的 dll_* 是"接口"。
 * ============================================================
 */

#ifndef DYNAMIC_LOADER_H
#define DYNAMIC_LOADER_H

#include <stddef.h>

/* 动态库句柄（对 void* 的语义化包装） */
typedef void* DllHandle;

/*
 * 加载动态库。
 *   path   : 库文件路径
 *   err    : 失败时写入人类可读的原因（可为 NULL）
 *   errlen : err 缓冲区长度
 *   返回   : 成功返回非 NULL 句柄；失败返回 NULL
 */
DllHandle dll_load(const char *path, char *err, size_t errlen);

/*
 * 按符号名取地址（C 风格符号，无 name mangling）。
 * 返回 NULL 表示符号不存在。
 */
void *dll_symbol(DllHandle handle, const char *name);

/* 卸载动态库 */
void dll_unload(DllHandle handle);

/* 当前平台的插件扩展名：Windows=".dll"，Linux/Mac=".so" */
const char *dll_extension(void);

/* 扫描目录时的回调：每发现一个匹配文件调用一次 */
typedef void (*DllFileCallback)(const char *fullpath, void *user);

/*
 * 扫描目录 dir 中所有以 ext 结尾的文件，逐个回调 cb。
 * 返回发现并回调的文件个数；目录不存在返回 0。
 */
int dll_scan_dir(const char *dir, const char *ext,
                 DllFileCallback cb, void *user);

#endif /* DYNAMIC_LOADER_H */
