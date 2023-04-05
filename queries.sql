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

--display tv shows from highest to lowest rating 
select titles.title, round(rating, 2)
from(titles join  
        (select E.parent_tconst, avg(rating) as rating
        from episodes E join ratings R ON R.tconst=E.tconst 
        group by E.parent_tconst
        order by parent_tconst desc) ON parent_tconst = titles.tconst)
order by rating desc; 

--display top 10 highest rated tvShows 
select titles.title, round(rating, 2)
from(titles join  
        (select E.parent_tconst, avg(rating) as rating
        from episodes E join ratings R ON R.tconst=E.tconst 
        group by E.parent_tconst
        order by parent_tconst desc) ON parent_tconst = titles.tconst)
order by rating desc limit 10; 

--display the average episode rating by parent_tconst
select titles.title, round(rating, 2)
from(titles join  
        (select E.parent_tconst, avg(rating) as rating
        from episodes E join ratings R ON R.tconst=E.tconst 
        group by E.parent_tconst
        order by parent_tconst desc) ON parent_tconst = titles.tconst)
where parent_tconst = "tt0279600";

--display top 10 tvShows by genre 
select titles.title, round(rating, 2)
from((titles join  
        (select E.parent_tconst, avg(rating) as rating
        from episodes E join ratings R ON R.tconst=E.tconst 
        group by E.parent_tconst
        order by parent_tconst desc) ON parent_tconst = titles.tconst) 
        JOIN genres G ON G.tconst = titles.tconst)
where genre = 'Comedy'
order by rating desc limit 10; 

--list of all episodes for a given tconst
select title, season, epNo as episodeNumber
from episodes E full outer join titles T ON E.tconst = t.tconst
where parent_tconst = 'tt0108778'
order by season, epNo; 

--provide list of all the actors for a movie 
select name 
from ((people P JOIN actors A ON P.nconst = A.nconst) join movies M ON M.tconst = A.tconst) 
where A.tconst = 'tt1041829';

--provides list of all the crew for a movie 
select name 
from ((people P JOIN crew A ON P.nconst = A.nconst) join movies M ON M.tconst = A.tconst) 
where A.tconst = 'tt1041829';

-- provide list of titles that a given actor has been in (movies and tvSeries) 
select title
from (((people P JOIN actors A ON P.nconst = A.nconst) 
    join movies M ON M.tconst = A.tconst) 
    join titles T on T.tconst = M.tconst) 
where A.nconst = 'nm0000098'
UNION
select title 
from (((people P JOIN actors A ON P.nconst = A.nconst) 
    join tvSeries M ON M.tconst = A.tconst) 
    join titles T on T.tconst = M.tconst)
where A.nconst = 'nm0000098'; 

--list of tvSeries an actor has been in 
select title 
from (((people P JOIN actors A ON P.nconst = A.nconst) 
    join tvSeries M ON M.tconst = A.tconst) 
    join titles T on T.tconst = M.tconst)
where A.nconst = 'nm0000098'; 

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

--number of titles that have a different title than their original title 
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