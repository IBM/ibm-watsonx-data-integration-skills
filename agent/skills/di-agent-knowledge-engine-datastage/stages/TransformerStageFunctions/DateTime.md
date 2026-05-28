# DataStage Date and Time Transformer Functions

Reference of builtin transfomer functions for manipulating date and time fields

### ConvertDatum

- **Description**: Convert date format
- **Usage**: `anystring ConvertDatum(anystring:string, anystring:string)`
- **Example**: If mylink.date contains the date string "01082022", then the following function returns the date string "20220801": ConvertDatum(mylink.date, "YYYY")

### ConvertTimeZone

- **Description**: Convert to different time zone
- **Usage**: `anystring ConvertTimeZone(int32:number, int32:number, int32:number, int32:number, int32:number, int32:number, anystring:string, anystring:string)`
- **Example**: If mylink.currentYear contains the integer 2021, then the following function returns a timestamp string that uses the new timezone, "2021-09-30 04:02:03". ConvertTimeZone(mylink.currentYear, 9, 30, 1, 2, 3, "PST", "EST")

### CurrentDate

- **Description**: Return the current date
- **Usage**: `date CurrentDate()`
- **Example**: Use this function to add a new column that contains the date to the data output by the Transformer stage. CurrentDate()

### CurrentTime

- **Description**: Return the current time
- **Usage**: `time CurrentTime(string)`
- **Example**: Use this function to add a new column that contains the time to the data output by the Transformer stage. You can add an optional parameter that has the datatype of time. CurrentTime(%time%)

### CurrentTimeMS

- **Description**: Return the current time including microseconds
- **Usage**: `time CurrentTimeMS()`
- **Example**: Use this function to add a new column that contains the time to the data output by the Transformer stage. You must set the Extended field in the column metadata to Microseconds to contain the full time. CurrentTimeMS()

### CurrentTimestamp

- **Description**: Return the current timestamp
- **Usage**: `timestamp CurrentTimestamp(string)`
- **Example**: Use this function to add a new column that contains the timestamp to the data output by the Transformer stage. You can add an optional parameter that has the datatype of timestamp. CurrentTimestamp(%timestamp%)

### CurrentTimestampMS

- **Description**: Return the current timestamp including microseconds
- **Usage**: `timestamp CurrentTimestampMS()`
- **Example**: Use this function to add a new column that contains the timestamp to the data output by the Transformer stage. You must set the Extended field in the column metadata to Microseconds to contain the full timestamp. CurrentTimestampMS()

### DateFromComponents

- **Description**: Returns a date object representing the specified year, month and day
- **Usage**: `date DateFromComponents(int32:years, int32:months, int32:days)`
- **Example**: If mylink.yearcol contains the value 2010, mylink.monthcol contains the value 12, and mylink.dayofmonthcol contains the value 2, then the two following functions are equivalent, and return the date 2010-12-02. DateFromComponents(2010, 12, 2) DateFromComponents(mylink.yearcol, mylink.monthcol, mylink.dayofmonthcol)

### DateFromDaysSince

- **Description**: Returns a date by adding an integer to a baseline date
- **Usage**: `date DateFromDaysSince(int32:number, string:"yyyy-mm-dd")`
- **Example**: If mylink.myintcol contains the integer 18250, and mylink.mydatecol contains the date 1958-08-18, then the three following functions are equivalent, and return the date 2008-08-05: DateFromDaysSince(18250, "1958-08-18") DateFromDaysSince(mylink.myintcol, "1958-08-18") DateFromDaysSince(mylink.myintcol, mylink.mydatecol) If mylink.mynegintcol contains the integer -1, and mylink.mydatecol contains the date 1958-08-18, then the following three functions are equivalent, and return the date 1958-08-17: DateFromDaysSince(-1, "1958-08-18") DateFromDaysSince(mylink.mynegintcol, "1958-08-18") DateFromDaysSince(mylink.mynegintcol, mylink.mydatecol)

### DateFromDaysSince2

- **Description**: Returns a date by adding an integer to a baseline date
- **Usage**: `date DateFromDaysSince2(int32:number, date)`
- **Example**: If mylink.myintcol contains the integer 18250, and mylink.mydatecol contains the date 1958-08-18, then the three following functions are equivalent, and return the date 2008-08-05: DateFromDaysSince2(18250, "1958-08-18") DateFromDaysSince2(mylink.myintcol, "1958-08-18") DateFromDaysSince2(mylink.myintcol, mylink.mydatecol) If mylink.mynegintcol contains the integer -1, and mylink.mydatecol contains the date 1958-08-18, then the following three functions are equivalent, and return the date 1958-08-17: DateFromDaysSince2(-1, "1958-08-18") DateFromDaysSince2(mylink.mynegintcol, "1958-08-18") DateFromDaysSince2(mylink.mynegintcol, mylink.mydatecol)

### DateFromJulianDay

- **Description**: Returns a date from the given julian date
- **Usage**: `date DateFromJulianDay(uint32:juliandate)`
- **Example**: If mylink.myjulcol contains the value 2454614, then the two following functions are equivalent, and return the date 2008-05-27. DateFromJulianDay(2454614) DateFromJulianDay(mylink.myjulcol)

### DateOffsetByComponents

- **Description**: Returns the given date, offset by the given components of years, months and days
- **Usage**: `date DateOffsetByComponents(date:basedate, int32:yearoffset, int32:monthoffset, int32:dayoffset)`
- **Example**: If mylink.basedate contains 2011-08-18 and mylink.yearos contains the value 2, mylink.monthos contains the value 0, and mylink.dayofmonthosol contains the value 0, then the two following functions are equivalent, and return the date 2013-08-18. DateOffsetByComponents("2011-08-18", 2, 0, 0) DateOffsetByComponents(mylink.basedate, mylink.yearos, mylink.monthos, mylink.dayofmonthos)

### DateOffsetByDays

- **Description**: Returns the given date, offset by the number of days specified
- **Usage**: `date DateOffsetByDays(date:basedate, int32:offset)`
- **Example**: If mylink.basedate contains 2011-08-18 and mylink.dayoffset contains the value 2, then the two following functions are equivalent, and return the date 2011-08-20. DateOffsetByDays("2011-08-18", 2) DateOffsetByDays(mylink.basedate, mylink.dayoffset)

### DaysInMonth

- **Description**: Returns the number of days in the month of the given date
- **Usage**: `int32 DaysInMonth(date)`
- **Example**: If mylink.mysourcedate contains the date 1958-08-18, then the two following functions are equivalent, and return the integer value 31. DaysInMonth(mylink.mysourcedate) DaysInMonth("1958-08-18")

### DaysInYear

- **Description**: Returns the number of days in the year of the given date
- **Usage**: `int32 DaysInYear(date)`
- **Example**: If mylink.mysourcedate contains the date 2012-08-18, then the two following functions are equivalent, and return the integer value 366. DaysInYear(mylink.mysourcedate) DaysInYear("2012-08-18") If mylink.mysourcedate contains the date 2011-08-18, then the two following functions are equivalent, and return the integer value 365. DaysInYear(mylink.mysourcedate) DaysInYear("2011-08-18")

### DaysSinceFromDate

- **Description**: Returns the number of days from source date to the given date
- **Usage**: `int32 DaysSinceFromDate(date, string:"yyyy-mm-dd")`
- **Example**: If mylink.mysourcedate contains the date 1958-08-18 and mylink.mygivendate contains the date 2008-08-18, then the two following functions are equivalent, and return the integer value 18263. DaysSinceFromDate(mylink.mygivendate, mylink.mysourcedate) DaysSinceFromDate("2008-08-18", "1958-08-18")

### DaysSinceFromDate2

- **Description**: Returns the number of days from source date to the given date
- **Usage**: `int32 DaysSinceFromDate2(date, date)`
- **Example**: If mylink.mysourcedate contains the date 1958-08-18 and mylink.mygivendate contains the date 2008-08-18, then the two following functions are equivalent, and return the integer value 18263. DaysSinceFromDate2(mylink.mygivendate, mylink.mysourcedate) DaysSinceFromDate2("2008-08-18", "1958-08-18")

### HoursFromTime

- **Description**: Return the hour portion of a time
- **Usage**: `int8 HoursFromTime(time)`
- **Example**: If mylink.mytime contains the time 22:30:00, then the following two functions are equivalent, and return the integer value 22. HoursFromTime(mylink.mytime) HoursFromTime("22:30:00")

### JulianDayFromDate

- **Description**: Returns julian day from the given date
- **Usage**: `int32 JulianDayFromDate(date)`
- **Example**: If mylink.mydate contains the date 2008-05-27, then the two following functions are equivalent, and return the value 2454614. JulianDayFromDate("2008-05-27") JulianDayFromDate(mylink.mydate)

### MicroSecondsFromTime

- **Description**: Returns the microsecond portion from a time
- **Usage**: `int32 MicroSecondsFromTime(time)`
- **Example**: If mylink.mytime contains the time 22:30:00.32, then the following function returns the value 320000: MicroSecondsFromTime(mylink.mytime)

### MidnightSecondsFromTime

- **Description**: Returns the number of seconds from midnight to the given time
- **Usage**: `dfloat MidnightSecondsFromTime(time)`
- **Example**: If mylink.mytime contains the time 00:30:52, then the two following functions are equivalent, and return the value 1852: MidnightSecondsFromTime("00:30:52") MidnightSecondsFromTime(mylink.mytime)

### MinutesFromTime

- **Description**: Returns the minute portion from a time
- **Usage**: `int8 MinutesFromTime(time)`
- **Example**: If mylink.mytime contains the time 22:30:52, then the two following functions are equivalent, and return the value 30: MinutesFromTime("22:30:52") MinutesFromTime(mylink.mytime)

### MonthDayFromDate

- **Description**: Returns the day of the month given the date
- **Usage**: `int8 MonthDayFromDate(date)`
- **Example**: If mylink.mydate contains the date 2008-08-18, then the two following functions are equivalent, and return the value 18: MonthDayFromDate("2008-08-18") MonthDayFromDate(mylink.mydate)

### MonthFromDate

- **Description**: Returns the month number given the date
- **Usage**: `int8 MonthFromDate(date)`
- **Example**: If mylink.mydate contains the date 2008-08-18, then the two following functions are equivalent, and return the value 8: MonthFromDate("2008-08-18") MonthDayDate(mylink.mydate)

### NextWeekdayFromDate

- **Description**: Returns the date of the specified day of the week soonest after the source date
- **Usage**: `date NextWeekdayFromDate(date:sourcedate, string:dayname)`
- **Example**: If mylink.mysourcedate contains the date 2008-08-18 and the day of the week that is specified is Thursday, then the two following functions are equivalent, and return the value 2008-08-21: NextWeekdayFromDate("2008-08-18", "Thursday") NextWeekdayFromDate(mylink.mysourcedate, "Thu")

### NthWeekdayFromDate

- **Description**: Return the date which lies on the specified weekday offset from the baseline date
- **Usage**: `date NthWeekdayFromDate(date:sourcedate, string:dayname, int32:offset)`
- **Example**: If mylink.mydate contains the date 2009-08-18 and Thursday is specified with an offset of 1, then the two following functions are equivalent, and return the value 2009-08-20: NthWeekdayFromDate("2009-08-18", "Thursday", 1) NthWeekdayFromDate(mylink.mydate, "Thu", 1) The first occurrence of Thursday is returned. In the proceeding example, the Thursday occurs in the same week as the date 2009-08-18. The date 2009-08-18 is a Tuesday.

### PreviousWeekdayFromDate

- **Description**: Returns the date of the specified day of the week most recent before the source date
- **Usage**: `date PreviousWeekdayFromDate(date:sourcedate, string:dayname)`
- **Example**: If mylink.mysourcedate contains the date 2008-08-18 and Thursday is specified, then the two following functions are equivalent, and return the value 2008-08-14: PreviousWeekdayFromDate("2008-08-18", "Thursday") PreviousWeekdayFromDate(mylink.mysourcedate, "Thu")

### SecondsFromTime

- **Description**: Returns the second portion from a time
- **Usage**: `dfloat SecondsFromTime(time)`
- **Example**: If mylink.mytime contains the time 22:30:52, then the two following functions are equivalent, and return the value 52: SecondsFromTime("22:30:52") SecondsFromTime(mylink.mytime)

### SecondsSinceFromTimestamp

- **Description**: Returns the number of seconds between two timestamps
- **Usage**: `dfloat SecondsSinceFromTimestamp(timestamp, string:"yyyy-mm-dd hh:nn:ss")`
- **Example**: If mylink.mytimestamp contains the timestamp 2008-08-18 22:30:52, and mylink.mytimestamp_base contains the timestamp 2008-08-19 22:30:52, then the two following functions are equivalent, and return the value -86400: SecondsSinceFromTimestamp("2008-08-18 22:30:52", "2008-08-19 22:30:52") SecondsSinceFromTimestamp(mylink.mytimestamp, mylink.mytimestamp_base)

### SecondsSinceFromTimestamp2

- **Description**: Returns the number of seconds between two timestamps
- **Usage**: `dfloat SecondsSinceFromTimestamp2(timestamp, timestamp)`
- **Example**: If mylink.mytimestamp contains the timestamp 2008-08-18 22:30:52, and mylink.mytimestamp_base contains the timestamp 2008-08-19 22:30:52, then the two following functions are equivalent, and return the value -86400: SecondsSinceFromTimestamp2("2008-08-18 22:30:52", "2008-08-19 22:30:52") SecondsSinceFromTimestamp2(mylink.mytimestamp, mylink.mytimestamp_base)

### TimeDate

- **Description**: Returns the time and date as a formatted string
- **Usage**: `anystring TimeDate()`
- **Example**: If the job was run at 4.21 pm on June 20th, 2008, then the following function returns the string "16:21:48 20 Jun 2008". TimeDate()

### TimeFromComponents

- **Description**: Returns a time object representing the specified hour, minutes, seconds and microseconds
- **Usage**: `time TimeFromComponents(int32:hours, int32:minutes, int32:seconds, int32:microseconds)`
- **Example**: If mylink.hourcol contains the value 10, mylink.mincol contains the value 12, mylink.seccol contains the value 2, and mylink.mseccol contains 0, then the two following functions are equivalent, and return the time 10:12:02.0: TimeFromComponents(10, 12, 2, 0) TimeFromComponents(mylink.hourcol, mylink.mincol, mylink.seccol, mylink.mseccol)

### TimeFromMidnightSeconds

- **Description**: Returns the time given the number of seconds since midnight
- **Usage**: `time TimeFromMidnightSeconds(dfloat:seconds)`
- **Example**: If mylink.mymidnightseconds contains the value 240, then the two following functions are equivalent, and return the value 00:04:00: TimeFromMidnightSeconds("240") TimeFromMidnightSeconds(mylink.mymidnightseconds)

### TimeOffsetByComponents

- **Description**: Returns the given time, offset by the given components of hours, minutes and seconds
- **Usage**: `time TimeOffsetByComponents(time:basetime, int32:houroffset, int32:minuteoffset, dfloat:secondoffset)`
- **Example**: If mylink.basetime contains 14:05:29 and mylink.houros contains the value 2, mylink.minos contains the value 0, mylink.secos contains the value 20, then the two following functions are equivalent, and return the time 16:05:49. TimeOffsetByComponents("14:05:29", 2, 0, 20) TimeOffsetByComponents(mylink.basetime, mylink.houros, mylink.minos, mylink.secos)

### TimeOffsetBySeconds

- **Description**: Returns the given time, offset by the number of seconds or part seconds specified
- **Usage**: `time TimeOffsetBySeconds(time:basetime, dfloat:offset)`
- **Example**: If mylink.basetime contains 14:05:29.30 and mylink.secos contains the value 2.5, then the two following functions are equivalent, and return the time 14:05:31.80. TimeOffsetBySeconds("14:05:29.30", 2.5) TimeOffsetBySeconds(mylink.basetime, mylink.secos)

### TimestampFromDate

- **Description**: Returns a timestamp from the given date
- **Usage**: `timestamp TimestampFromDate(date, string)`
- **Example**: If mylink.mydate contains the date 2022-11-28 and mylink.mytime contains the time 22:30:52, then the following function returns the time stamp 2022-11-28 22:30:52: TimestampFromDate(mylink.mydate,mylink.mytime)

### TimestampFromDateTime

- **Description**: Returns a timestamp from the given date and time
- **Usage**: `timestamp TimestampFromDateTime(date, time)`
- **Example**: If mylink.mydate contains the date 2008-08-18 and mylink.mytime contains the time 22:30:52, then the two following functions are equivalent, and return the timestamp 2008-08-18 22:30:52: TimestampFromDateTime("2008-08-18", "22:30:52") TimestampFromDateTime(mylink.mydate, mylink.mytime)

### TimestampFromSecondsSince

- **Description**: Return the timestamp from the number of seconds from the base timestamp
- **Usage**: `timestamp TimestampFromSecondsSince(dfloat:seconds, string:timestamp)`
- **Example**: If mylink.myseconds contains the value 2563 and mylink.timestamp_base contains the timestamp 2008-08-18 22:30:52, then the two following functions are equivalent, and return the timestamp 2008-08-18 23:13:35: TimestampFromSecondsSince("2563", "2008-08-18 22:30:52") TimestampFromSecondsSince(mylink.myseconds, mylink.timestamp_base)

### TimestampFromSecondsSince2

- **Description**: Return the timestamp from the number of seconds from the base timestamp
- **Usage**: `timestamp TimestampFromSecondsSince2(dfloat:seconds, timestamp)`
- **Example**: If mylink.myseconds contains the value 2563 and mylink.timestamp_base contains the timestamp 2008-08-18 22:30:52, then the two following functions are equivalent, and return the timestamp 2008-08-18 23:13:35: TimestampFromSecondsSince2("2563", "2008-08-18 22:30:52") TimestampFromSecondsSince2(mylink.myseconds, mylink.timestamp_base)

### TimestampFromTime

- **Description**: Returns a timestamp from the given time
- **Usage**: `timestamp TimestampFromTime(time, string)`
- **Example**: If mylink.time has a value of 19:37:57, and mylink.date has a value of 2022-11-29, then the following function returns a timestamp value of 2022-11-29 19:37:57: TimestampFromTime(mylink.time, mylink.date)

### TimestampFromTime2

- **Description**: Returns a timestamp with the date from the specified timestamp argument and the time from the specified time argument
- **Usage**: `timestamp TimestampFromTime2(time, timestamp)`
- **Example**: If mylink.mytime contains the time 12:03:22 and mylink.mytimestamp contains the timestamp 2008-08-18 22:30:52, then the two following functions are equivalent, and return the timestamp 2008-08-18 12:03:22: TimestampFromTime2("12:03:22", "2008-08-18 22:30:52") TimestampFromTime2(mylink.mytime, mylink.mytimestamp)

### TimestampFromTimet

- **Description**: Returns a timestamp from the given unix time_t value
- **Usage**: `timestamp TimestampFromTimet(int64:timetvalue)`
- **Example**: If mylink.mytimet contains the value 1234567890, then the two following functions are equivalent, and return the timestamp 2009-02-13 23:31:30: TimestampFromTimet("1234567890") TimestampFromTimet(mylink.mytimet)

### TimestampOffsetByComponents

- **Description**: Returns the given timestamp, offset by the given components of years, months, days, hours, minutes and seconds
- **Usage**: `timestamp TimestampOffsetByComponents(timestamp:basetimestamp, int32:yearoffset, int32:monthoffset, int32:dayoffset, int32:houroffset, int32:minuteoffset, dfloat:secondoffset)`
- **Example**: If mylink.basetimestamp contains 2009-08-18 14:05:29, mylink.yearos contains 0, mylink.monthos contains the value 2, mylink.dayos contains the value -4, mylink.houros contains the value 2, mylink.minos contains the value 0, and mylink.secos contains the value 20, then the two following functions are equivalent and return the time stamp 2009-10-14 16:05:49. TimestampOffsetByComponents("2009-08-18 14:05:29", 0, 2, -4, 2, 0, 20) TimestampOffsetByComponents(mylink.basetimestamp, mylink.year, mylink.month, mylink.day)

### TimestampOffsetBySeconds

- **Description**: Returns the given timestamp, offset by the number of seconds or part seconds specified
- **Usage**: `timestamp TimestampOffsetBySeconds(timestamp:basetimestamp, dfloat:offset)`
- **Example**: If mylink.basetimestamp contains 2009-08-18 14:05:29 and mylink.secos contains the value 32760, then the two following functions are equivalent, and return the timestamp 2009-08-18 23:11:29: TimestampOffsetBySeconds("2009-08-18 14:05:29", 32760) TimestampOffsetBySeconds(mylink.basetimestamp, mylink.secos)

### TimetFromTimestamp

- **Description**: Returns a unix time_t value from the given timestamp
- **Usage**: `int64 TimetFromTimestamp(timestamp)`
- **Example**: If mylink.mytimestamp contains the value 2009-02-13 23:31:30, then the two following functions are equivalent, and return the value 1234567890: TimetFromTimestamp("2009-02-13 23:31:30") TimetFromTimestamp(mylink.mytimestamp)

### WeekdayFromDate

- **Description**: Returns the day of the week from the given date
- **Usage**: `int8 WeekdayFromDate(date, string:startdayname)`
- **Example**: If mylink.mydate contains the date 2008-08-18, then the two following functions are equivalent, and return the value 1: WeekdayFromDate("2008-08-18") WeekdayFromDate(mylink.mydate) If mylink.mydate contains the date 2008-08-18, and mylink.origin_day contains saturday, then the two following functions are equivalent, and return the value 2: WeekdayFromDate("2008-08-18", "saturday") WeekdayFromDate(mylink.mydate, mylink.origin_day)

### YeardayFromDate

- **Description**: Returns the day number in the year from the given date
- **Usage**: `int16 YeardayFromDate(date)`
- **Example**: If mylink.mydate contains the date 2008-08-18, then the two following functions are equivalent, and return the value 231: YeardayFromDate("2008-08-18") YeardayFromDate(mylink.mydate)

### YearFromDate

- **Description**: Returns the year from the given date
- **Usage**: `int16 YearFromDate(date)`
- **Example**: If mylink.mydate contains the date 2008-08-18, then the two following functions are equivalent, and return the value 2008: YearFromDate("2008-08-18") YearFromDate(mylink.mydate)

### YearweekFromDate

- **Description**: Returns the week number in the year from the given date
- **Usage**: `int16 YearweekFromDate(date)`
- **Example**: If mylink.mydate contains the date 2008-08-18, then the two following functions are equivalent, and return the value 33: YearweekFromDate("2008-08-18") YearweekFromDate(mylink.mydate)
