-- Dimensions
SELECT * FROM recargas_tiempo ORDER BY fecha;
SELECT * FROM recargas_direccion;
SELECT * FROM recargas_region;
SELECT * FROM recargas_gerente;
SELECT * FROM recargas_empresa;
SELECT * FROM recargas_distribuidor;
-- Fact
SELECT DISTINCT distribuidor_id FROM recargas_venta 
WHERE empresa_id = 15; 

-- Numbers of row
SELECT COUNT(id) AS 'total' FROM recargas_venta;

-- DELETE FROM recargas_venta WHERE recargas_venta.tiempo_id >= 427;
-- UPDATE recargas_venta 
-- SET distribuidor_id =  1101 
--     , direccion_id = 3
--     , region_id = 10
--     , gerente_id = 10
--     , empresa_id = 15 
-- WHERE distribuidor_id IN (
-- SELECT id FROM recargas_distribuidor WHERE activo = 0
-- )

-- SELECT DISTINCT distribuidor_id FROM recargas_venta 
-- WHERE direccion_id = 3;



-- Query to find Fact by Dim : this case Venta by Gerente
SELECT recargas_gerente.nombre,
       SUM(recargas_venta.monto) as monto_total, 
       SUM(recargas_venta.cuota) as cuota_total
FROM recargas_venta 
INNER JOIN recargas_gerente
ON recargas_venta.gerente_id= recargas_gerente.id 
INNER JOIN recargas_tiempo 
ON recargas_tiempo.id = recargas_venta.tiempo_id
WHERE (recargas_tiempo.fecha BETWEEN '2018-04-01' AND '2018-04-09')
AND recargas_gerente.nombre <> 'DESJERARQUIZADO'
GROUP BY recargas_gerente.nombre
ORDER BY monto_total DESC;

SELECT monto, monto_iva, cuota FROM recargas_venta
-- UPDATE recargas_venta
-- SET monto = monto / 100000,
--     monto_iva = monto_iva / 100000,
--     cuota = cuota / 100000

SELECT * FROM reporteria_produccionplan
-- UPDATE reporteria_produccionplan
-- SET renta_mensual = renta_mensual / 100000,
--     recarga_plan = recarga_plan / 100000