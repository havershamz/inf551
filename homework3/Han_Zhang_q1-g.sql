select name, gnp
	from country
having gnp > any(select gnp
	from country);