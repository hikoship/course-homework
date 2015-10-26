#include <iostream>
using namespace std;
#include "SavingAccount.h"

int main(){
         SavingAccount saver1(0.03, 2000, "zhangsan"); // SavingAccount的数据成员变量可以设置3个，分别为：年利率，存户余额，存户的姓名
         SavingAccount saver2(0.03, 3000, "lisi");

         saver1.print();
         saver2.print();
         cout <<endl;

         saver1.annualInterestRate=0.04;
         saver1.print();
         saver2.print();
         return 0;
}
