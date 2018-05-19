#ifndef __COMMON_H__
#define __COMMON_H__

#include <cstdlib>
#include <cmath>
#include <ctime>
#include <cstring>
#include <limits>
#include <chrono>
#include <thread>
#include <unistd.h>

#include <iostream>
#include <ostream>
#include <fstream>
#include <sstream>
#include <iomanip>

#include <string>
#include <vector>
#include <list>
#include <queue>
#include <unordered_set>
#include <unordered_map>

#include <functional>
#include <utility>

#include "color.h"
#include "dsets.h"


using std::size_t;
using std::numeric_limits;
using std::system;

using std::cout;
using std::endl;
using std::setw;
using std::ifstream;
using std::stringstream;

using std::string;
using std::vector;
using std::list;
using std::queue;
using std::priority_queue;
using std::unordered_set;
using std::unordered_map;

using std::less;
using std::hash;

using std::pair;
using std::make_pair;

using std::unordered_map;


enum DIR { UP, DOWN, LEFT, RIGHT };


/****************************************************
 *                      Scorer                      *
 ****************************************************/
static size_t ORDER;


template <typename T>
struct OrderScorer
{
    size_t operator() (const T& s)
    {
        return ++ORDER;
    }
};

template <typename T>
struct GreedyScorer
{
    size_t operator() (const T& s)
    {
        return s.heuristic();
    }
};

template <typename T>
struct AStarScorer
{
    size_t operator() (const T& s)
    {
        return s.heuristic() + s.get_step();
    }
};

template <typename T>
struct AStarInflateScorer
{
    size_t operator() (const T& s)
    {
        return s.heuristic(5) + s.get_step();
    }
};

/****************************************************
 *                    Comparator                    *
 ****************************************************/
template <typename T>
struct HigherBetter
{
    bool operator() (const T* x, const T* y)
    {
        return x->operator<(*y);
    }
};
template <typename T>
struct LowerBetter
{
    bool operator() (const T* x, const T* y)
    {
        return y->operator<(*x);
    }
};

/****************************************************
 *                      Hasher                      *
 ****************************************************/
template <typename T>
struct StateHash
{
    size_t operator() (const T& s) const
    {
        return hash<string>()(s.to_string());
    }
};
template <typename T>
struct StateHash_wp
{
	size_t operator() (const T& s) const
	{
		return hash<string>()(s.to_string_wp());
	}
};

struct PairHash {
public:
    template <typename T, typename U>
    std::size_t operator()(const std::pair<T, U> &x) const
    {
        return std::hash<T>()(x.first) ^ std::hash<U>()(x.second);
    }
};

pair<int, int> calc_pos(pair<int, int> pos, DIR dir)
{
    switch (dir)
    {
        case UP:
        return make_pair(pos.first - 1, pos.second);
        case DOWN:
        return make_pair(pos.first + 1, pos.second);
        case LEFT:
        return make_pair(pos.first, pos.second - 1);
        case RIGHT:
        return make_pair(pos.first, pos.second + 1);
    }
}

inline bool is_bounded(int row, int col, pair<int, int> pos)
{
    return pos.first >= 0 && pos.first < row && pos.second >= 0 && pos.second < col;
}

#endif