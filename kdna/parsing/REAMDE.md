## 2. Parsing of the .conf file

Once you've created the `kdna.conf` file, you move on to the parsing. 

Parsing a file means we are breaking down the data into its component parts, such as fields or elements, and then processing or interpreting them according to the rules of the specific file format.

The file `parser.py` will automatically apply the parsing based on our criteria ( see 1. kdna.conf file format). 

Once the parsing is done, the different data that we have recovered will be used to create the different objects, here `server` and `auto-backup`.

We will then save the initialized objects in lists in order not to lose the data. 