#ifndef __TREE_SEARCH_H__
#define __TREE_SEARCH_H__

#define DEBUG_SLEEP 
#define DEBUG_SLEEP_INTERVAL 100

#include "common.h"

template <
    class T, 
    class Scorer, 
    class Container = vector<T*>, 
    class Compare = less<typename Container::value_type>, 
    class Hash = hash<T> >
class TreeSearch
{
    int expansion_count;
    int step_count;
    vector<T*>* garbage_collection;
    void clear();
    list<T*> trace_solution(T* final_state);
public:
    TreeSearch() { garbage_collection = NULL; step_count = 0; }
    ~TreeSearch();
    list<T*> search(T& start_state, bool can_repeat = true, bool ignore_player = false, bool debug = false);
    int get_expansion_count() { return expansion_count; }
    int get_step_count() { return step_count; }
};

#include "tree_search.cpp"
#endif
