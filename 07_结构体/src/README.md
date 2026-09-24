# 第7讲 结构体 —— 把散落的数据打包成一个东西

> struct 把一组相关数据打包，代码可读性上一个台阶。

## 一、文件清单

| 文件 | 说明 |
|:---|:---|
| `struct_atm.c` | ======================================== |
| `console_utf8.h` | 控制台 UTF-8 初始化（解决中文乱码，全系列共用） |
| `build.bat` | Windows 一键构建（cmd 里双击或命令行运行） |
| `Makefile` | Linux / macOS / Git Bash 构建 |
| `运行示例.txt` | 一次完整演示的真实输出，可直接对照 |

## 二、怎么构建

**Windows（cmd / PowerShell）**

```bat
cd 07_结构体\src
build.bat
```

**Linux / macOS / Git Bash**

```bash
cd 07_结构体/src
make          # 只编译
make run      # 编译并自动演示
make clean    # 清理产物
```

## 三、怎么运行

- 演示输入序列：`1001 → 1 → 2/500 → 3/200 → 5 → 6 → 0`
- 完整输出见 [`运行示例.txt`](运行示例.txt)

## 四、构建产物

```
struct_atm.exe
```

（目录里当前存在：struct_atm.exe）

## 五、中文为什么会乱码，以及本讲怎么解决的

源码统一保存为 **UTF-8**，而 Windows 中文版控制台默认用 **GBK(936)** 解释字节，
两边对不上就显示成乱码。解决办法是让程序自己把控制台切到 UTF-8：

```c
#include "console_utf8.h"

int main(void)
{
    console_utf8_init();   /* 内部：SetConsoleOutputCP(CP_UTF8) */
    ...
}
```

`build.bat` 开头也有 `chcp 65001`，保证脚本自己打印的中文同样不乱码。

---

本讲是「表达式 → 函数 → 模块 → 库 → 插件 → 框架」主线上的第 7 级台阶。
