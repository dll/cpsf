/*
 * ============================================================
 *  第14讲：完整项目与总结展望
 *  dynamic_loader.c —— 跨平台动态加载实现
 * ============================================================
 *
 *  平台差异（第10 / 11讲讲过）：
 *
 *               Windows                    Linux / macOS
 *    ------------------------------------------------------------
 *    加载库      LoadLibrary                dlopen
 *    取符号      GetProcAddress             dlsym
 *    卸载库      FreeLibrary                dlclose
 *    错误信息    GetLastError+FormatMessage dlerror
 *    扫描目录    FindFirstFile/FindNextFile opendir/readdir
 *
 *  本文件用条件编译把上述差异集中处理，给上层一套统一 API。
 * ============================================================
 */

#include "dynamic_loader.h"
#include <stdio.h>
#include <string.h>

/* ============================================================
 *  Windows 实现
 * ============================================================ */
#ifdef _WIN32

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

const char *dll_extension(void)
{
    return ".dll";
}

DllHandle dll_load(const char *path, char *err, size_t errlen)
{
    HMODULE h = LoadLibraryA(path);
    if (h == NULL) {
        if (err != NULL && errlen > 0) {
            DWORD code = GetLastError();
            char msg[256] = {0};
            size_t i;
            /* 把系统错误码翻译成人话，方便课堂上演示"到底为什么加载失败" */
            FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
                           NULL, code, 0, msg, (DWORD)sizeof(msg), NULL);
            /* 系统消息可能带换行/回车，统一压成单行，避免打印时串行 */
            for (i = 0; msg[i] != '\0'; i++) {
                if (msg[i] == '\r' || msg[i] == '\n') {
                    msg[i] = ' ';
                }
            }
            snprintf(err, errlen, "系统错误码 %lu（%s）", (unsigned long)code,
                     msg[0] != '\0' ? msg : "未知原因");
        }
        return NULL;
    }
    return (DllHandle)h;
}

void *dll_symbol(DllHandle handle, const char *name)
{
    if (handle == NULL) {
        return NULL;
    }
    return (void*)GetProcAddress((HMODULE)handle, name);
}

void dll_unload(DllHandle handle)
{
    if (handle != NULL) {
        FreeLibrary((HMODULE)handle);
    }
}

int dll_scan_dir(const char *dir, const char *ext,
                 DllFileCallback cb, void *user)
{
    char pattern[512];
    WIN32_FIND_DATAA fd;
    HANDLE hfind;
    int found = 0;

    snprintf(pattern, sizeof(pattern), "%s\\*%s", dir, ext);
    hfind = FindFirstFileA(pattern, &fd);
    if (hfind == INVALID_HANDLE_VALUE) {
        return 0;   /* 目录不存在或没有匹配文件 */
    }

    do {
        if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            continue;   /* 跳过子目录 */
        }
        char fullpath[512];
        snprintf(fullpath, sizeof(fullpath), "%s\\%s", dir, fd.cFileName);
        if (cb != NULL) {
            cb(fullpath, user);
        }
        found++;
    } while (FindNextFileA(hfind, &fd));

    FindClose(hfind);
    return found;
}

/* ============================================================
 *  Linux / macOS 实现
 * ============================================================ */
#else

#include <dlfcn.h>
#include <dirent.h>
#include <stdlib.h>

const char *dll_extension(void)
{
    return ".so";
}

DllHandle dll_load(const char *path, char *err, size_t errlen)
{
    void *h = dlopen(path, RTLD_LAZY);
    if (h == NULL) {
        if (err != NULL && errlen > 0) {
            const char *e = dlerror();
            snprintf(err, errlen, "%s", e != NULL ? e : "未知原因");
        }
        return NULL;
    }
    return (DllHandle)h;
}

void *dll_symbol(DllHandle handle, const char *name)
{
    if (handle == NULL) {
        return NULL;
    }
    return dlsym(handle, name);
}

void dll_unload(DllHandle handle)
{
    if (handle != NULL) {
        dlclose(handle);
    }
}

int dll_scan_dir(const char *dir, const char *ext,
                 DllFileCallback cb, void *user)
{
    DIR *d = opendir(dir);
    int found = 0;
    struct dirent *entry;
    size_t extlen = strlen(ext);

    if (d == NULL) {
        return 0;
    }

    while ((entry = readdir(d)) != NULL) {
        size_t len = strlen(entry->d_name);
        if (len < extlen) {
            continue;
        }
        if (strcmp(entry->d_name + (len - extlen), ext) != 0) {
            continue;   /* 后缀不匹配 */
        }
        char fullpath[512];
        snprintf(fullpath, sizeof(fullpath), "%s/%s", dir, entry->d_name);
        if (cb != NULL) {
            cb(fullpath, user);
        }
        found++;
    }

    closedir(d);
    return found;
}

#endif /* _WIN32 */
