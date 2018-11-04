select city.name as city_name, country.name as country_name
	from city join country
	on city.countrycode = country.code
order by city_name;