#include<stdio.h>
#include<stdlib.h>

int* ArrayInit(int width,int length){
	int* ptr = (int*)malloc(length * width * sizeof(int));
	return ptr;
}

void ArrayAssignment(int x, int y,int* ptr,int value,int width) {
	ptr[x * width + y ] = value;
}

int ArrayVisit(int x, int y, int* p,int width) {
	return p[x *width + y ];
}

void transpose(int* src, int* dst, int width, int length) {
	for (int i = 0; i < length; i++) {
		for (int j = 0;j < width;j++) {
			dst[j * length + i] = src[i * width + j];
		}
	}
}

void print2DArray(int* p,int width, int length) {
	for (int i = 0; i < length; i++) {
		for (int j = 0;j < width;j++) {
			printf("%d  ", p[i * width + j]);
		}
		printf("\n");
	}
}

int main() {
	int width = 3, length = 2;
	int* p = ArrayInit(width, length);
	for (int i = 0;i < 6;i++) {
		p[i] = i;
	}
	int* dst;
	dst = (int*)malloc(width * length * sizeof(int));
	transpose(p, dst, width, length);
	print2DArray(dst,length, width);
}