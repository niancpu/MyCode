#include <stdio.h>
#include <math.h>
#define  f(x) x*x-5*x+sin(x)
int main(void)                    
{   
  int i; float max;
  max=f(1);        
  for(i=2;i<=10;i++)
  {
    if(f(i)>max) max+=i;    /*$1*/    
  }
  printf("%f\n",max);   
  return 0;  
}