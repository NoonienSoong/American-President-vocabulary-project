

##Introduction:
The premise of this project is that American politicians must speak to their electorate with the level of linguistic sophistication that the electorate understands. As a result, political speeches are great indicators of the state of the American vocabulary. This project then sets out to prove that over the last century, the vernacular used by the average American — representative of the electorate — has been drastically simplified. This will be achieved by doing unique word counts on American political speeches.


##Motivation:
As the 2016 presidential primaries unfold in perhaps the most polarized political climate since the Civil War, there is one thing that unites both parties — shock at the success of Donald Trump’s candidacy and his ability to galvanize a group of Americans despite weekly gaffes and a generally “unpresidential” demeanor.
To date, the results of the primaries have defied prediction after prediction from even the most reputable pollsters and election forecasters. Though this project will not examine Trump specifically, we think it is a step towards understanding the relationship between the political climate and the current American electorate, and perhaps also a way to understand how an apparently bigoted, alarmingly unpredictable, and unqualified candidate has amassed such strong support.


##Running Code

###Make sure that the right permissions are set on the make file:

>*$ chmod +x make*

### run the make file wich will in turn scrape the data sources and runn the analytics:


>*$ make*


>####note: *runnning make produces two  json files (NJ_data.json and pres_wc.json) these are products of the two scrape funcitions and are necessary to run the mapper.py in the repo*	

##Running mapper.py and reducer.py (unique word count for each president):
========================================================================

We used MapReduce to verify the preliminary research that we had already
conducted using webscrapers, and to process larger amounts of data (please see data sources). 

Our input was json-formatted.

_--- To run on Dumbo (Hadoop cluster) ---_

>*$ hadoop jar /opt/cloudera/parcels/CDH-5.4.5-1.cdh5.4.5.p0.7/lib/hadoop-mapreduce/hadoop-streaming.jar -numReduceTasks 16 -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py -file <input_file> -file list_of_presidents -input </path/to/input_file/hdfs> -output </path/to/output>*

1. mapper.py, reducer.py, and the input file must be sent using the -file flag as well as specified with the -mapper, -reducer, and -input flags, respectively. "list_of_presidents" must also be sent with the -file flag.

2. The shebang for local use must be removed from mapper.py and reducer.py for the job to run on Dumbo (these are here for local testing).

_--- To run locally --_-
(we processed some data this way due to intermittent Dumbo issues)

*Make sure mapper.py and reducer.py are executable.*

>*$ cat <input_file> | ./mapper.py | sort | ./reducer.py | sort*


###Data Sources
- *"Miller Center." American President-speeches. N.p., n.d. Web. 04 May 2016. <http://millercenter.org/president/speeches>.*

-*"The American Presidency Project." The American Presidency Project. N.p., n.d. Web. 04 May 2016. <http://www.presidency.ucsb.edu/>.*
