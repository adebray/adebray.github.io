{- writeStatistics.hs

   Arun Debray, 22 June 2014

   This program reads the sleep data found in sleep_data.txt and generates statistics
   about them, which will be fed to the plotter and/or used directly by the final
   document.

   Ideas: maximum and minimum sleep time, and the date in question...
 -}

module Main where

import SleepTime
import System.IO

-- should factor elsewhere. (TODO)
-- is there a smarter way to write this...?
hourOf :: Time -> Int
hourOf t = case (hour t) of
	Hour h -> h

minuteOf :: Time -> Int
minuteOf t = case (minute t) of
	Minute m -> m

-- convert (hour, minute) -> number of hours, as a float
timeAsDouble :: Time -> Double
timeAsDouble t = (fromIntegral $ hourOf t) + ((fromIntegral $ minuteOf t) / 60)

-- calculates sleep time.
-- currently naively |b-a|. Perhaps this isn't ideal...
timeDifference :: Double -> Double -> Double
timeDifference awake asleep
	-- need to deal with 23 vs. 02 skewing data
	| asleep > 12 = 24 + awake - asleep
	| otherwise	  = awake - asleep

-- since I generally don't nap at midnight, it's easier to have these separate functions
-- for napping.
napDifference :: Double -> Double -> Double
napDifference awake asleep = awake - asleep

napAsDouble :: Sleep -> Double
napAsDouble n = napDifference (timeAsDouble $ rise n) (timeAsDouble $ rest n)

-- convert Sleep type into its duration
sleepAsDouble :: Sleep -> Double
sleepAsDouble s = timeDifference (timeAsDouble $ rise s) (timeAsDouble $ rest s)

-- I ought to figure out how to round this or print it in rounded form.
asleepTime :: DailyRecord -> Double
asleepTime = sleepAsDouble . bed

-- guess this is a Daily Double!
asleepTimeWithNaps :: DailyRecord -> Double
asleepTimeWithNaps rec = sleepAsDouble (bed rec) + (sum $ map napAsDouble $ naps rec)

-- here's hoping this works on Doubles. Whoops
mean :: (Fractional a) => [a] -> a
mean xs = (sum xs) / (fromIntegral $ length xs)

stdDev :: (Floating a) => [a] -> a
stdDev xs = sqrt $ mean [(x - m) * (x - m) | x <- xs]
	where m = mean xs

overallAverage :: [DailyRecord] -> Double
overallAverage = mean . (map asleepTimeWithNaps)

-- calculates the total average and trims to two decimal places.
overallNoNaps :: [DailyRecord] -> Double
overallNoNaps = mean . (map asleepTime)

overallStdDev :: [DailyRecord] -> Double
overallStdDev = stdDev . (map asleepTimeWithNaps)

stdDevNoNaps :: [DailyRecord] -> Double
stdDevNoNaps = stdDev . (map asleepTime)

totalHours :: [DailyRecord] -> Double
totalHours = sum . (map asleepTimeWithNaps)

recent :: Int -> [DailyRecord] -> Double
recent n = overallAverage . (take n) . reverse

recentNoNaps :: Int -> [DailyRecord] -> Double
recentNoNaps n = overallNoNaps . (take n) . reverse

recentSD :: Int -> [DailyRecord] -> Double
recentSD n = overallStdDev . (take n) . reverse

recentSDNoNaps :: Int -> [DailyRecord] -> Double
recentSDNoNaps n = stdDevNoNaps . (take n) . reverse

-- checks if the given time was between the two others.
-- I'll need to fix this if I ever sleep past noon... or get up before
-- midnight. It could happen.
timeBetween :: Double -> Sleep -> Bool
timeBetween t s
	| restTime > 12 && t > 12  = restTime <= t
	| restTime > 12 && t <= 12 = t < riseTime
	| otherwise				   = restTime <= t && t < riseTime
    where restTime = timeAsDouble $ rest s
          riseTime = timeAsDouble $ rise s

-- since naps don't fall across midnight, this should be separated out.
-- I hope to make this cleaner someday, but for now this is what it shall be.
timeBetweenForNaps :: Double -> Sleep -> Bool
timeBetweenForNaps t s = (timeAsDouble $ rest s) <= t && t < (timeAsDouble $ rise s)

-- on a given night, was I asleep at the given time?
isAsleep :: Double -> DailyRecord -> Bool
isAsleep t rec = (timeBetween t $ bed rec) || any (timeBetweenForNaps t) (naps rec)

-- returns P(awake at time t), given records and time t
atTime :: Double -> [DailyRecord] -> Double
atTime t rec = (fromIntegral total) / (fromIntegral $ length rec)
	where total = length $ filter (isAsleep t) rec

-- produces list of moving quantities from a list of data
-- arguments: function to apply, window size, list
windowedStat :: ([a] -> a) -> Int -> [a] -> [a]
-- we need to build the windows
windowedStat f n xs = [f (window i) | i <- [1..length xs]]
	where window i = take n $ drop (i - 1 - n `div` 2) xs

-- calculates the moving averge. Arguments: window size, list
-- by a quick call to windowedStat
-- note that you can't pass in records to these functions, just numbers!
windowedMean :: (Fractional a) => Int -> [a] -> [a]
windowedMean = windowedStat mean

-- in the same vein, this calculates the moving standard deviation.
windowedStdDev :: (Floating a) => Int -> [a] -> [a]
windowedStdDev = windowedStat stdDev

-- Given a filename, writes to 'statistics/filename.txt'
-- In order to make things Python-readable, I don't want to write lists this way.
writeStatistic :: (Num a, Show a) => String -> a -> IO ()
writeStatistic filename stat = do
	let path = "statistics/" ++ filename ++ ".txt"
	writeFile path $ show stat

-- recenter going-to-sleep time at midnight (so 23.9 is just before 0.0)
centerFix :: Double -> Double
centerFix val
	| val <= 12 = val
	| otherwise = val - 24

-- processes awake and asleep times for a single record.
putSingleTime :: Handle -> DailyRecord -> IO ()
putSingleTime h record = do
	let toSleep = timeAsDouble $ rest $ bed record
	    wakeUp  = timeAsDouble $ rise $ bed record
	hPutStrLn h ((show $ centerFix toSleep) ++ "\t" ++ show wakeUp)

putSingleProb :: Handle -> [DailyRecord] -> Double -> IO ()
putSingleProb h records t = hPutStrLn h $ show $ atTime t records

-- puts raw awake/asleep data into raw form for Python to plot.
-- I think I should factor this out, which will require moving
-- some other functions into SleepTime.hs.
-- also, assumes that the file is ordered, which is true but not enforced anywhere...
putTimes :: FilePath -> [DailyRecord] -> IO ()
putTimes filename records = withFile filename WriteMode $ \h -> mapM_ (putSingleTime h) records

-- these should be refactored and/or prettified.
-- that is, I should kill putSingleTime/Prob and just map strings to lines of a file. That makes life simplest.
putProbs :: FilePath -> [DailyRecord] -> IO ()
putProbs filename records = withFile filename WriteMode $ \h -> mapM_ (putSingleProb h records) [x/10.0 | x <- [0..239]]

-- yeah, I want to refactor. Blah.
-- and then I want to include naps!
-- so many moving averages... this is weekly for now
putMovingAvgs :: FilePath -> [DailyRecord] -> IO ()
putMovingAvgs filename records = withFile filename WriteMode $ \h -> mapM_ (\x -> hPutStrLn h (show x)) $ windowedMean 7 $ map asleepTime records

main :: IO ()
main = do
	records <- readDataFile "sleep_data.txt"
	writeStatistic "overallAverage" $ overallAverage records
	writeStatistic "overallNoNaps" $ overallNoNaps records
	writeStatistic "numDays" $ length records
	writeStatistic "totalHours" $ totalHours records
	writeStatistic "lastWeek" $ recent 7 records
	writeStatistic "weekNoNaps" $ recentNoNaps 7 records
	writeStatistic "lastMonth" $ recent 30 records
	writeStatistic "monthNoNaps" $ recentNoNaps 30 records
	writeStatistic "overallStdDev" $ overallStdDev records
	writeStatistic "stdDevNoNaps" $ stdDevNoNaps records
	writeStatistic "weekSD" $ recentSD 7 records
	writeStatistic "weekSDNoNaps" $ recentSDNoNaps 7 records
	writeStatistic "monthSD" $ recentSD 30 records
	writeStatistic "monthSDNoNaps" $ recentSD 30 records
	putTimes "raw_times.txt" records
	putProbs "raw_probs.txt" records
	putMovingAvgs "weekly_moving_avgs.txt" records
