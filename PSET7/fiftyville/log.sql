-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Looking for a crime scene report that matches the date and the location of the crime
SELECT description
FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND street = 'Humphrey Street';

-- Checking Their Interview Transcripts at the Time and Mentions Bakery
SELECT transcript
FROM interviews
WHERE day = 28 AND month = 7 AND transcript LIKE '%bakery%';

-- Look through security footage to look for cars that left parking lot in time frame (10:15 - 10:25)
SELECT *
FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND year = 2021 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- Find the Names of the people associated with the Same License Plate
SELECT p.name from people p
JOIN bakery_security_logs ON p.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.day = 28 AND bakery_security_logs.month = 7
AND bakery_security_logs.year = 2021 AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute BETWEEN 15 AND 25;
|
-- Find All withdraws from the specific ATM referenced in 2nd Witness Transcript
SELECT * FROM atm_transactions
WHERE year = 2021 AND month = 7
AND day = 28 AND atm_location = 'Leggett Street';

-- Finds the Name of the people associated with the ATM account Number
SELECT people.name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021 AND month = 7
AND day = 28 AND atm_location = 'Leggett Street';
|
-- Check Phone Calls During the Time Frame and Tap Into Call
SELECT caller FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
AND duration <= 60;

-- Find the Names of the Callers
SELECT people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28
AND phone_calls.duration <= 60;

-- Flights From Airport in Fiftyville (8 is ID #)
SELECT * FROM airports
WHERE city = 'Fiftyville';

-- Find Earliest Flight That Day (8: 20)
SELECT * FROM flights
WHERE origin_airport_id = 8 AND flights.year = 2021 AND flights.month = 7 AND flights.day = 29;

-- Find Passenger Names for the flight (Killer is Bruce)
SELECT people.name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE airports.city = 'Fiftyville'
AND flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20;

-- Find Flight Arrival Location (New York City)
SELECT airports.city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.origin_airport_id = 8
AND flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20;

-- Find Phone # of Bruce ((367) 555-5533)
SELECT phone_number FROM people
WHERE name = 'Bruce';

-- Check the Calls of Bruce to Find Accomplice (Robin)
SELECT people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28
AND phone_calls.duration <= 60 AND phone_calls.caller = '(367) 555-5533';

