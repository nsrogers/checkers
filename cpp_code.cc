#include <list>
#include <iostream>
#include <cstring>
#define LEN 32
using namespace std;

class minMaxTree
{
    public:
        int heuristic;
        list<int> move;
        list<minMaxTree*> children;
        
        minMaxTree(list<int>);
};

minMaxTree::minMaxTree(list<int> mov1)
{
    move = mov1;
    heuristic = 0;
}



int* applyMove(int* board, list<int> move)
{
    int* temp = static_cast<int*>(malloc(sizeof(int) * LEN));
    memcpy(temp, board, sizeof(int)*LEN);
    auto piece = move.begin();
    for(auto j = ++move.begin(); j != move.end(); j++ )
    {
        temp[*j] = temp[*piece];
        temp[*piece] = 0;

        int offset = ((*j)/4) % 2;
        if((*j) - (*piece) == 9)
            temp[(*j) - 4 - offset] = 0;
        else if((*j) - (*piece) == 7)
            temp[(*j) - 3 - offset] = 0;
        else if((*piece) - (*j) == 9)
            temp[(*piece) - 4 - offset] = 0;
        else if((*piece) - (*j) == 7)
            temp[(*piece) - 3 - offset] = 0;
        
        piece = j;
    }
    return temp;
}

list<list<int> > getAllJumps(int* board, int piece);

list<list<int> > jumpHelper(int* board, int piece, int offset)
{
    list<int> move;
    move.push_back(piece);
    move.push_back(piece+offset);
    list<list<int> > temp = getAllJumps(applyMove(board, move),piece+offset);
    for(auto i = temp.begin(); i != temp.end(); ++i){
        (*i).push_front(piece);
    }
    temp.push_back(move);
    return temp;
}


list<list<int> > getAllJumps(int* board, int piece){
    list<list<int> > moves;
    int offset = (piece/4) % 2;
    if(piece < 24)
    {
        if(board[piece + 7] == 0 && board[piece + 4 - offset] < 0 && piece % 4 != 0){
            list<list<int> > temp = jumpHelper(board, piece, 7);
            moves.insert(moves.end(), temp.begin(), temp.end());
        }
        if(board[piece + 9] == 0 && board[piece + 5 - offset] < 0 && piece % 4 != 3){
            list<list<int> > temp = jumpHelper(board, piece, 9);
            moves.insert(moves.end(), temp.begin(), temp.end());
        }
    }
    if(board[piece] == 2 && piece > 7){
        if(board[piece - 7] == 0 && board[piece -3 - offset] < 0 && piece % 4 != 3){
            list<list<int> > temp = jumpHelper(board, piece, -7);
            moves.insert(moves.end(), temp.begin(), temp.end());
        }
        if(board[piece - 9] == 0 && board[piece -4 - offset] < 0 && piece % 4 != 0){
            list<list<int> > temp = jumpHelper(board, piece, -9);
            moves.insert(moves.end(), temp.begin(), temp.end());
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
            if(i < 28)
            {
                if(board[i + 4 - offset] == 0 && i % 8 != 4)
                {
                    list<int> move;
                    move.push_back(i);
                    move.push_back(i+4-offset);
                    moves.push_back(move);
                }
                if(board[i + 5 - offset] == 0 && i % 8 != 3)
                {
                    list<int> move;
                    move.push_back(i);
                    move.push_back(i+5-offset);
                    moves.push_back(move);
                }
            }
            if (board[i] == 2 && i > 3){
                if(board[i - 4 - offset] == 0 && i % 8 != 4)
                {
                    list<int> move;
                    move.push_back(i);
                    move.push_back(i-4-offset);
                    moves.push_back(move);
                }
                if(board[i - 3 - offset] == 0 && i % 8 != 3)
                {
                   list<int> move;
                   move.push_back(i);
                   move.push_back(i-3-offset);
                   moves.push_back(move);
                }

            }
            list<list<int> > jumps = getAllJumps(board, i);
            moves.insert(moves.end(), jumps.begin(), jumps.end());
        }
    }
    return moves;
}

void swap(int* a, int i, int j)
{
    int t = a[i];
    a[i] = a[j];
    a[j] = t;
}

int* flip(int* board)
{
    for(int i = 0; i < (LEN-1)/2; i++)
    {
        swap(board, i, LEN - 1 - i);
    }
    for(int i = 0; i < LEN; i++)
    {
        board[i] = -board[i];
    }
    return board;
}

int heuristic(int* board)
{
    int h = 0;
    for(int i = 0; i < LEN; i++)
    {
        h -= board[i];
    }
    return h;
}

minMaxTree* build(int* board, int depth, minMaxTree* node)
{
    if(depth == 0)
    {
        node->heuristic = heuristic(board);
        return node;
    }
    list<list<int> > temp = possibleMoves(board);
    for(auto move = temp.begin(); move != temp.end(); move++)
    {
        int* tempBoard = flip(applyMove(board, *move));
        node->children.push_back(build(tempBoard, depth - 1,
            new minMaxTree(*move)));
    }
    return node;
}

void printListOfListOfInts(list<list<int> > moves)
{
    for(auto i = moves.begin(); i != moves.end(); i++)
    {
        cout << "[";
        for(auto j = (*i).begin(); j != (*i).end(); j++)
        {
            cout << (*j) << " ";
        }
        cout << "]" << endl;
    }
}

int minmax(bool turn, minMaxTree* node)
{
    if(node->children.empty())
    {
        return node->heuristic;
    }
    
    int val = ((turn) ? -25 : 25);
    for(auto i = node->children.begin(); i != node->children.end(); i++)
    {
        if(!turn)
        {
            if((*i)->heuristic < val)
            {
                val = minmax(true ,*i);
            }
        }
        else
        {
            if((*i)->heuristic > val)
            {
                val = minmax(false ,*i);
            }
        }
    }
    return val;
}


list<int> minmaxCaller(minMaxTree* root)
{
    minMaxTree* max = *(root->children.begin());
    for(auto i = root->children.begin(); i != root->children.end(); i++)
    {
        int val = minmax(false ,*i);
        if(val > max->heuristic)
        {
            max = *i;
        }
    }
    return max->move;
}

void printTree(minMaxTree* node, int depth)
{
    for(int i = 0; i < depth; i++)
        cout << "   ";
    cout << "[";
    for(auto j = node->move.begin(); j != node->move.end(); j++)
        cout << *j << " ";
    cout << "]\n";
    for(auto k = node->children.begin(); k != node->children.end(); k++)
        printTree(*k, depth+1);
    
}

/*
 * This function is called by the Python front end
 * Using ctypes
 * Pass in an array of ints that represent the board
 */
extern "C" int* callAI(int* board, int* retMove)
{    
    //printListOfListOfInts(possibleMoves(board));
    minMaxTree* root = new minMaxTree(list<int>());
    root = build(board, 3, root);
    //printTree(root,0);
    list<int> aiMove = minmaxCaller(root);
    cout << "HELP" << endl;
    int j = 0;
    for(auto i = aiMove.begin(); i != aiMove.end(); i++, j++)
    {
        retMove[j] = *i;
    }
    return retMove;
}
