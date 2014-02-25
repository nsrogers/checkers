module HsklAI where
    
import Data.Char

callAI :: [Int] -> [Int]
callAI xs = (possibleMoves xs)!!0

getPossibleMove :: [Int] -> Int -> [[Int]]
getPossibleMove board index = do offset <- [(index `div` 4) `mod` 2]
                                 downL <- if board!!(index + 4 - offset) == 0 then
                                             [index + 4 - offset] else []
                                 return [downL]

possibleMoves :: [Int] -> [[Int]]
possibleMoves board = foldl (++) [] (map (getPossibleMove board)  [0..31])
