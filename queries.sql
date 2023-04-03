Select * from actors;
select * from crew; 
select * from episodes; 
select distinct genre from genres; 
select * from movies; 
select * from people; 
select * from profession; 
select * from ratings; 
select * from titles; 
select * from tvSeries; 

--RATING QUERIES--
-- display all movies in order of highest to lowest rating  
select title, rating
from ((titles T JOIN movies S ON T.tconst = S.tconst) join ratings R ON R.tconst = T.tconst)
order by rating desc; 

--display top 10 highest rated movies 
select title, rating
from ((titles T JOIN movies S ON T.tconst = S.tconst) join ratings R ON R.tconst = T.tconst)
order by rating desc limit 10; 

--display top 10 movies by genre 
select title, rating, genre
from (((titles T JOIN movies S ON T.tconst = S.tconst) join ratings R ON R.tconst = T.tconst) join genres G on G.tconst=T.tconst)
where genre = 'Comedy'
order by rating desc limit 10; 

-- display all tvShows in order of highest to lowest rating  
select title, ave()
from ((titles T JOIN episodes E ON T.tconst = E.parent_tconst) join ratings R ON R.tconst=T.tconst) 
order by title desc; 

--display top 10 highest rated tvShows 
select title, rating
from ((titles T JOIN movies S ON T.tconst = S.tconst) join ratings R ON R.tconst = T.tconst)
order by rating desc limit 10; 

--display top 10 tvShows by genre 
select title, rating, genre
from (((titles T JOIN movies S ON T.tconst = S.tconst) join ratings R ON R.tconst = T.tconst) join genres G on G.tconst=T.tconst)
where genre = 'Comedy'
order by rating desc limit 10; 

Select name
from people P JOIN actors A ON P.nconst = A.nconst;  

Select name
from people P JOIN crew A ON P.nconst = A.nconst; 

select title
from titles T JOIN tvSeries S ON T.tconst = S.tconst;


select title, originaltitle
from titles T JOIN movies S ON T.tconst = S.tconst
where title != originaltitle
order by title asc; 

--number of tit
select count(title)
from titles T JOIN movies S ON T.tconst = S.tconst
where title != originaltitle; 

--number of seasons for each tv show 
SELECT distinct title, max(season)
from episodes E join titles T on E.parent_tconst = T.tconst
group by title
order by max(season) desc; 

--number of episodes for each tv show 
SELECT distinct title, count(epNo)
from episodes E join titles T on E.parent_tconst = T.tconst
group by title
order by count(epNo) desc; 