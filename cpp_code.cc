#include <list>
#include <list>
#define LEN 32
using namespace std;

class minMaxTree
{
    public:
        int heuristic;
        list<list<int> > moves;
        list<minMaxTree*> children;
        
        minMaxTree(list<list<int> >);
};

minMaxTree::minMaxTree(list<list<int> > mov)
{
    moves = mov;
    heuristic = 0;
}

list<list<int> > getAllJumps(int* board, int piece, list<int> move){
    list<list<int> > moves;
    int offset = (piece/4) % 2
    if(board[piece + 7] == 0 && board[piece + 4 - offset] < 0){
        move.push_back(piece);
        move.push_back(piece+7);
        moves.push_back(move);
        list<list<int> > temp = getAllJumps(applyMove(board),piece+7);
        for(type::iterator i = temp.begin(); i != temp.end(); ++i){
            moves.push_back(*i.push_front(piece));
        }
    }
    if(board[piece + 9] == 0 && board[piece + 5 - offset] < 0){
        move.push_back(piece);
        move.push_back(piece+9);
        moves.push_back(move);
        list<list<int> > temp = getAllJumps(applyMove(board),piece+9);
        for(type::iterator i = temp.begin(); i != temp.end(); ++i){
            moves.push_back(*i.push_front(piece));
        }
    }
    if(board[piece] == 2){
        if(board[piece - 7] == 0 && board[piece -3 - offset] < 0){
            move.push_back(piece);
            move.push_back(piece-7);
            moves.push_back(move);
            list<list<int> > temp = getAllJumps(applyMove(board),piece-7);
            for(type::iterator i = temp.begin(); i != temp.end(); ++i){
                moves.push_back(*i.push_front(piece));
            }
        }
        if(board[piece - 9] == 0 && board[piece -4 - offset] < 0){
            move.push_back(piece);
            move.push_back(piece-9);
            moves.push_back(move);
            list<list<int> > temp = getAllJumps(applyMove(board),piece-9);
            for(type::iterator i = temp.begin(); i != temp.end(); ++i){
                moves.push_back(*i.push_front(piece));
            }
        }
    }
    return moves;
}

list<list<int> > possibleMoves(int* board)
{
    list<list<int> > moves;
    for(int i = 0; i < LEN; i++)
    {
        if(board[i] > 0)
        {
            int offset = (i/4) % 2;
            if(board[i + 4 - offset] == 0)
            {
                list<int> move;
                move.push_back(i);
                move.push_back(i+4-offset);
                moves.push_back(move);
            }
            if(board[i + 5 - offset] == 0)
            {
                list<int> move;
                move.push_back(i);
                move.push_back(i+5-offset);
                moves.push_back(move);
            }
            if (board[i] == 2){
                if(board[i - 4 - offset] == 0)
                {
                    list<int> move;
                    move.push_back(i);
                    move.push_back(i-4-offset);
                    moves.push_back(move);
                }
                if(board[i - 3 - offset] == 0)
                {
                   list<int> move;
                   move.push_back(i);
                   move.push_back(i-3-offset);
                   moves.push_back(move);
                }

            }
            list<list<int> jumps = getAllJumps(board, i);
            moves.insert(moves.end(), jumps.begin(), jumps.end());
        }
    }
    return moves;
}





/*
 * This function is called by the Python front end
 * Using ctypes
 * Pass in an array of ints that represent the board
 */
extern "C" int* callAI(int* board)
{    
    cout << possibleMoves(board);
    return board;
}
