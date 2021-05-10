SELECT COUNT(*) FROM movies_with_genre_index
WHERE genres CONTAINS 'Horror' and year >= 1980 and year <= 1990
ALLOW FILTERING;
