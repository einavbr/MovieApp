select count(*) as amount_movies
from (
	select m.movie_id,
		count(distinct a.id) as amount_actors_in_movie
	from actors as a
	join movies_actors as ma
	on ma.actor_id = a.id
	join movies as m
	on m.movie_id = ma.movie_id
	where a.actor_name = "Tom Hanks"
	group by m.movie_id
) as t
where amount_actors_in_movie = 1
;
