{-	enter_data.hs
	Arun Debray, June 2014
	
	Command-line utility for entering sleep data into a file for later statstical analysis.
	Usage:
		./enter_data [-f filename]
	Specify the file to place the data into; otherwise, uses the default, sleep_data.txt.
 -}

module Main where

import System.Environment (getArgs)
import System.IO (hFlush, stdout)

import SleepTime -- module for handling dates/times specified to this app

{- two small utilities for I/O.
   Might wrap them in their own module if they're useful for other programs.
 -}
putStr' :: String -> IO ()
putStr' s = do
	putStr s
	hFlush stdout

promptLine :: String -> IO String
promptLine prompt = do
	putStr' prompt
	getLine

-- actually writes to the file.
recordToFile :: FilePath -> DailyRecord -> IO ()
recordToFile filename record = appendFile filename $ (show record) ++ "\n"

queryDay :: IO Date
queryDay = do
	putStrLn "What date are you entering data for?"
	-- might be able to make this fancier
	dayStr <- promptLine "Day: "
	monthStr <- promptLine "Month: "
	yearStr <- promptLine "Year: "
	return $ Date {
		day	  = Day (read dayStr :: Int),
		month = Month (read monthStr :: Int),
		year  = Year (read yearStr :: Int)
	}

{- One nice and easy fix would be for this to recognize strings of the form
   hh:mm and do something about that. Would make the program considerably
   cleaner.

   Also, until further notice, please specify all times in 24h.
 -}
queryTime :: String -> IO Time
queryTime kind = do
	putStrLn $ "When did you " ++ kind ++ "?"
	hourStr <- promptLine "Hour: "
	minuteStr <- promptLine "Minute: "
	return $ Time {
		minute = Minute (read minuteStr :: Int),
		hour   = Hour (read hourStr	:: Int)
	}

-- for convenience
napMessage :: [Nap] -> String
napMessage partialList
	| null partialList	= "Did you take a nap (yes/no)? "
	| otherwise			= "Did you take another nap (yes/no)? "

getYesNo :: IO Bool
getYesNo = do
	userInput <- getLine
	case userInput of
		"yes" -> return True
		"Yes" -> return True
		"no"  -> return False
		"No"  -> return False
		_	  -> do
			putStr' "Please answer 'yes' or 'no' > "
			getYesNo

-- loops to ask for naps from the user.
queryNaps :: [Nap] -> IO [Nap]
queryNaps partialList = do
	putStr' $ napMessage partialList

	nextAnswer <- getYesNo
	if nextAnswer
	then do
		start <- queryTime "sleep"
		finish <- queryTime "awake"
		let nextNap = Sleep {
			rest = start,
			rise = finish
		}
		return $ nextNap : partialList
	else return partialList

-- interactive loop
talkToUser :: IO DailyRecord
talkToUser = do
	date <- queryDay
	asleep <- queryTime "sleep"
	up <- queryTime "awake"
	napList <- queryNaps []
	return $ DailyRecord {
		today = date,
		bed = Sleep { rest = asleep, rise = up },
		naps = napList
	}

-- chooses the filename based on whether one was specified.
-- note: there is no error checking here...
getFilename :: [String] -> FilePath
getFilename args
	| length args < 2 = "sleep_data.txt"
	| otherwise		  = args !! 1

main :: IO ()
main = do
	args <- getArgs
	record <- talkToUser
	recordToFile (getFilename args) record
