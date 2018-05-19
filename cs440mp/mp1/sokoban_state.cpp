/****************************************************
 *                Sokoban State Class               *
 ****************************************************/
#include "Hungarian.h"
#include "algs.h"

typedef std::vector<double> Row;
typedef std::vector<Row> Matrix;

template <typename T>
SokobanState<T>::SokobanState(string filename) : State<T>(filename)
{
}

template <typename T>
size_t SokobanState<T>::heuristic() const
{
    SokobanState<T> curr_state(*this);
    int matrixSize = 0;
    
    vector<SokobanCell*> boxList;
    vector<SokobanCell*> goalList;
    
    for (auto& v1 : curr_state.table)
    {
        for (auto& c1 : v1)
        {
            if(c1.is_box())
            {
                boxList.push_back(&c1);
                matrixSize++;
            }
            
            if(c1.is_goal())
            {
                goalList.push_back(&c1);
            }
            
        }
    }

    Row boxrow(matrixSize, 0);
    Matrix distanceMatrix(matrixSize, boxrow);
    
    for(int i = 0; i < matrixSize; i++)
    {
        SokobanCell* start = boxList[i];
        pair<int, int> startPos = start->get_position();
        
        clearBFSInfo(curr_state);
        bfs(curr_state, startPos);
        
        for(int j = 0; j < matrixSize; j++)
        {
            double bfsDistance = goalList[j]->get_bfs_distance();
            if(bfsDistance < 0)
            {
                cout << "bfs distance is less than 0" << endl;
                distanceMatrix[i][j] = numeric_limits<int>::max();
            }
            else
            {
                distanceMatrix[i][j] = goalList[j]->get_bfs_distance();
            }
            
        }
    }
    
    HungarianAlgorithm HungAlgo;
    vector<int> assignment;
    
    double retCost = HungAlgo.Solve(distanceMatrix, assignment);

    clearBFSInfo(curr_state);
	bfs(curr_state, curr_state.player_pos);

	//calculate the length of path to the nearest goal
	int path_length = numeric_limits<int>::max();
  	for (auto& v : curr_state.table)
    {
      	for (auto& c : v)
        {
          	if (c.is_box() && c.get_bfs_distance() < path_length)
              	path_length = c.get_bfs_distance();
        }
    }

    return retCost + path_length;
}

template <typename T>
vector<SokobanState<T>* > SokobanState<T>::expand(bool ignore_player = false)
{
    vector<SokobanState*> ret;
    if (ignore_player)
    {
        clearBFSInfo(*this);
        bfs(*this, this->player_pos, false);

        auto player_pos_back = this->player_pos;
        for (auto& v : this->table)
        {
            for (auto& c : v)
            {
                if (c.is_box())
                {
                    pair<int, int> mypos = c.get_position();
                    pair<int, int> myleft = make_pair(mypos.first, mypos.second-1);
                    pair<int, int> myright = make_pair(mypos.first, mypos.second+1);
                    pair<int, int> myup = make_pair(mypos.first-1, mypos.second);
                    pair<int, int> mydown = make_pair(mypos.first+1, mypos.second);
                    if (is_bounded(this->get_row(), this->get_col(), myleft) 
                        && this->get_cell(myleft).is_bfs_explored()
                        && !this->get_cell(myleft).is_wall()
                        && !this->get_cell(myleft).is_box())
                    {
                        this->player_pos = myleft;
                        if (this->can_perform(RIGHT))
                        {
                            SokobanState* tmp = new SokobanState(*this);
                            tmp->reset_cell_parent();
                            tmp->table[player_pos_back.first][player_pos_back.second].leave(RIGHT);
                            tmp->table[mypos.first][mypos.second].enter(RIGHT);
                            tmp->player_pos = mypos;
                            ret.push_back(tmp);
                        }
                    }

                    if (is_bounded(this->get_row(), this->get_col(), myright) 
                        && this->get_cell(myright).is_bfs_explored()
                        && !this->get_cell(myright).is_wall()
                        && !this->get_cell(myright).is_box())
                    {
                        this->player_pos = myright;
                        if (this->can_perform(LEFT))
                        {
                            SokobanState* tmp = new SokobanState(*this);
                            tmp->reset_cell_parent();
                            tmp->table[player_pos_back.first][player_pos_back.second].leave(LEFT);
                            tmp->table[mypos.first][mypos.second].enter(LEFT);
                            tmp->player_pos = mypos;
                            ret.push_back(tmp);
                        }
                    }

                    if (is_bounded(this->get_row(), this->get_col(), myup) 
                        && this->get_cell(myup).is_bfs_explored()
                        && !this->get_cell(myup).is_wall()
                        && !this->get_cell(myup).is_box())
                    {
                        this->player_pos = myup;
                        if (this->can_perform(DOWN))
                        {
                            SokobanState* tmp = new SokobanState(*this);
                            tmp->reset_cell_parent();
                            tmp->table[player_pos_back.first][player_pos_back.second].leave(DOWN);
                            tmp->table[mypos.first][mypos.second].enter(DOWN);
                            tmp->player_pos = mypos;
                            ret.push_back(tmp);
                        }
                    }

                    if (is_bounded(this->get_row(), this->get_col(), mydown) 
                        && this->get_cell(mydown).is_bfs_explored()
                        && !this->get_cell(mydown).is_wall()
                        && !this->get_cell(mydown).is_box())
                    {
                        this->player_pos = mydown;
                        if (this->can_perform(UP))
                        {
                            SokobanState* tmp = new SokobanState(*this);
                            tmp->reset_cell_parent();
                            tmp->table[player_pos_back.first][player_pos_back.second].leave(UP);
                            tmp->table[mypos.first][mypos.second].enter(UP);
                            tmp->player_pos = mypos;
                            ret.push_back(tmp);
                        }
                    }
                }
            }
        }
        this->player_pos = player_pos_back;
    }
    else
    {
        if (this->can_perform(UP))
        {
            SokobanState* tmp = new SokobanState(*this);
            tmp->reset_cell_parent();
            tmp->perform(UP);
            ret.push_back(tmp);
        }
        if (this->can_perform(DOWN))
        {
            SokobanState* tmp = new SokobanState(*this);
            tmp->reset_cell_parent();
            tmp->perform(DOWN);
            ret.push_back(tmp);
        }
        if (this->can_perform(LEFT))
        {
            SokobanState* tmp = new SokobanState(*this);
            tmp->reset_cell_parent();
            tmp->perform(LEFT);
            ret.push_back(tmp);
        }
        if (this->can_perform(RIGHT))
        {
            SokobanState* tmp = new SokobanState(*this);
            tmp->reset_cell_parent();
            tmp->perform(RIGHT);
            ret.push_back(tmp);
        }
    }
    return ret;
}

template <typename T>
bool SokobanState<T>::is_goal()
{
    bool ret = true;
    for (auto& v : this->table)
    {
        for (auto& c : v)
        {
            ret = ret && (c.is_goal() == c.is_box());
        }
    }
    return ret;
}


template <typename T>
std::ostream & operator<<(std::ostream & out, const SokobanState<T>& state)
{
    out << static_cast<const State<T>&>(state);
    out << "Player at (" << state.player_pos.first << ", " << state.player_pos.second << ")" << endl;
    int h = state.heuristic();
    out << "Heuristic: " << h + state.get_step() << " = Step " << state.get_step() << " + Distance " << h << endl;
    out << "Order: " << state.get_order() << endl;
    return out;
}
