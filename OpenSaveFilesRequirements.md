#specification to improve the user experience using code and sample worlds and save and opening their own files for packaged version

# Introduction #
Due to the packaged versions of rurple, the open and save behavior for code and world files need to be rethought in order to deal with file locations and properties on various platforms.


# Configuration file #
Currently rurple creates a .rurple folder where it stores a rurple.lang file to remember in which language the application was used the last time. This should probably be moved to a location that is platform specific:
  * .config/rurple on Linux
  * user/application data/rurple  on Windows (need to double check exact location)
  * to be verified for mac

# Sample and user's files #
As we currently have 2 open/save buttons for code and world files, and the software comes with sample files and encourages users to save their own we need to come up with a solution which doesn't make the software more complicated while keeping the same logic as when it was running from source.

Taking into consideration multi-user systems and various scenari here is the solution we feel the most appropriate:
  * source version: no change in the behavior
  * Packaged version:
    * install the sample files in the program directories
    * at startup check for a rurple directory in the user's home
    * if one, do nothing
    * else
      * create one
      * copy sample files as read only files (so kids can't modify but can save as)
    * after any upgrade overwrite those sample files (for example by adding a version file in .config/rurple)
    * ask confirmation when user is overwriting a file