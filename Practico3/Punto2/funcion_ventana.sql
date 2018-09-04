/*EJECUTAR ESTE COMANDO SOLO SI NO LEVANTO EL BKP Y GENERO LA BD */
CREATE TABLE empleado (
  empid integer,
  departamento text,
  salario integer,
  edad integer,
  primary key (empid)
);

/*EJECUTAR ESTE COMANDO SOLO SI NO LEVANTO EL BKP Y GENERO LA BD */
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (1,'ventas',3000,24);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (2,'ventas',3200,26);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (3,'ventas',3500,35);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (4,'distribucion',2000,22);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (5,'distribucion',2100,42);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (6,'distribucion',2400,40);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (7,'produccion',2800,41);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (8,'produccion',2400,29);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (9,'produccion',1900,19);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (10,'produccion',3000,45);
INSERT INTO empleado (empid,departamento,salario,edad) 
VALUES (11,'produccion',3000,40);

/* CON LA SIGUIENTE CONSULTA PODEMOS OBTENER EL SALARIO Y EDAD MEDIA POR DEPARTAMENTO*/
SELECT 
  empid,
  departamento,
  salario,
  edad,
  round(avg(salario) OVER ventana_departamento) AS sal_medio, 
  round(avg(edad) OVER ventana_departamento) AS ed_media 
FROM empleado 
WINDOW 
  ventana_departamento AS (PARTITION BY departamento);
  
/* SI QUEREMOS HACERLO A NIVEL EMPRESA DEBEMOS EJECUTAR LA SIGUIENTE CONSULTA */
SELECT 
  empid,
  departamento,
  salario,
  edad,
  round(avg(salario) OVER ventana_empresa) AS sal_medio, 
  round(avg(edad) OVER ventana_empresa) AS ed_media 
FROM empleado 
WINDOW 
  ventana_empresa AS ();
  
/*SI UTILIZARAMOS UN AVG SIN UTILIZAR UNA FUNCION VENTANA OBTENDRIAMOS LO SIGUIENTE*/
SELECT 
  departamento,
  avg(salario) AS sal_medio, 
  avg(edad) AS ed_media 
FROM empleado 
GROUP BY departamento;

  