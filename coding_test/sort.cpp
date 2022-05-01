#include <bits/stdc++.h>

using namespace std;
int target[10] = {1, 3, 10, 5, 7, 2, 9, 8, 6, 4};

int *selection(int arr[], int length){
    int index, min, temp;
    for(int i=0; i<length; i++){
        min = arr[i];
        index = i;
        for(int j=i+1; j<length; j++){
            if(arr[j] < min){
                min = arr[j];
                index = j;
            }
        }
        temp = arr[i];
        arr[i] = arr[index];
        arr[index] = temp;
    }
    
    return arr;
}

int main(){
    int length = sizeof(target)/sizeof(int);
    
    int *sorted = selection(target, length);
    for(int i=0; i<length; i++){
        cout << sorted[i] << "\n";
    }
    return 0;
}