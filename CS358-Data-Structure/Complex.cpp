//Filename: Complex.cpp
//实现 class Complex

#include "Complex.h"

Complex operator+( const Complex c1,const Complex c2){
                Complex tmp(0,0);
                tmp.real=c1.real+c2.real;
                tmp.imaginary=c1.imaginary+c2.imaginary;
                 return tmp;
}

Complex operator-( const Complex c1,const Complex c2){
                Complex tmp(0,0);
                tmp.real=c1.real-c2.real;
                tmp.imaginary=c1.imaginary-c2.imaginary;
                 return tmp;
}

Complex operator*( const Complex c1,const Complex c2){
                Complex tmp(0,0);
                tmp.real=c1.real*c2.real-c1.imaginary*c2.imaginary;
                tmp.imaginary=c1.real*c2.imaginary+c1.imaginary*c2.imaginary;
                 return tmp;
}

ostream &operator<<(ostream &os, const Complex &obj){

                 if(obj.real==0){
                                 if(obj.imaginary==0) os<<0;
                                 if(obj.imaginary==1) os<<"i" ;
                                 if(obj.imaginary==-1) os<<"-i" ;
                                 else os<<obj.imaginary<<"i" ;
                }
                 else {
                                 if(obj.imaginary==0) os<<obj.real;
                                 if(obj.imaginary==1) os<<obj.real<<"+i";
                                 if(obj.imaginary==-1) os<<obj.real<<"-i";
                                 else os<<obj.real<<showpos<<obj.imaginary<<noshowpos<<"i";
                }
                 return os;
}


  
