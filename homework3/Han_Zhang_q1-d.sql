select countrycode, count(name) as number_of_cities
	from city
group by countrycode
having number_of_cities >=50
order by countrycode;