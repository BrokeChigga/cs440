#include "tree_search.h"

template<typename T> void print_queue(T q) {
    while(!q.empty()) {
        cout << q.top()->get_order() << " ";
        q.pop();
    }
    cout << '\n';
}

template <class T, class Scorer, class Container, class Compare, class Hash>
TreeSearch<T, Scorer, Container, Compare, Hash>::~TreeSearch()
{
    clear();
}

template <class T, class Scorer, class Container, class Compare, class Hash>
void TreeSearch<T, Scorer, Container, Compare, Hash>::clear()
{
    if (garbage_collection != NULL)
    {
        for (auto it = garbage_collection->begin(); it != garbage_collection->end(); it++)
            delete *it;
    }
    delete garbage_collection;
    garbage_collection = NULL;
}

template <class T, class Scorer, class Container, class Compare, class Hash>
list<T*> TreeSearch<T, Scorer, Container, Compare, Hash>::search(T& start_state, bool can_repeat, bool ignore_player, bool debug)
{
    priority_queue<T*, Container, Compare> pq;
    unordered_set<T, Hash> explored_set;
    expansion_count = step_count = 0;
    clear();
    garbage_collection = new vector<T*>();
    Scorer scorer;

    start_state.set_step(0);
    start_state.set_order(scorer(start_state));
    pq.push(&start_state);
    while (!pq.empty())
    {
        T* state = pq.top();
        pq.pop();

        if (!can_repeat)
        {
            if (explored_set.find(*state) != explored_set.end())
                continue;
            else
                explored_set.insert(*state);
        }

        if (debug)
        {
            system("clear");
            cout << "Poped [Order=" << state->get_order() << "]" << endl;
            cout << *state;
        }

        if (state->is_goal())
            return this->trace_solution(state);
        
        vector<T*> children;
        if (ignore_player)
            children = state->expand(true);
        else
            children = state->expand();
        expansion_count++;
        if (debug)
        {
            cout << children.size() << " Children" << endl;
        }
        for (T* child : children)
        {
            garbage_collection->push_back(child);
            child->set_parent(state);
            child->set_step(state->get_step() + 1);
            child->set_order(scorer(*child));
            pq.push(child);
            
            if (debug)
            {
                cout << "Pushed. [Order=" << child->get_order() << "]" << endl;
            }
        }

#ifdef DEBUG_SLEEP
        if (debug)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(DEBUG_SLEEP_INTERVAL));
        }
#endif

    }
    return list<T*>();
}

template <class T, class Scorer, class Container, class Compare, class Hash>
list<T*> TreeSearch<T, Scorer, Container, Compare, Hash>::trace_solution(T* final_state)
{
    list<T*> ret;
    while (final_state != NULL)
    {
        ret.push_front(final_state);
        step_count++;
        final_state = static_cast<T*>(final_state->get_parent());
    }
    return ret;
}
