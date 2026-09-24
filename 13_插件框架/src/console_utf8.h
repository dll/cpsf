#ifndef CONSOLE_UTF8_H
#define CONSOLE_UTF8_H

/*
 * ============================================================
 *  console_utf8.h —— 让控制台正确显示中文（一行搞定乱码）
 * ============================================================
 *
 *  【为什么会乱码？】
 *    本课程的源码一律保存为 UTF-8 编码。
 *    但 Windows 中文版控制台默认用 GBK（代码页 936）来解释字节：
 *
 *        源码里的 "欢迎"  =  E6 AC A2 E8 BF 8E   (UTF-8)
 *        控制台按 GBK 读  =  六个字节 → 六个奇怪的汉字
 *
 *    字节本身没错，是"解释方式"错了 —— 这就是乱码的全部秘密。
 *
 *  【怎么解决？】
 *    把控制台的代码页改成 65001（UTF-8），两边就对齐了：
 *
 *        SetConsoleOutputCP(CP_UTF8);   // 输出：程序 → 屏幕
 *        SetConsoleCP(CP_UTF8);         // 输入：键盘 → 程序
 *
 *    Linux / macOS 默认就是 UTF-8，只需 setlocale 让库函数知道即可。
 *
 *  【怎么用？】
 *        #include "console_utf8.h"
 *        int main(void) {
 *            console_utf8_init();     // 必须放在任何 printf 之前
 *            ...
 *        }
 *
 *  提示：本头文件用 static 函数，多个 .c 同时 include 也不会重复定义。
 * ============================================================
 */

#if defined(_WIN32) || defined(_WIN64)
#  include <windows.h>
#else
#  include <locale.h>
#endif

/*
 * console_utf8_init —— 在 main 开头调用一次即可
 * 返回值：0=已切换到 UTF-8，非0=设置失败（但不影响程序运行）
 */
static int console_utf8_init(void)
{
#if defined(_WIN32) || defined(_WIN64)
    /* CP_UTF8 = 65001，Windows 控制台的 UTF-8 代码页 */
    if (!SetConsoleOutputCP(CP_UTF8))
        return 1;                 /* 输出代码页设置失败（例如输出被重定向） */
    if (!SetConsoleCP(CP_UTF8))
        return 2;                 /* 输入代码页设置失败 */
    return 0;
#else
    /* Linux / macOS：让 C 库按系统本地环境处理多字节字符 */
    setlocale(LC_ALL, "");
    return 0;
#endif
}

#endif /* CONSOLE_UTF8_H */
