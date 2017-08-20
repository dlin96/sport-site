# sport-site

## Useful Links
1. [nfldb api](http://pdoc.burntsushi.net/nfldb)
2. [mysql](https://dev.mysql.com/doc/refman/5.7/en/creating-database.html)
3. [nba_db](http://databasebasketball.com/stats_download.htm) databasebasketball only goes up to 2010
4. [nba/mlb api](https://erikberg.com/api#) invitation only. 
5. [nfl/nba api](https://www.suredbits.com/api/nfl/stats/) free
6. [D3js](https://d3js.org/)
7. [React.js](https://facebook.github.io/react/docs/introducing-jsx.html)  
  
## ML Tools (Python)  
1. Scikit Learn  
2. Numpy  
3. Jupyter  
4. Matplotlib  
5. tensorflow.  

## Idea
Create a multi-platform application that allows users to compare statistics of players from the NBA or NFL  
side-by-side. Eventually, we want to chart the statistics of players each season and analyze that along with  
the player's schedule to try and create accurate projections for the season (and next game).  

## Clients
Web -- MySQL database, Node.js server, express, and react front end (in progress). 
Android -- Node.js for the backend, same MySQL database

## Progress  
Android progress is stalled because of lack of autocomplete library (like typeaheadjs) to complete player search. This will continue after web is completed. Web has basic functionality of comparing two NBA players. The next steps are to use reactjs on the front end to create a better UI, host the site on AWS and to add in NFL data. Additionally, I will migrate my fantasy-football tool into this repository to get the depth charts of the NFL teams. 

