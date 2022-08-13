# Website blocker 

A website blocker GUI app developed with python and tkinter. 
 
This application writes to the user's laptop hosts file to block websites 
To use this application, you need to run as administrator on your cmd prompt so 
that the program is able to access and write to your host files and run the application 
using "python (main file name)"

The main.pyw is the main file of the application where the program will be run, you may place all of the files 
into your system32 ( if you are on windows) and rename the main file to something else so you can easily 
identify the main file and run it in your cmd as an administrator. 

To block a website, you need to insert a website (Format either with "www" or without it. Example: www.google.com, google.com (no https:// require as well as no 
query in the url (must end in .com, org, .io, etc))) into the entry located on the middle frame and click on the block button. This 
will result on the program writing a local address and the block website into the host file which results in the user unable to access the website. 

The bottom frame contains a list of block websites format as radio buttons which user may click to have a test website button and unblock button pop up. 
These buttons allow the user to test and see if the website is fully block and unblock the selected website. 
The back and forward buttons are used to move across the pages and look at other block websites as each page contains up to 5 block websites.

Finally, the user may click on the history button to access all of the past block websites in another GUI. The user may click on any of the past 
block websites button to reblock the website if it is not currently block. 