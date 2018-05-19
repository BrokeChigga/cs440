/****************************************************
 *                   State Class                    *
 ****************************************************/

template <typename T>
string State<T>::to_string() const
{
    stringstream ss;
    for (int i = 0; i < this->row; i++)
    {
        for (int j = 0; j < this->col; j++)
        {
            const T& temp = this->table[i][j];
            ss << temp.get_char();
        }
        ss << endl;
    }
    return ss.str();
}

template <typename T>
string State<T>::to_string_wp() const
{
	stringstream ss;
	for (int i = 0; i < this->row; i++)
	{
		for (int j = 0; j < this->col; j++)
		{
            const T& temp = this->table[i][j];
            if (temp.get_char() == 'P')
                ss << ' ';
            else
                ss << temp.get_char();
		}
		ss << endl;
	}
    return ss.str();
}

template <typename T>
State<T>::State(string filename)
{
    row = col = step = order = 0;
    parent = NULL;
    ifstream input(filename.c_str());
    for (string line; getline(input, line); )
    {
        vector<T> row_vec;
        col = 0;
        for (int i = 0; i < line.length(); i++)
        {
            if (line[i] != '%' && line[i] != ' ' && line[i] != '.' &&
                line[i] != 'P' && line[i] != 'B' && line[i] != 'b')
            {
                continue;
            }
            T temp(this, line[i], row, col);
            if (line[i] == 'P')
            {
                player_pos = make_pair(row, i);
                temp.set_start();
            }
            row_vec.push_back(temp);
            col++;
        }
        table.push_back(row_vec);
        row++;
    }
}

template <typename T>
vector<T>& State<T>::operator[](int index)
{
    return table[index];
}

template <typename T>
bool State<T>::operator==(const State& obj) const
{
    return row == obj.row && col == obj.col && table == obj.table;
}

template <typename T>
void State<T>::reset_cell_parent()
{
    for (auto& v : table)
    {
        for (auto& c : v)
            c.set_parent(this);
    }
}

template <typename T>
bool State<T>::can_perform(DIR dir)
{
    pair<int, int> new_pos = calc_pos(player_pos, dir);
    if (!is_bounded(row, col, new_pos))
        return false;
    return table[player_pos.first][player_pos.second].can_leave(dir)
            && table[new_pos.first][new_pos.second].can_enter(dir);
}

template <typename T>
void State<T>::perform(DIR dir)
{
    if (can_perform(dir))
    {
        pair<int, int> new_pos = calc_pos(player_pos, dir);
        table[player_pos.first][player_pos.second].leave(dir);
        table[new_pos.first][new_pos.second].enter(dir);
        player_pos = new_pos;
    }
}

template <typename T>
std::ostream & operator<<(std::ostream & out, const State<T>& state)
{
    out << "Row: " << state.row << "  Col: " << state.col << endl;
    for (int i = 0; i < state.row; i++)
    {
        for (int j = 0; j < state.col; j++)
        {
            const T& temp = state.table[i][j];
            out << temp;
        }
        out << endl;
    }
	return out;
}
