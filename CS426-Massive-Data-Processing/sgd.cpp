#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define USER_NUM 100000
#define MOVIE_NUM 17770
#define DATE_NUM 5115
#define DATE_SPAN 30
#define UV_DIMEN 2
#define TOTAL 20629659

int main(){
    // initailize
    srand(time(NULL));
    int user_rating[USER_NUM];
    int user_num[USER_NUM];
    int movie_rating[MOVIE_NUM];
    int movie_num[MOVIE_NUM];
    int date_rating[DATE_NUM];
    int date_num[DATE_NUM];
    int total_rating = 0;
    int total_num = 0;
    int p_user[USER_NUM][UV_DIMEN];
    int q_movie[USER_NUM][UV_DIMEN];
    for(int i = 0; i < USER_NUM; i++) {
        user_rating[i] = 0;
        user_num[i] = 0;
        for(int j = 0; j < UV_DIMEN; j++)
            p_user[i][j] = 0.1 * rand() / double(RAND_MAX);
    }
    for(int i = 0; i < MOVIE_NUM; i++) {
        movie_rating[i] = 0;
        movie_num[i] = 0;
        for(int j = 0; j < UV_DIMEN; j++)
            q_movie[i][j] = 0.1 * rand() / double(RAND_MAX);
    }
    for(int i = 0; i < DATE_NUM; i++) {
        date_rating[i] = 0;
        date_num[i] = 0;
    }

    FILE *f_train = fopen("train.txt", "w");
    int _u, _m, _d, _r;
    for(int i = 0; fscanf(f_train, "%d,%d,%d,%d", &_u, &_m, &_d, &_r); i++);
    fclose(f_train);

    printf("%d,%d,%d,%d", _u, _m, _d, _r);


    
    printf("%d\n", USER_NUM);

    return 0;
}
