CREATE TABLE circuits (
    circuitId INTEGER PRIMARY KEY, 
    circuitRef VARCHAR, 
    name VARCHAR,
    location VARCHAR, 
    country VARCHAR, 
    lat DECIMAL (8, 6), 
    lng DECIMAL (9, 6), 
    alt INTEGER, 
    url VARCHAR
)
CREATE TABLE constructor_results (
    constructorResultsId INTEGER PRIMARY KEY, 
    raceId INTEGER REFERENCES races (raceId), 
    constructorId INTEGER REFERENCES constructors (constructorId), 
    points INTEGER, 
    status VARCHAR
)
CREATE TABLE constructor_standings (
    constructorStandingsId INTEGER PRIMARY KEY, 
    raceId INTEGER REFERENCES races (raceId), 
    constructorId INTEGER REFERENCES constructors (constructorId), 
    points INTEGER, 
    position INTEGER, 
    positionText VARCHAR, 
    wins INTEGER, ""
)
CREATE TABLE constructors (
    constructorId, 
    constructorRef, 
    name, 
    nationality, 
    url,
    ""
)
CREATE TABLE driver_standings (
    driverStandingsId INTEGER PRIMARY KEY, 
    raceId INTEGER REFERENCES races (raceId), 
    driverId INTEGER REFERENCES drivers (driverId), 
    points INTEGER, 
    position INTEGER, 
    positionText VARCHAR, 
    wins INTEGER
)
CREATE TABLE drivers (
    driverId INTEGER PRIMARY KEY, 
    driverRef VARCHAR, 
    number VARCHAR, 
    code VARCHAR, 
    forename VARCHAR, 
    surname VARCHAR, 
    dob VARCHAR, 
    nationality VARCHAR, 
    url VARCHAR
)
CREATE TABLE laptimes (
    raceId INTEGER REFERENCES races (raceId), 
    driverId INTEGER REFERENCES drivers (driverId), 
    lap INTEGER, 
    position INTEGER, 
    time VARCHAR, 
    milliseconds 
    INTEGER
)
CREATE TABLE pitstops (
    raceId INTEGER REFERENCES races (raceId), 
    driverId INTEGER REFERENCES drivers (driverId), 
    stop INTEGER, lap INTEGER, 
    time VARCHAR, 
    duration DECIMAL, 
    milliseconds INTEGER
)
CREATE TABLE qualifying (
    qualifyId INTEGER PRIMARY KEY,
    raceId INTEGER REFERENCES races (raceId),
    driverId INTEGER REFERENCES drivers (driverId),
    constructorId INTEGER REFERENCES constructors (constructorId) ON DELETE CASCADE,
    number INTEGER,
    position INTEGER,
    q1 VARCHAR,
    q2 VARCHAR,
    q3 VARCHAR
)
CREATE TABLE races (
    raceId INTEGER PRIMARY KEY, 
    year INTEGER, round INTEGER, 
    circuitId INTEGER REFERENCES circuits (circuitId), 
    name VARCHAR, 
    date DATE, 
    time TIME, 
    url VARCHAR
)
CREATE TABLE results (
    resultId, 
    raceId INTEGER REFERENCES races (raceId), 
    driverId INTEGER REFERENCES drivers (driverId), 
    constructorId INTEGER REFERENCES constructors (constructorId), 
    number INTEGER, 
    grid INTEGER, 
    position INTEGER, 
    positionText VARCHAR, 
    positionOrder INTEGER, 
    points INTEGER, 
    laps INTEGER, 
    time VARCHAR, 
    milliseconds INTEGER, 
    fastestLap VARCHAR, 
    rank INTEGER, 
    fastestLapTime VARCHAR, 
    fastestLapSpeed DECIMAL, 
    statusId INTEGER
)
CREATE TABLE seasons (
    year INTEGER,
    url VARCHAR
)
CREATE TABLE status (
    statusId INTEGER PRIMARY KEY, 
    status VARCHAR
)
 
