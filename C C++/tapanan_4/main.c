#include <stdio.h>
#include <locale.h>

int main()
{
    setlocale(LC_ALL, "th_TH");
    char first[20], last[20], id[9];
    float points, full;

    float radius, pi, area, width, hight, area1;
    pi = 22.0/7;

    printf("Enter Radius = ");
    scanf("%f", &radius);
    area = pi*radius*radius;
    printf("Area = %.2f\n\n", area);

    printf("Enter Width = ");
    scanf("%f", &width);
    printf("Enter Hight = ");
    scanf("%f", &hight);
    area1 = width*hight;
    printf("\nArea = %.2f\n\n", area1);


    printf("First name = ");
    scanf("%s", first);
    printf("Last name = ");
    scanf("%s", last);
    printf("Id = ");
    scanf("%s", id);
    printf("Point = ");
    scanf("%f", &points);
    printf("Full = ");
    scanf("%f", &full);

    if ((points/full) >= 0.6)
    {
        printf("\nName = %s %s\n", first, last);
        printf("ID = %s\n", id);
        printf("Points %f/%f\n", points, full);
        printf("You Passed.!!!\n");
        printf("!!!Congratulations on your freaking life, dude.!!!");
    }
    else
    {
        printf("Your fail!!!");
        // printf("%s", "!!!มึงไม่ผ่านไอโง่ เรียนใหม่ซะ!!!);
    }
    

    return 0;
}
