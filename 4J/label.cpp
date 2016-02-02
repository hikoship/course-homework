/*
g++ label.cpp -o label -lpthread
0'54 96.835% 0'32 no gen
*/
#include<cstdlib>
#include<cstdio>
#include<iostream>
#include<cstring>
#include<algorithm>
#include<sys/types.h>
#include<unistd.h>
#include<pthread.h>
#define o *(int *)arg
#define maxq 37786
#define n 4
#define m 8
using namespace std;

char s[111111],buf[n*m+3][111],BUF[n+3][111];
FILE *f[n*m+3];
pthread_t th[n*m+3],TH[n+3];
int tmp,cnt,total,finish[n+3],a[n*m+3],b[n][maxq+5];
pthread_mutex_t mutex;

void gen(){
	for (int i=0;i<n*m;i++){
		strcpy(s,"train");
		s[5]=i/10+'0';
		s[6]=i%10+'0';
		f[i]=fopen(s,"w");
	}
	freopen("train.txt","r",stdin);
	while (gets(s)){
		int t,x=(s[1]-'0')*10+s[2]-'0';
		if (s[0]=='A'){
			if (x<45) t=0; else if (x<61) t=1; else if (x<62) t=2; else t=3;
			for (int i=0;i<m;i++) fprintf(f[t*m+i],"%s\n",s);
		}
		if (s[0]=='B'){
			if (x<24) t=0; else if (x<41) t=1; else if (x<60) t=2; else if (x<65) t=3; else t=4;
			for (int i=0;i<n;i++) fprintf(f[i*m+t],"%s\n",s);
		}
		if (s[0]=='C'){
			if (x<9) t=5; else t=6;
			for (int i=0;i<n;i++) fprintf(f[i*m+t],"%s\n",s);
		}
		if (s[0]=='D'){
			int t=7;
			for (int i=0;i<n;i++) fprintf(f[i*m+t],"%s\n",s);
		}
	}
	for (int i=0;i<n*m;i++) fclose(f[i]);
}

void *work(void *arg){
	sprintf(buf[o],"./train train%02d",o);
	system(buf[o]);
	sprintf(buf[o],"./predict test.txt train%02d.model output%02d",o,o);
	system(buf[o]);
	pthread_mutex_lock(&mutex);
	++finish[o/m];
	pthread_mutex_unlock(&mutex);
}

void *merge(void *arg){
	for (int i=0;i<maxq;i++) b[o][i]=1;
	strcpy(BUF[o],"output");
	while (finish[o]<m);
	for (int i=0;i<m;i++){
		BUF[o][6]=(o*m+i)/10+'0';
		BUF[o][7]=(o*m+i)%10+'0';
		FILE *f=fopen(BUF[o],"r");
		int x;
		for (int j=0;j<maxq;j++){
			fscanf(f,"%d",&x);
			if (x==-1) b[o][j]=0;
		}
		fclose(f);
	}
	pthread_mutex_lock(&mutex);
	++total;
	pthread_mutex_unlock(&mutex);
}

int main(){
	gen();
	pthread_mutex_init(&mutex, NULL);
	for (int i=0;i<n*m;i++){
		a[i]=i;
		pthread_create(&th[i],NULL,work,&a[i]);
	}
	for (int i=0;i<n;i++){
		pthread_create(&TH[i],NULL,merge,&a[i]);
	}
	while (total<n);
	freopen("test.txt","r",stdin);
	for (int i=0;i<maxq;i++){
		gets(s);
		tmp=0;
		for (int j=0;j<n;j++) tmp|=b[j][i];
		if (s[0]=='A' && tmp || s[0]!='A' && !tmp) cnt++;
	}
	printf("Final result:\nAccuracy = %.4f% (%d/%d)\n",100.0*cnt/maxq,cnt,maxq);
}
