module HsklAI where
    
import Data.Char

type Move = [Int]

data MinMaxTree = Node Int Move [MinMaxTree]

instance Show MinMaxTree where
    show (Node _ m []) = show m
    show (Node _ m (xs)) = (show xs) ++ (show m)

heuristic :: [Int] -> Int
heuristic board = foldl (-) 0 board

flipB :: [Int] -> [Int]
flipB b = map (*(-1)) $ reverse b

build :: [Int] -> Int -> Move -> MinMaxTree
build board 0 mov = Node (heuristic board) mov []
build board depth mov = if (null) children then (Node (if depth `mod` 2 == 1 then (-25) else 25) mov children) else (Node 0 mov children)
    where children = map (\x -> build (flipB (applyMove board x)) (depth-1) x) $ possibleMoves board

getMove :: MinMaxTree -> Move
getMove (Node _ mov _) = mov

minmax :: Bool -> MinMaxTree -> Int
minmax _ (Node h _ []) = h
minmax True (Node h _ children) = maximum (map (minmax False) children) 
minmax False (Node h _ children) = minimum (map (minmax True) children) 

minmaxCall :: Int -> Move -> [MinMaxTree] -> Move
--minMaxCall :: [MinMaxTree] -> Move
--minmaxCall children = (maximum (map (minMax True) children))
minmaxCall _ mov [] = mov
minmaxCall h mov (node@(Node _ m1 _):nodes) = if tempH > h then minmaxCall tempH m1 nodes
                                            else minmaxCall h mov nodes
                                            where tempH = minmax True node

getChildren :: MinMaxTree -> [MinMaxTree]
getChildren (Node _ _ children) = children

callAI :: [Int] -> [Int]
callAI xs = minmaxCall (-9001) [] (getChildren (build xs 5 []))

possibleMoves :: [Int] -> [Move]
possibleMoves board = filter (not . null) $ (foldl (++) [] (map (getPossibleMove board)  [0..31])) ++ (foldl (++) [] (map (getAllJumps board) [0..31]))


getPossibleMove :: [Int] -> Int -> [Move]
getPossibleMove board index 
            | board!!index > 0 = [downL, downR, upL, upR]
            | otherwise = []
                where downL = if index < 28 && index `mod` 8 /= 4 && board!!(index + 4 - offset) == 0 then
                             index:[(index + 4 - offset)] else []
                      downR = if index < 28 && index `mod` 8 /= 3 && board!!(index + 5 - offset) == 0 then
                              index:[(index + 5 - offset)] else []
                      upL = if board!!index == 2 && index > 3 && index `mod` 8 /= 4 && board!!(index - 4 - offset) == 0 then
                              index:[(index - 4 - offset)] else []
                      upR = if board!!index == 2 && index > 3 && index `mod` 8 /= 3 && board!!(index - 3 - offset) == 0 then
                              index:[(index - 3 - offset)] else []
                      offset = ((index `div` 4) `mod` 2)

-- http://stackoverflow.com/questions/5852722/replace-individual-list-elements-in-haskell
replaceNth n newVal (x:xs)
     | n == 0 = newVal:xs
     | otherwise = x:replaceNth (n-1) newVal xs           
           
applyMove :: [Int] -> Move -> [Int]
applyMove board [] = board
applyMove board (m1:[]) = board
applyMove board (m1:m2:moves)
            | (m2 - m1) == 9 = applyMove (replaceNth (m2 - 4 - offset) 0 newBoard) (m2:moves)
            | (m2 - m1) == 7 = applyMove (replaceNth (m2 - 3 - offset) 0 newBoard) (m2:moves)
            | (m2 - m1) == (-9) = applyMove (replaceNth (m1 - 4 - offset) 0 newBoard) (m2:moves)
            | (m2 - m1) == (-7) = applyMove (replaceNth (m1 - 3 - offset) 0 newBoard) (m2:moves)
            | otherwise = newBoard
                where newBoard = (replaceNth m1 0 (replaceNth m2 (if m2 > 27 then 2 else (board!!m1)) board))
                      offset = ((m2 `div` 4) `mod` 2)
                  
jumperHelper :: [Int] -> Int -> Int -> [Move]
jumperHelper board index offset = [index, index+offset] : (map (index:) $ getAllJumps (applyMove board [index, index+offset]) (index+offset))
                      
getAllJumps :: [Int] -> Int -> [Move]
getAllJumps board index
        | board!!index > 0 = downL ++ downR ++ upL ++ upR
        | otherwise = [] 
            where downL = if index `mod` 4 /= 0 && index < 24 && board!!(index + 7) == 0 && board!!(index + 4 - offset) < 0 then
                             (jumperHelper board index 7) else []
                  downR = if index `mod` 4 /= 3 && index < 24 && board!!(index + 9) == 0 &&  board!!(index + 5 - offset) < 0 then
                             (jumperHelper board index 9) else []
                  upL = if index `mod` 4 /= 0 && index > 7 && board!!index == 2 && board!!(index - 9) == 0 && board!!(index - 4 - offset) < 0 then
                             (jumperHelper board index (-9)) else []
                  upR = if index `mod` 4 /= 3 && index > 7 && board!!index == 2 && board!!(index - 7) == 0 && board!!(index - 3 - offset) < 0 then
                             (jumperHelper board index (-7)) else []
                  offset = ((index `div` 4) `mod` 2)