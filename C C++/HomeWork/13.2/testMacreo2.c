#include <stdio.h>

int main()
{
    int ret;
    printf("This is %s program\n", __FILE__);
    printf("Time to run this program is %s\n", __TIME__);
    ret = __STDC__;
    
    if (ret == 1){
        printf("RUN BY STANDARD ISO/ANSI C\n");
    }
    else{
        printf("DON'T RUN BY STANDARD ISO/ANSI C\n");
    }
}
