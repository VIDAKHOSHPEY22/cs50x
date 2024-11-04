SELECT name
FROM people
WHERE id IN
    (SELECT DISTINCT directors.person_id
     FROM directors
     JOIN movies ON movies.id = directors.movie_id
     WHERE movie_id IN
         (SELECT movie_id
          FROM ratings
          WHERE rating >= 9));
