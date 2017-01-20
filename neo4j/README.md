## Neo4j



### EJERCICIO: Construir los nodos :Tag para cada uno de los tags que aparecen en las preguntas. Construir las relaciones ```post-[:TAGGED]->tag``` para cada tag y también ```tag-[:TAGS]->post```

Para ello, buscar en la ayuda las construcciones WITH y UNWIND y las funciones replace() y split() de Cypher. La siguiente consulta debe retornar 1192 resultados:

```neo4j
MATCH p=(t:Tag)-[:TAGS]->(:Question)
	WHERE t.name =~ "^java$|^c\\+\\+$" RETURN count(p);
```


#### Borrar las Tags:
```neo4j
MATCH (n: Tag)
	DETACH DELETE n
;
```

#### Definir sus restricciones:
```neo4j
CREATE CONSTRAINT ON (t:Tag)
	ASSERT t.Name IS UNIQUE;
```

#### Solución:
```neo4j
MATCH ( c:Question )
	UNWIND SPLIT(replace(c.Tags,">", "<"), "<") as tagC
		WITH distinct tagC as tag, c as pregunta
		MERGE (t:Tag {name: tag })
		MERGE (t)-[:TAGS]->(pregunta)
		MERGE (pregunta)-[:TAGGED]->(t)
;
```
Ampliamente mejorable el _split_, pero válido.

```text
Added 874 labels, created 874 nodes, set 874 properties, created 46218 relationships, statement executed in 23598 ms.
```


La siguiente consulta muestra los usuarios que preguntan por cada Tag:

```neo4j
MATCH (t:Tag)-->(:Question)<--(u:User) RETURN t.name,collect(distinct u.Id) ORDER BY t.name;
```

El mismo MATCH se puede usar para encontrar qué conjunto de tags ha usado cada usuario cambiando lo que retornamos:

```neo4j
MATCH (t:Tag)-->(:Question)<--(u:User) RETURN u.Id,collect(distinct t.name) ORDER BY toInt(u.Id);
```


### EJERCICIO: Relacionar cada usuario con los tags de sus preguntas a través de la relación _:INTERESTED_IN_.

```neo4j
MATCH (u: User)-[:WROTE]->(:Question)-[:TAGGED]->(label: Tag)
	MERGE (u)-[:INTERESTED_IN]->(label);
```

Salida:
```text
Created 12327 relationships, statement executed in 381 ms.
```


### EJERCICIO: Recomendar a los usuarios tags sobre los que podrían estar interesados en base a tags en los que los usuarios con los que están relacionados con _:RECIPROCATE_ están interesados y ellos no, ordenado por número de usuarios interesados en cada tag.

```neo4j
MATCH (usuario1: User)-[:RECIPROCATE]->(usuario2: User)-[:INTERESTED_IN]->(etiqueta)
	WHERE NOT (usuario1)-[:INTERESTED_IN]->(etiqueta)
	WITH etiqueta as etiqueta, usuario1 as usuario
	MATCH(interesados)-[:INTERESTED_IN]->(etiqueta)
		WITH etiqueta as etiqueta, usuario as u, count(interesados) as inter
		ORDER BY inter desc
		RETURN u as idusuario, COLLECT(distinct etiqueta.name) AS recomendaciones
```
[Ejemplo de salida en CSV](./recomendaciones.csv)

