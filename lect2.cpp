#include <stream>
#include <stdio.h>
#include <stdlib.h>
using namespace std;

class image{
	int mx;
	int my;
	int data[100000];
public:
	image (int tmx, int tmy){
		for(int i=0; i<100000;i++)
			data[i]=0;
	}

	int getMx(){
		return mx;
	}
	int getMy(){
		return my;
	}

	void show() {
		for (int i=0;i<10;i++){
			for (int j=0; j<10; j++){
				cout<< data[i*10+j];
				cout<<endl;
			}
		}	
	}

	int get(int x, int y){ 
		i = (y-1)*10 + x;
		color = data[i]
		return color;
	}
	
	void set(int x, int y, int color) {
		i = (y-1)*10 + x;
		data[i] = color;
	}

	void copy(int newmx, int newmy, newdata[100000]){
		mx = newmx;
		my = newmy;
		
		for(int i=0; i<100000;i++)
			data[i]=0;
		for(int i=0; i<100000; i++)
			data[i] = newdata[i];
	}

	void vline (int x, int color){
		for (int i=0; i<10; i++)
			data[i*10+x] = color;
	}
	
	void gline (int y, int color){
		for (int i=0, i<10; i++)
			data[y*10+i]=color;
	}
};
image a(10,10);
image b(5,6);
int main (){
	ofstream F("result.pnm");
	for (int i = 0; i < 100000; i++)
	{
		F << data[i] << " ";
	}
	F.close();
	getch();

	ifstream F("result.pnm");
	for (int i = 0; i < col; i++) {
			ifs >> data[i];
		}
	}
	return 0;
}