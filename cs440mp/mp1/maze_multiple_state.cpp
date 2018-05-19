/****************************************************
 *            Maze Multiple State Class             *
 ****************************************************/


unordered_map<MazeMultipleGoalState<MazeCell>, int, StateHash_wp<MazeMultipleGoalState<MazeCell> > > mst_cost_map;

template <typename T>
MazeMultipleGoalState<T>::MazeMultipleGoalState(string filename) : State<T>(filename)
{
    for (int i = 0; i < this->get_row(); i++)
    {
        for (int j = 0; j < this->get_col(); j++)
        {
            if ((*this)[i][j].is_goal())
                goals.insert(make_pair(i, j));
        }
    }
    show_numbering = goals.size() < 35;
}

template <typename T>
size_t MazeMultipleGoalState<T>::heuristic(int multiplier = 1) const
{
    MazeMultipleGoalState<T> copy(*this);

	int mst_cost = -1;
    if (mst_cost_map.find(copy) != mst_cost_map.end())
    {
        mst_cost = mst_cost_map[copy];
    }
    else
    {
		mst_cost = mst(copy);
        mst_cost_map[copy] = mst_cost;
	}
    
    clearBFSInfo(copy);
	bfs(copy, copy.player_pos);

	//calculate the length of path to the nearest goal
	int path_length = numeric_limits<int>::max();
  	for (auto& v : copy.table)
    {
      	for (auto& c : v)
        {
          	if (c.is_goal() && c.get_bfs_distance() < path_length)
              	path_length = c.get_bfs_distance();
        }
    }

    return multiplier * mst_cost + path_length;
}

template <typename T>
vector<MazeMultipleGoalState<T>* > MazeMultipleGoalState<T>::expand()
{
    vector<MazeMultipleGoalState*> ret;
    if (this->can_perform(UP))
    {
        MazeMultipleGoalState* tmp = new MazeMultipleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(UP);
        ret.push_back(tmp);
    }
    if (this->can_perform(DOWN))
    {
        MazeMultipleGoalState* tmp = new MazeMultipleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(DOWN);
        ret.push_back(tmp);
    }
    if (this->can_perform(LEFT))
    {
        MazeMultipleGoalState* tmp = new MazeMultipleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(LEFT);
        ret.push_back(tmp);
    }
    if (this->can_perform(RIGHT))
    {
        MazeMultipleGoalState* tmp = new MazeMultipleGoalState(*this);
        tmp->reset_cell_parent();
        tmp->perform(RIGHT);
        ret.push_back(tmp);
    }
    return ret;
}

template <typename T>
bool MazeMultipleGoalState<T>::is_goal()
{
    return goals.empty();
}

template <typename T>
void MazeMultipleGoalState<T>::process_enter(int r, int c, DIR dir)
{
    auto it = this->goals.find(make_pair(r, c));
    if (it != this->goals.end())
    {
        this->goals.erase(it);
        if (show_numbering)
        {
            this->get_cell(*it).set_goal_number(num);
            num++;
            if (num == 58)
                num = 97;
        }
    }
}

template <typename T>
std::ostream & operator<<(std::ostream & out, const MazeMultipleGoalState<T>& state)
{
    out << static_cast<const State<T>&>(state);
    out << "Player at (" << state.player_pos.first << ", " << state.player_pos.second << ")" << endl;
    int h = state.heuristic();
    out << "Heuristic: " << h + state.get_step() << " = Step " << state.get_step() << " + Distance " << h << endl;
    out << "Order: " << state.get_order() << endl;
    // out << "Goal(s): " << endl;
    // int counter = 1;
    // for (auto g : state.goals)
    // {
    //     cout << "\t";
    //     cout << std::setw(3) << std::left << (counter++) << ": ";
    //     cout << "(" << g.first << ", " << g.second << ")" << endl;
    // }
    return out;
}
