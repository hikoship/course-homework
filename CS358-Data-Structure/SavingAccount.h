//Filename: SavingAccount.h
//Define class SavingAccount

#ifndef _SavingAccount_h
#define _SavingAccount_h
#include <iostream>
using namespace std;
class SavingAccount{
private:
                 double principle;
                 char *name;
public:
                 static double annualInterestRate;
                SavingAccount( double rate, double pr, char n[])
                {
                                annualInterestRate=rate;
                                principle=pr;
                                name=n;
                }
                 double rate;
                 void print();
};
#endif
