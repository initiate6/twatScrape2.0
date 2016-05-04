# twatScrape2.0
Data Mining for passwords

linkedout.py will parse a linkedin profile page. Printing links, unique list of words, unique list of hash tags, unique list of dates, and connector words.
hash tags will be used to search in twitters streaming API for more words related to those topics. 
connector words = words that are less than 3 used to concatenate other words for password cracking. 

TODO: Parse each link that was collected from the profile page. 


End result will be a custom dictionary that can be used for password cracking. Note this is just the base words still need to use hashcat rules to modify them.


