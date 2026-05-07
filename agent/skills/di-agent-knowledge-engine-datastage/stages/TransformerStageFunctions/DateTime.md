# DataStage Date and Time Transformer Functions

Reference of builtin transfomer functions for manipulating date and time fields

### ConvertDatum

- **Description**: Convert date format
- **Usage**: `anystring ConvertDatum(anystring:string, anystring:string)`

### ConvertTimeZone

- **Description**: Convert to different time zone
- **Usage**: `anystring ConvertTimeZone(int32:number, int32:number, int32:number, int32:number, int32:number, int32:number, anystring:string, anystring:string)`

### CurrentDate

- **Description**: Return the current date
- **Usage**: `date CurrentDate()`

### CurrentTime

- **Description**: Return the current time
- **Usage**: `time CurrentTime(string)`

### CurrentTimeMS

- **Description**: Return the current time including microseconds
- **Usage**: `time CurrentTimeMS()`

### CurrentTimestamp

- **Description**: Return the current timestamp
- **Usage**: `timestamp CurrentTimestamp(string)`

### CurrentTimestampMS

- **Description**: Return the current timestamp including microseconds
- **Usage**: `timestamp CurrentTimestampMS()`

### DateFromComponents

- **Description**: Returns a date object representing the specified year, month and day
- **Usage**: `date DateFromComponents(int32:years, int32:months, int32:days)`

### DateFromDaysSince

- **Description**: Returns a date by adding an integer to a baseline date
- **Usage**: `date DateFromDaysSince(int32:number, string:"yyyy-mm-dd")`

### DateFromDaysSince2

- **Description**: Returns a date by adding an integer to a baseline date
- **Usage**: `date DateFromDaysSince2(int32:number, date)`

### DateFromJulianDay

- **Description**: Returns a date from the given julian date
- **Usage**: `date DateFromJulianDay(uint32:juliandate)`

### DateOffsetByComponents

- **Description**: Returns the given date, offset by the given components of years, months and days
- **Usage**: `date DateOffsetByComponents(date:basedate, int32:yearoffset, int32:monthoffset, int32:dayoffset)`

### DateOffsetByDays

- **Description**: Returns the given date, offset by the number of days specified
- **Usage**: `date DateOffsetByDays(date:basedate, int32:offset)`

### DaysInMonth

- **Description**: Returns the number of days in the month of the given date
- **Usage**: `int32 DaysInMonth(date)`

### DaysInYear

- **Description**: Returns the number of days in the year of the given date
- **Usage**: `int32 DaysInYear(date)`

### DaysSinceFromDate

- **Description**: Returns the number of days from source date to the given date
- **Usage**: `int32 DaysSinceFromDate(date, string:"yyyy-mm-dd")`

### DaysSinceFromDate2

- **Description**: Returns the number of days from source date to the given date
- **Usage**: `int32 DaysSinceFromDate2(date, date)`

### HoursFromTime

- **Description**: Return the hour portion of a time
- **Usage**: `int8 HoursFromTime(time)`

### JulianDayFromDate

- **Description**: Returns julian day from the given date
- **Usage**: `int32 JulianDayFromDate(date)`

### MicroSecondsFromTime

- **Description**: Returns the microsecond portion from a time
- **Usage**: `int32 MicroSecondsFromTime(time)`

### MidnightSecondsFromTime

- **Description**: Returns the number of seconds from midnight to the given time
- **Usage**: `dfloat MidnightSecondsFromTime(time)`

### MinutesFromTime

- **Description**: Returns the minute portion from a time
- **Usage**: `int8 MinutesFromTime(time)`

### MonthDayFromDate

- **Description**: Returns the day of the month given the date
- **Usage**: `int8 MonthDayFromDate(date)`

### MonthFromDate

- **Description**: Returns the month number given the date
- **Usage**: `int8 MonthFromDate(date)`

### NextWeekdayFromDate

- **Description**: Returns the date of the specified day of the week soonest after the source date
- **Usage**: `date NextWeekdayFromDate(date:sourcedate, string:dayname)`

### NthWeekdayFromDate

- **Description**: Return the date which lies on the specified weekday offset from the baseline date
- **Usage**: `date NthWeekdayFromDate(date:sourcedate, string:dayname, int32:offset)`

### PreviousWeekdayFromDate

- **Description**: Returns the date of the specified day of the week most recent before the source date
- **Usage**: `date PreviousWeekdayFromDate(date:sourcedate, string:dayname)`

### SecondsFromTime

- **Description**: Returns the second portion from a time
- **Usage**: `dfloat SecondsFromTime(time)`

### SecondsSinceFromTimestamp

- **Description**: Returns the number of seconds between two timestamps
- **Usage**: `dfloat SecondsSinceFromTimestamp(timestamp, string:"yyyy-mm-dd hh:nn:ss")`

### SecondsSinceFromTimestamp2

- **Description**: Returns the number of seconds between two timestamps
- **Usage**: `dfloat SecondsSinceFromTimestamp2(timestamp, timestamp)`

### TimeDate

- **Description**: Returns the time and date as a formatted string
- **Usage**: `anystring TimeDate()`

### TimeFromComponents

- **Description**: Returns a time object representing the specified hour, minutes, seconds and microseconds
- **Usage**: `time TimeFromComponents(int32:hours, int32:minutes, int32:seconds, int32:microseconds)`

### TimeFromMidnightSeconds

- **Description**: Returns the time given the number of seconds since midnight
- **Usage**: `time TimeFromMidnightSeconds(dfloat:seconds)`

### TimeOffsetByComponents

- **Description**: Returns the given time, offset by the given components of hours, minutes and seconds
- **Usage**: `time TimeOffsetByComponents(time:basetime, int32:houroffset, int32:minuteoffset, dfloat:secondoffset)`

### TimeOffsetBySeconds

- **Description**: Returns the given time, offset by the number of seconds or part seconds specified
- **Usage**: `time TimeOffsetBySeconds(time:basetime, dfloat:offset)`

### TimestampFromDate

- **Description**: Returns a timestamp from the given date
- **Usage**: `timestamp TimestampFromDate(date, string)`

### TimestampFromDateTime

- **Description**: Returns a timestamp from the given date and time
- **Usage**: `timestamp TimestampFromDateTime(date, time)`

### TimestampFromSecondsSince

- **Description**: Return the timestamp from the number of seconds from the base timestamp
- **Usage**: `timestamp TimestampFromSecondsSince(dfloat:seconds, string:timestamp)`

### TimestampFromSecondsSince2

- **Description**: Return the timestamp from the number of seconds from the base timestamp
- **Usage**: `timestamp TimestampFromSecondsSince2(dfloat:seconds, timestamp)`

### TimestampFromTime

- **Description**: Returns a timestamp from the given time
- **Usage**: `timestamp TimestampFromTime(time, string)`

### TimestampFromTime2

- **Description**: Returns a timestamp with the date from the specified timestamp argument and the time from the specified time argument
- **Usage**: `timestamp TimestampFromTime2(time, timestamp)`

### TimestampFromTimet

- **Description**: Returns a timestamp from the given unix time_t value
- **Usage**: `timestamp TimestampFromTimet(int64:timetvalue)`

### TimestampOffsetByComponents

- **Description**: Returns the given timestamp, offset by the given components of years, months, days, hours, minutes and seconds
- **Usage**: `timestamp TimestampOffsetByComponents(timestamp:basetimestamp, int32:yearoffset, int32:monthoffset, int32:dayoffset, int32:houroffset, int32:minuteoffset, dfloat:secondoffset)`

### TimestampOffsetBySeconds

- **Description**: Returns the given timestamp, offset by the number of seconds or part seconds specified
- **Usage**: `timestamp TimestampOffsetBySeconds(timestamp:basetimestamp, dfloat:offset)`

### TimetFromTimestamp

- **Description**: Returns a unix time_t value from the given timestamp
- **Usage**: `int64 TimetFromTimestamp(timestamp)`

### WeekdayFromDate

- **Description**: Returns the day of the week from the given date
- **Usage**: `int8 WeekdayFromDate(date, string:startdayname)`

### YeardayFromDate

- **Description**: Returns the day number in the year from the given date
- **Usage**: `int16 YeardayFromDate(date)`

### YearFromDate

- **Description**: Returns the year from the given date
- **Usage**: `int16 YearFromDate(date)`

### YearweekFromDate

- **Description**: Returns the week number in the year from the given date
- **Usage**: `int16 YearweekFromDate(date)`
