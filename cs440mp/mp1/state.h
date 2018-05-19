#ifndef __STATE_H__
#define __STATE_H__

#include "common.h"

/****************************************************
 *                   State Class                    *
 ****************************************************/
template <typename T>
class State
{
public:
    int row, col;
    pair<int, int> player_pos;
    vector<vector<T> > table;
    size_t order;
    size_t step;
    State* parent;
    // Constructor
    State() {}
    State(string filename);

    // Getters & setters
    int get_row() const { return row; }
    int get_col() const { return col; }
    T& get_cell(int r, int c) { return table[r][c]; }
    T get_const_cell(int r, int c) const { return table[r][c]; }
    void set_order(size_t o) { this->order = o; }
    size_t get_order() const { return this->order; }
    void set_step(size_t o) { this->step = o; }
    size_t get_step() const { return this->step; }
    void set_parent(State* state_ptr) { this->parent = state_ptr; }
    State* get_parent() { return parent; }
    void reset_cell_parent();

    T& get_cell(pair<int, int> mypair) { return table[mypair.first][mypair.second]; }

    // Methods
    virtual bool can_perform(DIR dir);
    virtual void perform(DIR dir);
    virtual bool is_goal() { return false; }
    virtual void process_enter(int r, int c, DIR dir) { }
    virtual void process_leave(int r, int c, DIR dir) { }
    string to_string() const;

    string to_string_wp() const;

    // Operator Overrides
    virtual bool operator<(const State& obj) const
        { return this->order < obj.order; }
    vector<T>& operator[](int index);
    bool operator==(const State& obj) const;
    template <typename U> friend std::ostream & operator<<(std::ostream & out, const State<U>& state);
};


/****************************************************
 *             Maze Single State Class              *
 ****************************************************/
template <typename T>
class MazeSingleGoalState : public State<T>
{
    pair<int, int> goal;
public:
    // Constructor
    MazeSingleGoalState(string filename);
    MazeSingleGoalState(const State<T>& state, int r, int c);

    size_t heuristic() const;
    vector<MazeSingleGoalState*> expand();
    vector<MazeSingleGoalState*> expand(bool) { return expand(); }
    virtual bool is_goal();

    // Operator Overrides
    bool operator<(const MazeSingleGoalState& obj) const
        { return (this->order < obj.order) || (this->order == obj.order && this->heuristic() < obj.heuristic()); }
    template <typename U> friend std::ostream & operator<<(std::ostream & out, const MazeSingleGoalState<U>& state);
};


/****************************************************
 *            Maze Multiple State Class             *
 ****************************************************/

template <typename T>
class MazeMultipleGoalState : public State<T>
{
public:
    unordered_set<pair<int, int>, PairHash> goals;
    char num = 49;
    bool show_numbering = true;
    // Constructor
    MazeMultipleGoalState(string filename);

    size_t heuristic(int multiplier) const;
    size_t heuristic() const { return heuristic(1); }
    vector<MazeMultipleGoalState*> expand();
    vector<MazeMultipleGoalState*> expand(bool) { return expand(); }
    virtual bool is_goal();
    virtual void process_enter(int r, int c, DIR dir);

    // Operator Overrides
    bool operator<(const MazeMultipleGoalState& obj) const
        { return (this->order < obj.order) || (this->order == obj.order && this->heuristic() < obj.heuristic()); }
    template <typename U> friend std::ostream & operator<<(std::ostream & out, const MazeMultipleGoalState<U>& state);
};


/****************************************************
 *                Sokoban State Class               *
 ****************************************************/

template <typename T>
class SokobanState : public State<T>
{
public:
    // Constructor
    SokobanState(string filename);

    size_t heuristic() const;
    vector<SokobanState*> expand(bool ignore_player);
    virtual bool is_goal();

    // Operator Overrides
    bool operator<(const SokobanState& obj) const
        { return (this->order < obj.order) || (this->order == obj.order && this->heuristic() < obj.heuristic()); }
    template <typename U> friend std::ostream & operator<<(std::ostream & out, const SokobanState<U>& state);
};


#include "cell.h"
#include "tree_search.h"

#include "algs.h"

#include "state.cpp"
#include "maze_single_state.cpp"
#include "maze_multiple_state.cpp"
#include "sokoban_state.cpp"


#endif
