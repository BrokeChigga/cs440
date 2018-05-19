#ifndef DSETS_H
#define DSETS_H

#include <vector>

class DisjointSets
{
    // Private member to store the Uptree structure
    std::vector<int> v;

public:
    /**
     * Creates n unconnected root nodes at the end of the vector.
     *
     * @param num The number of nodes to create.
     */
    void addelements(int num)
    {
        size_t i = v.size();
        for (v.resize(v.size() + num); i < v.size(); i++)
            v[i] = -1;
    }

    /**
     * This function return the representative and
     * do path-compression.
     *
     * @param elem The elements for which to be found the root
     * @return The index of the root of the up-tree in which
     * the parameter element resides.
     */
    int find(int elem)
    {
        if (v[elem] < 0)
            return elem;
        return (v[elem] = find(v[elem]));
    }
    /**
     * union-by-size
     *
     * @param a index of the first element to union
     * @param b index of the second element to union
     */
    void setunion(int a, int b)
    {
        a = find(a);
        b = find(b);

        if (a == b)
            return;

        int newSize = v[a] + v[b];

        if (v[a] <= v[b])
        {
            v[b] = a;
            v[a] = newSize;
        }
        else
        {
            v[a] = b;
            v[b] = newSize;
        }
    }
};

#endif
