import Control.Monad (liftM)

main :: IO ()
main = do
    lines <- readToList (return [])
    let processedLines = let mid = (length lines) `div` 2 in (drop mid lines) ++ (take mid lines)
    putStr (unlines processedLines)


readToList :: IO [String] -> IO [String]
readToList acc = do
    line <- getLine
    list <- acc
    if line == "EOF" then acc else readToList (return (list ++ [line]))