#include <bits/stdc++.h>

using namespace std;

priority_queue<int, vector<int>, greater<int> > pq; // 오름차순
// priority_queue<int, vecoter<int>, less<int> > pq;

int idx = 2;

void go(int &idx){
    idx = 1;
}

void go2(int idx){
    idx = 100;
}

int main(){
    
    int a[10] = {1, 3, 10, 5, 7, 2, 9, 8, 6, 4};

    int index, temp, min;
    for(int i=0; i<sizeof(a)/sizeof(int); i++){
        min = a[i];
        index = i;
        for(int j=i+1; j<sizeof(a)/sizeof(int); j++){
            if(min > a[j]){
                min = a[j];
                index = j;
            }
        }
        temp = a[i];
        a[i] = a[index];
        a[index] = temp;
    }

    for(int i=0; i<sizeof(a)/sizeof(int); i++){
        cout << a[i] << "\n";
    }
    
    return 0;
}