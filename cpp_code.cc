#include <vector>
#define LEN 32
using namespace std;

class minMaxTree
{
    public:
        int heuristic;
        vector<vector<int> > moves;
        vector<minMaxTree*> children;
        
        minMaxTree(vector<vector<int> >);
};

minMaxTree::minMaxTree(vector<vector<int> > mov)
{
    moves = mov;
    heuristic = 0;
}



vector<vector<int> > possibleMoves(int* board)
{
    vector<vector<int> > moves;
    for(int i = 0; i < LEN; i++)
    {
        if(board[i] > 0)
        {
            int offset = (i/4) % 2;
            if(board[i + 4 - offset] == 0)
            {
                vector<int> move;
                move.push_back(i);
                move.push_back(i+4);
                moves.push_back(move);
            }
            else if(board[i + 4 - offset] == 0)
            {
                vector<int> move;
                move.push_back(i);
                move.push_back(i+4);
                moves.push_back(move);
            }
        }
    }
}





/*
 * This function is called by the Python front end
 * Using ctypes
 * Pass in an array of ints that represent the board
 */
extern "C" int* callAI(int* board)
{
    
    return board;
}