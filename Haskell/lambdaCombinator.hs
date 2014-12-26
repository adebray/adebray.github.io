-- The λ Combinator, or "Is Haskell on the front page of Y Combinator?"
-- Arun Debray, September 5, 2013

import Data.List
import System.Process

second :: (a, b, c) -> b
second (_, x, _) = x

-- This is basically wget, but without any sort of error reporting.
downloadURL :: String -> IO String
downloadURL url = do
	results <- readProcessWithExitCode "curl" ["https://news.ycombinator.com/"] ""
	return $ second results

-- Tried to cover some common indicators that a post mentions Haskell. If you can
-- think of any others, let me know!
isHaskellOnTheFrontPage :: String -> Bool
isHaskellOnTheFrontPage webpage = any (\x -> isInfixOf x webpage) ["GHC", "ghc", "ghci", "GHCi", "Haskell", "haskell"]

prefix = "<html>\n<head>\n<title>Is Haskell on the front page of Y Combinator?</title>\n<link rel=\"shortcut icon\" href=\"../sun.ico\" />\n</head>\n<body>\n<div align=right style=\"font-family: sans-serif; font-size: 10pt;\"><a href='lambdaCombinator.hs'>Source</a></div>\n<center style=\"margin-top: 200px;\">\n<h1 style=\"font-family: sans-serif; font-size: 9em;\">"
suffix = "</h1>\n</center>\n</body>\n</html>"

report :: Bool -> String
report True = prefix ++ "YES" ++ suffix
report False = prefix ++ "NOPE" ++ suffix

main = do
	source <- downloadURL "https://news.ycombinator.com/"
	putStrLn $ report $ isHaskellOnTheFrontPage source
