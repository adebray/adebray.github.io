{-# LANGUAGE GeneralizedNewtypeDeriving #-} -- I like deriving Num

{- sleepTime.hs
   Arun Debray, June 29, 2014

   Common definitions for my sleep-data trackers, mostly data types.
 -}

module SleepTime (
	Minute (Minute),
	Hour (Hour),
	Day (Day), -- a day is a number; a date is a DDMMYY combination
	Month (Month),
	Year (Year),
	Date (Date), day, month, year,
	Time (Time), hour, minute,
	Sleep (Sleep), rise, rest,
	Nap,
	DailyRecord (DailyRecord), today, bed, naps,
	readDataFile
) where

newtype Minute = Minute Int deriving (Read, Show, Ord, Eq, Num)
newtype Hour   = Hour Int deriving (Read, Show, Ord, Eq, Num)
newtype Day	   = Day Int deriving (Read, Show, Ord, Eq, Num)
newtype Month  = Month Int deriving (Read, Show, Ord, Eq, Num)
newtype Year   = Year Int deriving (Read, Show, Ord, Eq, Num)

data Date = Date {
	day	  :: Day,
	month :: Month,
	year  :: Year
} deriving (Read, Show, Eq)

-- time instance. Doesn't need to be more exact than this
data Time = Time {
	hour   :: Hour,
	minute :: Minute
} deriving (Read, Show, Eq)

instance Ord Date where
	d1 <= d2
		| year d1  < year d2  = True
		| month d1 < month d2 = True
		| day d1   <= day d2  = True
		| otherwise			  = False

instance Ord Time where
	t1 <= t2
		| hour t1	< hour t2	 = True
		| minute t1 <= minute t2 = True
		| otherwise				 = False

data Sleep = Sleep { rise, rest :: Time } deriving (Read, Show)
type Nap = Sleep

data DailyRecord = DailyRecord {
	today :: Date,
	bed   :: Sleep,
	naps  :: [Nap]
} deriving (Read, Show)

-- Takes in the data file and produces everything it contains.
readDataFile :: FilePath -> IO [DailyRecord]
readDataFile filename = do
	-- will want to error handle
	contents <- readFile filename
	return $ map (\s -> (read s :: DailyRecord)) $ lines contents
