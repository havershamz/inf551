create view country_city_view as
	select countrycode, count(name) as number_of_cities
	from city
	group by countrycode
	order by countrycode;