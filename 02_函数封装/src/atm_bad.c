/*
 * 第2阶段：函数封装 - 进化前版本（屎山main）
 * 
 * 所有代码都堆在main函数里，像一团乱麻
 * 这就是我们要解决的问题！
 */

#include <stdio.h>
#include <string.h>

int main() {
    // ===== 打印欢迎信息 =====
    printf("========================================\n");
    printf("     欢迎使用 ATM 简易系统\n");
    printf("========================================\n");
    printf("\n");

    // ===== 用户登录 =====
    char username[20];
    char password[20];
    int login_ok = 0;
    
    printf("请输入用户名：");
    scanf("%s", username);
    printf("请输入密码：");
    scanf("%s", password);
    
    // 简单的验证（真实系统不会这么写，只是演示）
    if (strcmp(username, "admin") == 0 && strcmp(password, "123456") == 0) {
        login_ok = 1;
        printf("\n✅ 登录成功！欢迎，%s\n", username);
    } else {
        printf("\n❌ 登录失败！用户名或密码错误\n");
        return 1;
    }
    
    printf("\n");

    // ===== 显示余额 =====
    double balance = 5000.00;
    printf("💰 当前余额：%.2f 元\n", balance);
    printf("\n");

    // ===== 存款操作 =====
    double deposit_amount;
    printf("请输入存款金额：");
    scanf("%lf", &deposit_amount);
    
    if (deposit_amount > 0) {
        balance += deposit_amount;
        printf("✅ 存款成功！存入 %.2f 元\n", deposit_amount);
        printf("💰 新余额：%.2f 元\n", balance);
    } else {
        printf("❌ 存款金额必须大于0\n");
    }
    
    printf("\n");

    // ===== 取款操作 =====
    double withdraw_amount;
    printf("请输入取款金额：");
    scanf("%lf", &withdraw_amount);
    
    if (withdraw_amount <= 0) {
        printf("❌ 取款金额必须大于0\n");
    } else if (withdraw_amount > balance) {
        printf("❌ 余额不足！\n");
    } else {
        balance -= withdraw_amount;
        printf("✅ 取款成功！取出 %.2f 元\n", withdraw_amount);
        printf("💰 新余额：%.2f 元\n", balance);
    }
    
    printf("\n");

    // ===== 打印结束语 =====
    printf("========================================\n");
    printf("     感谢使用 ATM 简易系统\n");
    printf("========================================\n");

    return 0;
}

/*
 * 🤔 思考：
 * 1. 这个main函数有多少行？
 * 2. 如果要加一个"转账"功能，应该往哪里加？
 * 3. 如果登录逻辑要改，会不会影响其他代码？
 * 4. 三个月后回来看，你能快速找到取款的代码吗？
 * 
 * 💡 这就是"屎山"的雏形——所有东西都堆在一起，
 *    越堆越高，最后谁也不敢碰。
 * 
 * 解决方案：函数封装！👇
 */
