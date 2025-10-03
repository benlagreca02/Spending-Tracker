# Spending tracker

I want something that sits in my apartment, and visibly _shows_ me how much I've
spent over the past month.

Going to take advantage of email alerts, IMAP, Python, and an ESP32 variant w/
arduino.

## Client
XIAO ESP32-C3 board, programmed with arduino libaries.
Chosen becasue:
    - Has Wifi
    - Cheap
    - Popular and easily programmed (Arduino is extremely easy)
    - Cute
    - I2C communication (For LCD screen)

## Server
I use the term server loosely. In its current implementation, I have my homelab
server run a cron job every so often (haven't decided a time interval yet) that
will download all emails about charges on my credit card, and do some math, then
send it to the client.

UDP packets (not a big deal if I miss one)

Client will be "dumb", just listens for messages



## Features/plans/requirements


### MVP
Uses LED meter I found (hopefully)
Keeps track of transactions over the past 30 days (rolling mode)
Shows total spending on screen (uncategorized)


### maybe one day

Can switch modes between:
- Keeps track of transactions over the past 30 days (rolling mode)
- Keeps track of transactions over the past 30 day pay period (month mode)

Has some kind of buttons for switching mode (or maybe it just does it every few
seconds

Client can use buttons (maybe) to cycle between different spending categories
(groceries, gas, etc)

Server can classify different transactions, and client can show different
categories of spending
