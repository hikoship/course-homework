//Filename: Complex.h
//Define class Complex

#ifndef _Complex_h
#define _Complex_h
#include <iostream>
#include <iomanip>
using namespace std;
class Complex{
                 friend ostream &operator <<(ostream &os, const Complex &obj);
                 friend Complex operator +(const Complex c1 , const Complex c2);
                 friend Complex operator -(const Complex c1 , const Complex c2);
                 friend Complex operator *(const Complex c1 , const Complex c2);
private:
                 double real;
                 double imaginary;

public:
                Complex( double r,double i) {real=r;imaginary=i;}
};

#endif
