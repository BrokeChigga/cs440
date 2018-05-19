#ifndef __CELL_H__
#define __CELL_H__

#define FANCY 

#include "common.h"

/****************************************************
 *                 Maze Cell Class                  *
 ****************************************************/
class MazeCell
{
    char _character;
    bool _is_wall, _is_goal, _is_player, _is_start;
    bool _explored;
    int _row, _col;
    int _enter_count;
    char _goal_num;

    bool _bfs_explored;
    double _bfs_distance;

    State<MazeCell>* _parent;
public:
    MazeCell(State<MazeCell>* parent, char c, int i, int j)
    {
        this->_parent = parent;
        this->_character = c;
        this->_row = i;
        this->_col = j;
        this->_is_wall = c == '%';
        this->_is_goal = c == '.';
        this->_is_player = c == 'P';
        this->_goal_num = ' ';
        this->_explored = false;
        this->_enter_count = 0;
        this->_is_start = false;

        this->_bfs_explored = false;
        this->_bfs_distance = -1;
    }

    pair<int, int> get_position() const { return make_pair(_row, _col); }
    char get_char() const { return _character; }

    bool operator==(const MazeCell& obj) const
    {
        return _character == obj._character;
    }

    bool is_wall() const { return _is_wall; }
    bool is_goal() const { return _is_goal; }
    bool is_player() const { return _is_player; }
    bool can_enter(DIR dir) const { return !_is_wall; }
    bool can_leave(DIR dir) const { return true; }
    void set_explored() { _explored = true; }
    void set_parent(State<MazeCell>* parent) { _parent = parent; }
    void set_start() { _is_start = true; }
    void set_goal(bool g) { _is_goal = g; }
    void set_goal_number(char num) { _goal_num = num; }
    char get_goal_number() const { return _goal_num; }
    void set_char(char c) { _character = c; }
    bool is_explored() const { return _explored; }
    bool is_start() const { return _is_start; }
    bool is_box() const { return false; }
    int get_enter_count() const { return _enter_count; }

    bool is_bfs_explored() const { return _bfs_explored; }
    void set_bfs_explored() { _bfs_explored = true; }
    void set_bfs_unexplored() { _bfs_explored = false; }
    double get_bfs_distance() const { return _bfs_distance; }
    void set_bfs_distance(double d) { _bfs_distance = d; }


    void enter(DIR dir)
    {
        _character = 'P';
        _is_player = true;
        _enter_count++;
        _parent->process_enter(_row, _col, dir);
    }
    void leave(DIR dir)
    {
        _character = ' ';
        if (_is_goal)
        {
            _is_goal = false;
        }
        if (_is_player)
        {
            _explored = true;
            _is_player = false;
        }
        _parent->process_leave(_row, _col, dir);
    }
};

std::ostream & operator<<(std::ostream & out, const MazeCell & cell)
{
#ifdef FANCY
    if (cell.get_char() == 'P')
        out << Color::FG_B_RED << "P" << Color::RESET;
    else if (cell.is_goal())
        out << Color::FG_B_GREEN << "G" << Color::RESET;
    else if (cell.is_start())
        out << Color::FG_B_RED << "S" << Color::RESET;
    else if (cell.is_wall())
        out << Color::FG_B_CYAN << "\u2588" << Color::RESET;
    else if (cell.is_explored())
    {
        switch (cell.get_enter_count())
        {
            case 2: out << Color::FG_B_MAGENTA; break;
            case 3: out << Color::FG_B_BLUE; break;
            case 4: out << Color::FG_B_GREEN; break;
            case 5: out << Color::FG_B_WHITE; break;
            case 6: out << Color::FG_B_RED; break;
            case 7: out << Color::FG_B_CYAN; break;
            default: out << Color::FG_B_YELLOW; break;
        }
        if (cell.get_goal_number() != ' ')
            out << cell.get_goal_number() << Color::RESET;
        else
            out << "." << Color::RESET;
    }
#else
    if (cell.is_player())
        out << "P";
    else if (cell.is_explored() && cell.get_goal_number() != ' ')
        out << cell.get_goal_number();
    else if (cell.is_explored())
        out << ".";
#endif
    else
        out << Color::FG_DEFAULT << cell.get_char() << Color::RESET;
	return out;
}


/****************************************************
 *                Sokoban Cell Class                *
 ****************************************************/
class SokobanCell
{
    char _character;
    bool _is_wall, _is_box, _is_goal, _is_player, _is_start;
    bool _explored;
    int _row, _col;
    int _enter_count;
    
    bool _bfs_explored;
    double _bfs_distance;
    
    State<SokobanCell>* _parent;
public:
    SokobanCell(State<SokobanCell>* parent, char c, int i, int j)
    {
        this->_parent = parent;
        this->_character = c;
        this->_row = i;
        this->_col = j;
        this->_is_wall = c == '%';
        this->_is_goal = c == '.' || c == 'B';
        this->_is_box = c == 'b' || c == 'B';
        this->_is_player = c == 'P';
        this->_explored = false;
        this->_enter_count = 0;
        this->_is_start = false;
        
        this->_bfs_explored = false;
        this->_bfs_distance = -1.0;

    }
    
    char get_char() const { return _character; }
    pair<int, int> get_position() const { return make_pair(_row, _col); }
    
    bool operator==(const SokobanCell& obj) const
    {
        return _character == obj._character;
    }
    
    bool is_wall() const { return _is_wall; }
    bool is_goal() const { return _is_goal; }
    bool is_box() const { return _is_box; }
    bool is_player() const { return _is_player; }
    bool can_enter(DIR dir) const
    {
        if (_is_wall)
            return false;
        if (_is_box)
        {
            auto npos = calc_pos(make_pair(_row, _col), dir);
            auto& neighbor = _parent->get_cell(npos.first, npos.second);
            if (neighbor._is_wall || neighbor._is_box)
                return false;
        }
        return true;
    }
    bool can_leave(DIR dir) const { return true; }
    void set_explored() { _explored = true; }
    void set_parent(State<SokobanCell>* parent) { _parent = parent; }
    void set_start() { _is_start = true; }
    bool is_explored() const { return _explored; }
    bool is_start() const { return _is_start; }
    int get_enter_count() const { return _enter_count; }
    
    bool is_bfs_explored() const { return _bfs_explored; }
    void set_bfs_explored() { _bfs_explored = true; }
    void set_bfs_unexplored() { _bfs_explored = false; }
    double get_bfs_distance() const { return _bfs_distance; }
    void set_bfs_distance(double d) { _bfs_distance = d; }
    
    void enter(DIR dir)
    {
        _character = 'P';
        _is_player = true;
        _enter_count++;
        if (_is_box)
        {
            _is_box = false;
            auto npos = calc_pos(make_pair(_row, _col), dir);
            auto& neighbor = _parent->get_cell(npos.first, npos.second);
            neighbor._is_box = true;
            if (neighbor._is_goal)
                neighbor._character = 'B';
            else
                neighbor._character = 'b';
        }
        _parent->process_enter(_row, _col, dir);
    }
    void leave(DIR dir)
    {
        if (_is_player)
        {
            _explored = true;
            _is_player = false;
        }
        if (_is_goal)
            _character = '.';
        else
        {
            _character = ' ';
        }
        _parent->process_leave(_row, _col, dir);
    }
};

std::ostream & operator<<(std::ostream & out, const SokobanCell & cell)
{
#ifdef FANCY
    if (cell.get_char() == 'P' && cell.is_goal())
        out << Color::FG_B_RED << "P" << Color::RESET;
    else if (cell.get_char() == 'P')
        out << Color::FG_B_BLUE << "P" << Color::RESET;
    else if (cell.is_goal() && cell.is_box())
        out << Color::FG_B_GREEN << "\u25A0" << Color::RESET;
    else if (cell.is_goal())
        out << Color::FG_B_RED << "\u2022" << Color::RESET;
    else if (cell.is_box())
        out << Color::FG_B_YELLOW << "\u25A0" << Color::RESET;
    else if (cell.is_start())
        out << Color::FG_B_WHITE << "S" << Color::RESET;
    else if (cell.is_wall())
        out << Color::FG_B_BLACK << "\u2588" << Color::RESET;
    else if (cell.is_explored())
    {
        switch (cell.get_enter_count())
        {
            case 2: out << Color::FG_B_MAGENTA; break;
            case 3: out << Color::FG_B_GREEN; break;
            case 4: out << Color::FG_B_CYAN; break;
            case 5: out << Color::FG_B_RED; break;
            case 6: out << Color::FG_B_BLUE; break;
            case 7: out << Color::FG_B_WHITE; break;
            default: out << Color::FG_B_YELLOW; break;
        }
        out << "." << Color::RESET;
    }
#else
    if (cell.is_player())
        out << "P";
    else if (cell.is_goal() && cell.is_box())
        out << "B";
    else if (cell.is_goal())
        out << ".";
    else if (cell.is_box())
        out << "b";
#endif
    else
        out << Color::FG_DEFAULT << cell.get_char() << Color::RESET;
	return out;
}

#endif
