# Windows 控制台默认是 GBK(936)，而本文件是 UTF-8：
# 先把代码页切到 65001，否则 make 打印的中文提示会显示成乱码。
ifeq ($(OS),Windows_NT)
$(shell cmd /c "chcp 65001 >nul 2>&1")
endif

# ============================================================
#  第13讲：插件框架架构  —— Makefile（Linux / MinGW）
# ============================================================
#  用法：
#    make          编译，生成 plugin_framework
#    make run      编译并自动喂入输入运行演示
#    make clean     清理中间产物
# ============================================================

CC      = gcc
CFLAGS  = -Wall -O2
TARGET  = plugin_framework

SRCS    = framework.c atm_state.c plugin_deposit.c plugin_withdraw.c \
          plugin_query.c plugin_transfer.c main.c
OBJS    = $(SRCS:.c=.o)

HEADERS = framework.h plugins.h atm_state.h

# 默认目标：链接
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# 每个 .c 编译成 .o（依赖头文件变化）
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# 自动演示：菜单输入序列 = 1/500, 2/200, 3/0, 4/300, 0
.PHONY: run
run: $(TARGET)
	printf '1\n500\n2\n200\n3\n0\n4\n300\n0\n' | ./$(TARGET)

.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET) $(TARGET).exe *.o
