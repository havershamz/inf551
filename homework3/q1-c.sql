select continent, sum(number_of_cities) as number_of_cities
	from country join
		(select countrycode, count(name) as number_of_cities
			from city
		group by countrycode) as country_city
	on country.code = country_city.countrycode
group by continent
order by continent;