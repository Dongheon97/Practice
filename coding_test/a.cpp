#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int v[10];

vector<string> split(string input, string delimiter){
    vector<string> ret;
    long long pos;
    string token = "";
    while ((pos=input.find(delimiter)) != string::npos){
        token = input.substr(0, pos);
        ret.push_back(token);
        input.erase(0, pos+delimiter.length());
    }
    ret.push_back(input);
    return ret;
}

int main(){
    unordered_map<string, int> umap;
    umap.emplace("test3", 3);
    umap.emplace("test4", 4);
    umap.emplace("test1", 1);
    umap.emplace("test2", 2);

    map<string, int> omap;
    omap.emplace("test3", 3);
    omap.emplace("test4", 4);
    omap.emplace("test1", 1);
    omap.emplace("test2", 2);


    for(auto element : umap){
        cout << element.first << " :: " << element.second << "\n";
    }
    cout << "\n";
    
    for(auto element : omap){
        cout << element.first << " :: " << element.second << "\n";
    }
    cout << "\n";

    auto search = umap.find("test4");
    cout << typeid(search).name();
    if(search != umap.end()){
        cout << "found: " << (*search).first << " " << search->second << "\n";
    }
    cout << "\n";
    string s = "Hello, My name is Dongheon Lee!";
    string d = " ";
    vector<string> splited = split(s, d);
    for (auto a:splited){
        cout << a << "\n";
    }    

    return 0;
}

