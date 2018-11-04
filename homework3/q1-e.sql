select city.name
	from city join country
	on city.countrycode = country.code
	where country.continent = "North America"
order by city.population desc
limit 1;