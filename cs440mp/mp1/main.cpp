#include "common.h"
#include "state.h"
#include "cell.h"
#include "tree_search.h"
#include "algs.h"

int main()
{
    {
        TreeSearch<
            MazeSingleGoalState<MazeCell>, 
            OrderScorer<MazeSingleGoalState<MazeCell> >, 
            vector<MazeSingleGoalState<MazeCell>* >, 
            HigherBetter<MazeSingleGoalState<MazeCell> >, 
            StateHash<MazeSingleGoalState<MazeCell> > > ts_dfs;
        TreeSearch<
            MazeSingleGoalState<MazeCell>, 
            OrderScorer<MazeSingleGoalState<MazeCell> >, 
            vector<MazeSingleGoalState<MazeCell>* >, 
            LowerBetter<MazeSingleGoalState<MazeCell> >, 
            StateHash<MazeSingleGoalState<MazeCell> > > ts_bfs;
        TreeSearch<
            MazeSingleGoalState<MazeCell>, 
            GreedyScorer<MazeSingleGoalState<MazeCell> >, 
            vector<MazeSingleGoalState<MazeCell>* >, 
            LowerBetter<MazeSingleGoalState<MazeCell> >, 
            StateHash<MazeSingleGoalState<MazeCell> > > ts_greedy;
        TreeSearch<
            MazeSingleGoalState<MazeCell>, 
            AStarScorer<MazeSingleGoalState<MazeCell> >, 
            vector<MazeSingleGoalState<MazeCell>* >, 
            LowerBetter<MazeSingleGoalState<MazeCell> >, 
            StateHash<MazeSingleGoalState<MazeCell> > > ts_astar;


        MazeSingleGoalState<MazeCell> start_state1("puzzles/mediumMaze.txt");
        MazeSingleGoalState<MazeCell> start_state2("puzzles/bigMaze.txt");
        MazeSingleGoalState<MazeCell> start_state3("puzzles/openMaze.txt");
        // Medium Maze
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_dfs.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_dfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_greedy.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_greedy.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        // Big Maze
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_dfs.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_dfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_greedy.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_greedy.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        // Open Maze
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_dfs.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_dfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_greedy.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_greedy.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
    }
    

    {
        TreeSearch<
            MazeMultipleGoalState<MazeCell>, 
            AStarScorer<MazeMultipleGoalState<MazeCell> >, 
            vector<MazeMultipleGoalState<MazeCell>* >, 
            LowerBetter<MazeMultipleGoalState<MazeCell> >, 
            StateHash<MazeMultipleGoalState<MazeCell> > > ts_astar;
        TreeSearch<
            MazeMultipleGoalState<MazeCell>, 
            AStarInflateScorer<MazeMultipleGoalState<MazeCell> >, 
            vector<MazeMultipleGoalState<MazeCell>* >, 
            LowerBetter<MazeMultipleGoalState<MazeCell> >, 
            StateHash<MazeMultipleGoalState<MazeCell> > > ts_inflate;

        MazeMultipleGoalState<MazeCell> start_state1("puzzles/tinySearch.txt");
        MazeMultipleGoalState<MazeCell> start_state2("puzzles/smallSearch.txt");
        MazeMultipleGoalState<MazeCell> start_state3("puzzles/mediumSearch.txt");
        MazeMultipleGoalState<MazeCell> start_state4("puzzles/bigDots.txt");

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_inflate.search(start_state4, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            while (true)
            {
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            cout << "Expanded " << ts_inflate.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
            }
        }
    }

    {
        SokobanState<SokobanCell> start_state1("puzzles/sokoban1.txt");
        SokobanState<SokobanCell> start_state2("puzzles/sokoban2.txt");
        SokobanState<SokobanCell> start_state3("puzzles/sokoban3.txt");
        SokobanState<SokobanCell> start_state4("puzzles/sokoban4.txt");
        TreeSearch<
            SokobanState<SokobanCell>, 
            OrderScorer<SokobanState<SokobanCell> >, 
            vector<SokobanState<SokobanCell>* >, 
            LowerBetter<SokobanState<SokobanCell> >, 
            StateHash<SokobanState<SokobanCell> > > ts_bfs;
        TreeSearch<
            SokobanState<SokobanCell>, 
            AStarScorer<SokobanState<SokobanCell> >, 
            vector<SokobanState<SokobanCell>* >, 
            LowerBetter<SokobanState<SokobanCell> >, 
            StateHash<SokobanState<SokobanCell> > > ts_astar;
        
        // BFS
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) *1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_bfs.search(start_state4, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_bfs.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }

        // A*
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) * 1000.0 / CLOCKS_PER_SEC) << " ms elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state4, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            while (true)
            {
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
            }
        }
    }


    {
        SokobanState<SokobanCell> start_state1("puzzles/sokoban_extra1.txt");
        SokobanState<SokobanCell> start_state2("puzzles/sokoban_extra2.txt");
        SokobanState<SokobanCell> start_state3("puzzles/sokoban_extra3.txt");
        TreeSearch<
            SokobanState<SokobanCell>, 
            AStarScorer<SokobanState<SokobanCell> >, 
            vector<SokobanState<SokobanCell>* >, 
            LowerBetter<SokobanState<SokobanCell> >, 
            StateHash<SokobanState<SokobanCell> > > ts_astar;
    
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state1, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state2, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
        {
            cout << "Searching..." << endl;
            clock_t begin = clock();
            auto ans = ts_astar.search(start_state3, false);
            clock_t end = clock();
            cout << (double(end - begin) / CLOCKS_PER_SEC) << " seconds elapsed" << endl;
            cout << "Solution Ready (press any key to continue)" << endl; getchar();
            int step = 0;
            for (auto item : ans)
            {
                system("clear");
                cout << "Step: " << step << endl;
                cout << *item;
                step++;
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
            }
            cout << "Expanded " << ts_astar.get_expansion_count() << " states (press any key to continue)" << endl; getchar();
        }
    }

    return 0;
}
