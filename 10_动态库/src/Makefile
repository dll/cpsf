# ============================================================
# 第10讲：动态库 - 构建脚本（Linux / MinGW）
# 将 account.c 和 transaction.c 编译成动态库 libaccount.so
# 主程序 main.c 链接动态库生成可执行文件
#
# 与第9讲静态库的差异：
#   静态库: gcc -c *.c; ar rcs libaccount.a *.o; 链接 .a
#   动态库: gcc -fPIC -shared -o libaccount.so *.c; 链接 .so
# ============================================================

CC = gcc
CFLAGS = -Wall -Wextra -g

# Linux 动态库文件名必须是 libxxx.so；Windows(MinGW) 为 xxx.dll + libxxx.dll.a
LIB_NAME = libaccount.so
TARGET = atm_dynamic

# 默认目标：构建动态库 + 可执行文件
all: $(LIB_NAME) $(TARGET)

# ---- 第1步：编译动态库 ----
# -fPIC   生成位置无关代码（Position Independent Code）
#         动态库会被映射到进程地址空间的任意位置，代码必须与位置无关
# -shared 生成共享库（动态库）
# 说明：Linux 下 ACCOUNT_EXPORTS / TRANSACTION_EXPORTS 不影响编译结果，
#       因为 Linux 分支统一使用 __attribute__((visibility("default")))，
#       这里仍一并定义，保持与 Windows 构建命令一致、便于阅读。
$(LIB_NAME): account.c transaction.c account.h transaction.h
	$(CC) $(CFLAGS) -fPIC -shared -o $(LIB_NAME) account.c transaction.c \
	    -DACCOUNT_EXPORTS -DTRANSACTION_EXPORTS
	@echo "============================================"
	@echo "动态库 $(LIB_NAME) 创建成功！"
	@echo "包含导出符号: account_* / transaction_*"
	@echo "============================================"

# ---- 第2步：链接可执行文件 ----
# -L.        在当前目录查找动态库
# -laccount  链接 libaccount.so（自动加 lib 前缀和 .so 后缀）
# -Wl,-rpath,'$$ORIGIN'  让程序运行时到自身所在目录查找 .so
$(TARGET): main.c $(LIB_NAME)
	$(CC) $(CFLAGS) -o $(TARGET) main.c -L. -laccount -Wl,-rpath,'$$ORIGIN'
	@echo "============================================"
	@echo "可执行文件 $(TARGET) 链接成功！"
	@echo "链接方式: 加载时链接（运行时加载 $(LIB_NAME)）"
	@echo "============================================"

# 查看动态库导出的符号
inspect:
	@echo "=== 动态库导出的符号 ==="
	nm -D --defined-only $(LIB_NAME)
	@echo "=== 可执行文件依赖的动态库 ==="
	ldd $(TARGET) 2>/dev/null || echo "(Windows/MinGW 下请用 objdump -p)"

# 清理
clean:
	-rm -f *.o $(LIB_NAME) $(TARGET) $(TARGET).exe *.dll *.dll.a
	@echo "清理完成"

.PHONY: all clean inspect
