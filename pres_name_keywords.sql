-----DROP TABLE IF EXISTS------

DROP TABLE IF EXISTS president_keywords;


-----CREATING TABLE-------

Create table president_keywords (president_order int, president_name string) row format delimited fields terminated by ',';

---DESCRIBE PRES ----
describe president_keywords;

---LOAD TABLE----

load data local inpath '/home/naj273/list_of_presidents.txt' into table president_keywords;

select * from president_keywords;
