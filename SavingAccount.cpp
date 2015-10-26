//Filename: SavingAccount.cpp
//实现 class SavingAccount

#include "SavingAccount.h"

void SavingAccount::print(){
                principle*=(1+annualInterestRate/12);
                cout<<name<< "\t"<<principle<<endl;
}
double SavingAccount::annualInterestRate=0.0;
