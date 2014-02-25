module HsklAI where
    
import Data.Char

callAI :: [Int] -> [Int]
callAI xs = (filter (not . null) (possibleMoves xs)) !! 0

possibleMoves :: [Int] -> [[Int]]
possibleMoves board = (foldl (++) [] (map (getPossibleMove board)  [0..31])) ++ (foldl (++) [] (map (getAllJumps board) [0..31]))


getPossibleMove :: [Int] -> Int -> [[Int]]
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
           
applyMove :: [Int] -> [Int] -> [Int]
applyMove board [] = board
applyMove board (m1:[]) = board
applyMove board (m1:m2:moves)
            | (m2 - m1) == 9 = applyMove (replaceNth (m2 - 4 - offset) 0 newBoard) (m2:moves)
            | (m2 - m1) == 7 = applyMove (replaceNth (m2 - 3 - offset) 0 newBoard) (m2:moves)
            | (m1 - m2) == 9 = applyMove (replaceNth (m1 - 4 - offset) 0 newBoard) (m2:moves)
            | (m1 - m2) == 7 = applyMove (replaceNth (m1 - 3 - offset) 0 newBoard) (m2:moves)
            | otherwise = board
                where newBoard = (replaceNth m1 0 (replaceNth m2 (board!!m1) board))
                      offset = ((m2 `div` 4) `mod` 2)
                  
jumperHelper :: [Int] -> Int -> Int -> [[Int]]
jumperHelper board index offset = [index, index+offset] : (map (index:) $ getAllJumps (applyMove board [index, index+offset]) (index+offset))
                      
getAllJumps :: [Int] -> Int -> [[Int]]
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