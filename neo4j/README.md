## Neo4j


### Ejecutar en docker

```
$ docker run -p7474:7475 neo4j
```

### EJERCICIO: Construir los nodos :Tag para cada uno de los tags que aparecen en las preguntas. Construir las relaciones ```post-[:TAGGED]->tag``` para cada tag y también ```tag-[:TAGS]->post```

Para ello, buscar en la ayuda las construcciones WITH y UNWIND y las funciones replace() y split() de Cypher. La siguiente consulta debe retornar 1192 resultados:

```neo4j
MATCH p=(t:Tag)-[:TAGS]->(:Question) WHERE t.name =~ "^java$|^c\\+\\+$" RETURN count(p);
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


### EJERCICIO: Recomendar a los usuarios tags sobre los que podrían estar interesados en base a tags en los que los usuarios con los que están relacionados con _:RECIPROCATE_ están interesados y ellos no, ordenado por número de usuarios interesados en cada tag.




Código temporal por ordenar

```
create (t:Tag { Name:  })

WITH SPLIT(line.SWords, ";") AS SWords, line 
unwind range(0, size(Swords)-1) as i

merge (t:Tag { Name: tagname })

WITH split(line.TWords, ';') as splitted
UNWIND range(0, size(splitted) -1) as i
MERGE (t:Tag {Name: splitted[i]})
MERGE (sentence)-[:HAS_WORD {position: i}]->(w)



create constraint on (p:Post) assert p.Id IS UNIQUE;
create constraint on (t:Tag) assert t.Name IS UNIQUE;

MATCH ( c:Question )
	WITH c, SPLIT(c.Tags, ",") as tags
	UNWIND RANGE(0,SIZE(tags)-1) as i
		MERGE (t:Tag {Name: replace(replace(tags[i], "<", ""), ">", "") })
		MERGE (t) -[:TAGS]->(c)
		MERGE (c) -[:TAGGED]->(t)


# borrar las Tags
MATCH (n: Tag)
DETACH DELETE n
;

# asignarlas
MATCH ( c:Question )
	WITH c AS pregunta
	UNWIND SPLIT(pregunta.Tags, "><") as tag
		WITH distinct tag
		MERGE (t:Tag {name: replace(replace(tag, "<", ""), ">", "") })
		MERGE (t)-[:TAGS]->(pregunta)<-[:TAGGED]->(t)
;

```
