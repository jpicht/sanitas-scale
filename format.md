File structure
==============

Overview
--------
The file constists of 64 blocks with 128 bytes each. First all the data for the user profiles is stored in six blocks for each profile. All these blocks contain 16 bit values. These blocks are followed by two unknown/blank blocks. Last in the file there are two blocks with metadata, where I think I got a basic understanding of some fields.

Content blocks
--------------
```
 block  description  bytes  interpretation
     0  weight           2           100 g 
     1  body fat         2            .1 % 
     2  % water          2            .1 % 
     3  % muscle         2            .1 % 
     4  date             2       see below
     5  time             2       see below
```  

Data Formats
------------
The weight is stored in 100g increments. The body fat, water and muscle values are stored in .1 % increments.

The date is stored packed in a 7 bits for the year (with 1920 as year zero), 4 bits for the month and 5 bit for the day of month. The base year 1920 seems a reasonable choice, if you want to use the same encoding for the day of birth. So I'll go with this assumption.
```
bit  : f e d c b a 9 8 7 6 5 4 3 2 1 0 
value: 1 0 1 1 1 1 0 0 0 1 1 0 1 0 0 1
      |-------------|-------|---------|
       year-1920     month   day
```

The time is stored with the hour (24h format) in the upper byte and the minute in the lower byte.
```
bit  : f e d c b a 9 8 7 6 5 4 3 2 1 0 
      |---------------|---------------|
       hour            minutes
```

First meta data block
---------------------
I currently assume this block contains eight bytes of configuration data for every channel. The first byte appears to be 0x00 on unused profiles and 0x01 for the first profile. It could be an indicator for the sex of the profile. The second byte contains the height in centimeters. The next two bytes contain the date of birth programmed into the scale. The next byte seems to be unused, the one after that contains the counter of how many measurements are currently stored for that profile.

