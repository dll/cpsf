# ============================================================
# 第9讲：静态库 - 构建脚本
# 将 account.c 和 transaction.c 编译打包成 libaccount.a
# 主程序 main.c 链接静态库生成可执行文件
# ============================================================

CC = gcc
CFLAGS = -Wall -Wextra -g

# 静态库名称（Linux: libaccount.a  Windows: libaccount.a）
LIB_NAME = libaccount.a
TARGET = atm_static

# 默认目标：构建静态库 + 可执行文件
all: $(LIB_NAME) $(TARGET)

# ---- 第1步：编译目标文件 ----
account.o: account.c account.h
	$(CC) $(CFLAGS) -c account.c -o account.o

transaction.o: transaction.c transaction.h account.h
	$(CC) $(CFLAGS) -c transaction.c -o transaction.o

main.o: main.c account.h transaction.h
	$(CC) $(CFLAGS) -c main.c -o main.o

# ---- 第2步：用 ar 创建静态库 ----
# ar rcs 含义：
#   r = 替换/插入归档文件中的成员
#   c = 创建归档文件（如果不存在）
#   s = 写入索引（相当于 ranlib，加速链接时查找）
$(LIB_NAME): account.o transaction.o
	ar rcs $(LIB_NAME) account.o transaction.o
	@echo "============================================"
	@echo "静态库 $(LIB_NAME) 创建成功！"
	@echo "包含: account.o + transaction.o"
	@echo "============================================"

# ---- 第3步：链接可执行文件 ----
# -L. 指定库搜索路径为当前目录
# -laccount 告诉链接器链接 libaccount 库（自动加 lib 前缀和 .a 后缀）
$(TARGET): main.o $(LIB_NAME)
	$(CC) $(CFLAGS) -o $(TARGET) main.o -L. -laccount
	@echo "============================================"
	@echo "可执行文件 $(TARGET) 链接成功！"
	@echo "链接方式: 静态链接（代码从 libaccount.a 复制到可执行文件）"
	@echo "============================================"

# 查看静态库内容
inspect:
	@echo "=== 静态库内容 ==="
	ar t $(LIB_NAME)
	@echo "=== 符号表 ==="
	nm $(LIB_NAME) | head -30

# 清理
clean:
	-rm -f *.o $(LIB_NAME) $(TARGET) $(TARGET).exe
	@echo "清理完成"

.PHONY: all clean inspect
