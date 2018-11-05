select continent, sum(number_of_cities) as number_of_cities
	from country join country_city_view
	on country.code = country_city_view.countrycode
group by continent
order by continent;