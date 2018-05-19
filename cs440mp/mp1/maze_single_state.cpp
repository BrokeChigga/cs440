/****************************************************
 *             Maze Single State Class              *
 ****************************************************/
template <typename T>
MazeSingleGoalState<T>::MazeSingleGoalState(string filename) : State<T>(filename)
{
    for (int i = 0; i < this->get_row(); i++)
    {
        for (int j = 0; j < this->get_col(); j++)
        {
            if ((*this)[i][j].is_goal())
                goal = make_pair(i, j);
        }
    }
}

template <typename T>
MazeSingleGoalState<T>::MazeSingleGoalState(const State<T>& state, int r, int c)
{
    this->row = state.row;
    this->col = state.col;
    this->player_pos = state.player_pos;
    this->table = state.table;
    this->order = state.order;
    this->step = state.step;
    this->parent = state.parent;
    for (int i = 0; i < this->get_row(); i++)
    {
        for (int j = 0; j < this->get_col(); j++)
        {
            if ((i != r || j != c) && this->table[i][j].is_goal())
            {
                this->table[i][j].set_goal(false);
                this->table[i][j].set_char(' ');
            }
        }
    }
    goal = make_pair(r, c);
}

template <typename T>
size_t MazeSingleGoalState<T>::heuristic() const
{
    int diffx = goal.first - this->player_pos.first;
    int diffy = goal.second - this->player_pos.second;
    return abs(diffx) + abs(diffy);
}

template <typename T>
vector<MazeSingleGoalState<T>* > MazeSingleGoalState<T>::expand()
{
    vector<MazeSingleGoalState*> ret;
    if (this->can_perform(UP))
    {
        MazeSingleGoalState* tmp = new MazeSingleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(UP);
        ret.push_back(tmp);
    }
    if (this->can_perform(DOWN))
    {
        MazeSingleGoalState* tmp = new MazeSingleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(DOWN);
        ret.push_back(tmp);
    }
    if (this->can_perform(LEFT))
    {
        MazeSingleGoalState* tmp = new MazeSingleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(LEFT);
        ret.push_back(tmp);
    }
    if (this->can_perform(RIGHT))
    {
        MazeSingleGoalState* tmp = new MazeSingleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(RIGHT);
        ret.push_back(tmp);
    }
    return ret;
}

template <typename T>
bool MazeSingleGoalState<T>::is_goal()
{
    return (*this)[this->player_pos.first][this->player_pos.second].is_goal();
}

template <typename T>
std::ostream & operator<<(std::ostream & out, const MazeSingleGoalState<T>& state)
{
    out << static_cast<const State<T>&>(state);
    out << "Player at (" << state.player_pos.first << ", " << state.player_pos.second << ")" << endl;
    int h = state.heuristic();
    out << "Heuristic: " << h + state.get_step() << " = Step " << state.get_step() << " + Distance " << h << endl;
    out << "Order: " << state.get_order() << endl;
    out << "Goal: (" << state.goal.first << ", " << state.goal.second << ")" << endl;
    return out;
}