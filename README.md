# Spending tracker

I want something that sits in my apartment, and visibly _shows_ me how much I've
spent over the past month. This is my overengineered solution.

Going to take advantage of email alerts on my credit card, IMAP, Python, and
Sqlite3 ESP32-C3 board.


Small LCD screen with a ESP32-C3 core that displays how much money
I've spent. Transactions pulled from Email, then
parses those emails with Regex, and stores relevant information
using sqlite3. Database is then read, and budget usage is
calculated. A UDP message is sent to the ESP32-C3, which has a
custom character set defined for display a "meter" along the bottom
row showing how much of the set budget I've spent.




## Client
XIAO ESP32-C3 board, programmed with arduino libaries.
Chosen becasue:
    - Has Wifi
    - Cheap
    - Popular and easily programmed (Arduino is extremely easy)
    - I2C communication (For LCD screen)

## Server
I use the term server loosely. In its current implementation, I have my homelab
server run a cron job every so often (haven't decided a time interval yet) that
will download all emails about charges on my credit card, and do some math, then
send it to the client.

UDP packets (not a big deal if I miss one)

Client will be "dumb", just listens for messages


## Plans for future

Can switch modes between:
- Keeps track of transactions over the past 30 days (rolling mode)
- Keeps track of transactions over the past 30 day pay period (month mode)

Has some kind of buttons for switching mode (or maybe it just does it every few
seconds

Client can use buttons (maybe) to cycle between different spending categories
(groceries, gas, etc)

Server can classify different transactions, and client can show different
categories of spending
