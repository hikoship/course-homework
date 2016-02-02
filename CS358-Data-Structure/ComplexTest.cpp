#include <iostream>
using namespace std;
#include "Complex.h"


int main()
{
         Complex a(1,2);   //Complex类的可设置变量有两个，分别是实部和虚部
         Complex b(2,3);
                                 Complex c(2,-3);

         cout << (a + b) << endl;
         cout << (a - b) << endl;
         cout << (a * b) << endl;

         cout<<endl;

         cout << (a + c) << endl;
         cout << (a - c) << endl;
         cout << (a * c) << endl;

         return 0;
}
