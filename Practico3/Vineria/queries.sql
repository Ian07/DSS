/* Muestre porcentaje de tipos de vinos más vendidos en X año */
SELECT	tipo, count(tipo) as cantidad,
		round(count(tipo) * 100.0/(SELECT count(*) from vino),2) as porcentaje
FROM ORDEN  AS ord
JOIN VINO as v ON ord.vino = v.codigo 
JOIN TIEMPO as t on t.codigo = ord.codigo
WHERE año ='2011'
GROUP BY tipo
ORDER BY porcentaje DESC

/* 
cantidad de registro por año en la tabla tiempo
ejemplo: año 2011
*/
select año, count(año) cantidad from tiempo
group by año
order by cantidad desc

/*
tipos:
Malbec, Sangiovese, Pinot Noir, Merlot, Cabernet Sauvignon
*/

/*
vintage (temporada) :
Verano,Otoño, Invierno, Primavera
*/

/*
Cual es la temporada con mayor cantidad de ventas en X año
ejemplo: año 2011
*/

SELECT	vintage, count(vintage) as cantidad
FROM VINO  as v
JOIN ORDEN as ord ON ord.vino = v.codigo 
JOIN TIEMPO as t ON t.codigo = ord.codigo
WHERE t.año ='2011'
GROUP BY vintage
ORDER BY cantidad DESC

/*
Qué clientes han realizado más compras a lo largo de 4 años
ejemplo: años 1980 y 1984
*/

SELECT nombre, direccion
FROM TIEMPO as t
JOIN ORDEN as ord ON t.codigo = ord.codigo
JOIN CLIENTE as cli ON cli.codigo = ord.codigo
WHERE EXTRACT(YEAR FROM fecha) BETWEEN 1980 AND 1984





