#ifndef __ALGS_H__
#define __ALGS_H__

#include "common.h"
#include "state.h"
#include "cell.h"
#include "tree_search.h"

struct Edge
{
	int start, end, dist;
  	Edge(int s, int e, double d) : start(s), end(e), dist(d) {}
	bool operator< (const Edge& other) const
	{
		return other.dist < this->dist;
	}
};

template <typename T>
void bfs(State<T>& curState, pair<int, int> Start, bool skip_box = true)
{
	queue<T*> q;
	curState[Start.first][Start.second].set_bfs_explored();
	curState[Start.first][Start.second].set_bfs_distance(0);
	q.push(&curState[Start.first][Start.second]);
	while (!q.empty()) {
		T* mycell = q.front();
		double cur_distance = mycell->get_bfs_distance();
		cur_distance++;
		q.pop();

		//go through four directions
		pair<int, int> mypos = mycell->get_position();
		pair<int, int> myleft = make_pair(mypos.first, mypos.second-1);
		pair<int, int> myright = make_pair(mypos.first, mypos.second+1);
		pair<int, int> myup = make_pair(mypos.first-1, mypos.second);
		pair<int, int> mydown = make_pair(mypos.first+1, mypos.second);
		if (is_bounded(curState.get_row(), curState.get_col(), myleft) 
			&& !curState.get_cell(myleft).is_bfs_explored()
			&& !curState.get_cell(myleft).is_wall()
			&& (skip_box || !curState.get_cell(myleft).is_box()))
		{
			curState.get_cell(myleft).set_bfs_explored();
			curState.get_cell(myleft).set_bfs_distance(cur_distance);
			q.push(&curState.get_cell(myleft));
		}

		if (is_bounded(curState.get_row(), curState.get_col(), myright) 
			&& !curState.get_cell(myright).is_bfs_explored()
			&& !curState.get_cell(myright).is_wall()
			&& (skip_box || !curState.get_cell(myright).is_box()))
		{
			curState.get_cell(myright).set_bfs_explored();
			curState.get_cell(myright).set_bfs_distance(cur_distance);
			q.push(&curState.get_cell(myright));
		}

		if (is_bounded(curState.get_row(), curState.get_col(), myup) 
			&& !curState.get_cell(myup).is_bfs_explored()
			&& !curState.get_cell(myup).is_wall()
			&& (skip_box || !curState.get_cell(myup).is_box()))
		{
			curState.get_cell(myup).set_bfs_explored();
			curState.get_cell(myup).set_bfs_distance(cur_distance);
			q.push(&curState.get_cell(myup));
		}

		if (is_bounded(curState.get_row(), curState.get_col(), mydown) 
			&& !curState.get_cell(mydown).is_bfs_explored()
			&& !curState.get_cell(mydown).is_wall()
			&& (skip_box || !curState.get_cell(mydown).is_box()))
		{
			curState.get_cell(mydown).set_bfs_explored();
			curState.get_cell(mydown).set_bfs_distance(cur_distance);
			q.push(&curState.get_cell(mydown));
		}
	}
}

template <typename T>
void clearBFSInfo(State<T>& state)
{
  	for (auto& v : state.table)
		for (auto& c : v)
		{
			c.set_bfs_unexplored();
			c.set_bfs_distance(-1);
		}
}

template <typename T>
int mst(MazeMultipleGoalState<T>& state)
{
	priority_queue<Edge> pq;
  	vector<pair<int, int> > calced_goals;
	clearBFSInfo(state);
	for (auto& pos : state.goals)
    {
      	bfs(state, pos);
      	calced_goals.push_back(pos);

      	for (auto& pos2 : state.goals)
        {
			if (pos == pos2) continue;
			if (state[pos2.first][pos2.second].get_bfs_distance() > 0)
			{
				Edge edge(pos.first * state.get_col() + pos.second, 
						pos2.first * state.get_col() + pos2.second, 
						state[pos2.first][pos2.second].get_bfs_distance());
				pq.push(edge);
			}
        }
        
      	clearBFSInfo(state);
      	for (auto visited : calced_goals)
			state[visited.first][visited.second].set_bfs_explored();
    }
	
  	DisjointSets ds;
  	ds.addelements(state.get_row() * state.get_col());
  	int edge_count = 0, mst_cost = 0;
  	while (!pq.empty() && edge_count < state.goals.size() - 1)
    {
      	Edge edge = pq.top();
      	pq.pop();
      	if (ds.find(edge.start) == ds.find(edge.end)) continue;
      	ds.setunion(edge.start, edge.end);
      	mst_cost += edge.dist;
    }
  	return mst_cost;
}

#endif
