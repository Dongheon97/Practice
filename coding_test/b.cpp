#include <bits/stdc++.h>

using namespace std;
struct Point{
    int y, x, z;
    Point(int y, int x): y(y), x(x), z(z){}
    Point(){
        y=-1; 
        x=-1;
        z=-1;
    }
    bool operator < (const Point &a) const{     // 1) y, 2) x, 3) z
        if (y==a.y){
            if(x==a.x){
                return z<a.z;
            }
            return x>a.x;
        }
        return y < a.y;
    }
    /*
    bool operator < (const Point &a) const{     // 1) x, 2) y
        if(x == a.x){
            return y < a.y;
        }
        return x < a.x;
    }
    */

};
struct percent{
    int x, y;
    double w, d, l;
} a[6];

vector<Point> v;

int main(){
    for(int i=10; i>=1; i--){
        Point a = {i, i};
        v.push_back(a);
    }
    Point aa = {3, 4};
    Point ab = {5, 4};
    Point ac = {3, 10};
    v.push_back(aa);
    v.push_back(ab);
    v.push_back(ac);

    sort(v.begin(), v.end());
    
    for(auto it : v){
        cout << it.y << " : " << it.x << "\n";
    }

    return 0;
}