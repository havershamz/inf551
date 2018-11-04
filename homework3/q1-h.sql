select name from country
where code in(
	select cl2.countrycode
		from countrylanguage as cl1 inner join countrylanguage as cl2
		on cl1.countrycode = cl2.countrycode
		where cl1.language = "English"
		and cl1.isofficial = "T"
		and cl2.language = "French"
		and cl2.isofficial = "F");