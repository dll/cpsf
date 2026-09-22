/*
 * 第2阶段：函数封装 - 进化后版本
 * 
 * 把不同功能封装成独立的函数
 * 代码清晰、易读、易维护
 */

#include <stdio.h>
#include <string.h>

// ========== 函数声明（接口）==========

// 打印欢迎界面
void print_welcome();

// 打印结束语
void print_goodbye();

// 用户登录，返回1表示成功，0表示失败
int user_login(char *username);

// 显示余额
void show_balance(double balance);

// 存款操作，返回新余额
double deposit(double balance, double amount);

// 取款操作，返回新余额
double withdraw(double balance, double amount);

// ========== 主函数 ==========

int main() {
    char username[20];
    double balance = 5000.00;
    double amount;

    // 1. 打印欢迎信息
    print_welcome();

    // 2. 用户登录
    if (!user_login(username)) {
        printf("\n❌ 登录失败！\n");
        return 1;
    }
    printf("\n✅ 登录成功！欢迎，%s\n", username);

    // 3. 显示余额
    printf("\n");
    show_balance(balance);

    // 4. 存款
    printf("\n请输入存款金额：");
    scanf("%lf", &amount);
    balance = deposit(balance, amount);
    show_balance(balance);

    // 5. 取款
    printf("\n请输入取款金额：");
    scanf("%lf", &amount);
    balance = withdraw(balance, amount);
    show_balance(balance);

    // 6. 打印结束语
    printf("\n");
    print_goodbye();

    return 0;
}

// ========== 函数实现 ==========

/*
 * 函数：print_welcome
 * 功能：打印欢迎界面
 * 参数：无
 * 返回：无
 */
void print_welcome() {
    printf("========================================\n");
    printf("     欢迎使用 ATM 简易系统\n");
    printf("========================================\n");
}

/*
 * 函数：print_goodbye
 * 功能：打印结束语
 * 参数：无
 * 返回：无
 */
void print_goodbye() {
    printf("========================================\n");
    printf("     感谢使用 ATM 简易系统\n");
    printf("========================================\n");
}

/*
 * 函数：user_login
 * 功能：用户登录验证
 * 参数：username - 存储登录成功的用户名
 * 返回：1=成功，0=失败
 */
int user_login(char *username) {
    char password[20];
    
    printf("请输入用户名：");
    scanf("%s", username);
    printf("请输入密码：");
    scanf("%s", password);
    
    // 简单验证（真实系统不会这么写）
    if (strcmp(username, "admin") == 0 && strcmp(password, "123456") == 0) {
        return 1;
    }
    return 0;
}

/*
 * 函数：show_balance
 * 功能：显示当前余额
 * 参数：balance - 当前余额
 * 返回：无
 */
void show_balance(double balance) {
    printf("💰 当前余额：%.2f 元\n", balance);
}

/*
 * 函数：deposit
 * 功能：存款
 * 参数：balance - 当前余额
 *       amount  - 存款金额
 * 返回：存款后的新余额
 */
double deposit(double balance, double amount) {
    if (amount > 0) {
        printf("✅ 存款成功！存入 %.2f 元\n", amount);
        return balance + amount;
    } else {
        printf("❌ 存款金额必须大于0\n");
        return balance;
    }
}

/*
 * 函数：withdraw
 * 功能：取款
 * 参数：balance - 当前余额
 *       amount  - 取款金额
 * 返回：取款后的新余额
 */
double withdraw(double balance, double amount) {
    if (amount <= 0) {
        printf("❌ 取款金额必须大于0\n");
        return balance;
    } else if (amount > balance) {
        printf("❌ 余额不足！\n");
        return balance;
    } else {
        printf("✅ 取款成功！取出 %.2f 元\n", amount);
        return balance - amount;
    }
}

/*
 * 🎉 进化后的好处：
 * 
 * 1. main函数变短了！一眼就能看懂整个流程
 * 2. 每个函数只做一件事（单一职责）
 * 3. 想改登录逻辑？只看user_login函数就行
 * 4. 想加转账功能？写个transfer函数，加一行调用
 * 5. 函数可以复用！比如show_balance调用了好多次
 * 
 * 📦 这就是"封装"的思想——把复杂的细节包起来，
 *    对外只暴露简洁的接口。
 * 
 * 下一阶段：多文件模块，把函数拆到不同的文件里！
 */
