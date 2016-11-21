

### Primer artículo

Mostrar cómo conseguir RQ1, RQ2, RQ3 y RQ4 (tablas y gráficas) del
[artículo](http://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=2810&context=sis_research),
y ver si también se repite en Stackoverflow en español.


Basándonos en la descripción de la semántica de los campos que está disponible en: http://meta.stackexchange.com/a/2678

Podemos deducir que PostTypeId = 1 cuando se trata de una pregunta y que PostTypeId = 2 cuando se trata de una respuesta, por tanto y como ayuda hacemos esta vista:
```mysql
create view UserStats as select OwnerUserId, sum(case when PostTypeId = 1 then 1 else 0 end) as numberofquestions, sum(case when PostTypeId = 2 then 1 else 0 end) as numberofanswers from Posts group by OwnerUserId;
```


#### RQ1: What are the distributions of developers that post questions?


```mysql
select numberofquestions, count(*) as count from (select count(*) as numberofquestions from Posts where PostTypeId=1 group by OwnerUserId) t group by numberofquestions;
```

#### RQ2: What are the distributions of developers that answer questions?

```mysql
select numberofanswers, count(*) as count from (select count(*) as numberofanswers from Posts where PostTypeId=2 group by OwnerUserId) t group by numberofanswers;
```

### RQ3: Do developers that ask questions answer questions too?

```mysql

select ratioofanswers, count(*) as count from (select ceiling(numberofanswers / (numberofanswers + numberofquestions) * 100) as ratioofanswers from UserStats) t group by ratioofanswers;


```

### RQ4: Do developers receiving help returns the favor?
```mysql

create view Answerers as select parent.OwnerUserId, GROUP_CONCAT(child.OwnerUserId) as AnswerersIds from Posts parent, Posts child where parent.Id = child.ParentId and parent.PostTypeId=1 and child.PostTypeId=2 group by OwnerUserId;

```
# un desarrollador es recíproco si contesta a las preguntas de alguno de los desarrolladores que le han contestado

#incorrecto:
select OwnerUserId, exists( select * from Answerers a2 where a1.OwnerUserId in a2.AnswerersIds  ) from Answerers a1


```


### [Segundo artículo](http://flosshub.org/sites/flosshub.org/files/hicssSMFinalWatermark.pdf)

Cuando la memoria es gratis, todo se precalcula y se replica.

```mysql
	CREATE TABLE IF NOT EXISTS `new_posts_meta` (
	`Id` int(11) NOT NULL auto_increment,
	`postId` INT NOT NULL,
	`plaintext_nocode_length` INT NOT NULL,
	`plaintext_code_length` INT NOT NULL,
	`code_text_ratio` FLOAT NOT NULL,
	`score` INT NOT NULL,
	`postTypeId` INT NOT NULL,
	`favcount` INT NOT NULL
	PRIMARY KEY  (`Id`));
```


```bash
$ python --version
Python 2.7.10
$ python UpdateScriptSize.py
```` 

#### Q1. Do higher scoring questions include more source code? What about higher scoring answers?

```mysql
select code_text_ratio, Score from new_posts_meta inner join Posts on Posts.Id = new_posts_meta.postId limit 10;
```

```mysql

select ceil(count(*) * 0.05) from new_posts_meta where PostTypeId = 1;
/* 352 */

select avg(code_text_ratio) from (select code_text_ratio from new_posts_meta where postTypeId = 1 order by Score desc limit 352) t;
/* el 5% de las consultas con más puntuación tienen una proporción de código de 0.331561081944859 */

select avg(code_text_ratio) from new_posts_meta where postTypeId = 1;
/* la media de la relación es de: 0.3695720485178994 */


select ceil(count(*) * 0.05) from new_posts_meta where PostTypeId = 2;
/* 447 */

select avg(code_text_ratio) from (select code_text_ratio from new_posts_meta where postTypeId = 2 order by Score desc limit 352) t;
/* el 5% de las consultas con más puntuación tienen una proporción de código de 0.31454946994331706 */

select avg(code_text_ratio) from new_posts_meta where postTypeId = 2;
/* la media de la relación es de: 0.3902041476015976 */


```
La conclusión es que no en ninguno de los dos casos.


#### Q2. Do questions with high favorite counts have more source code?




#### Q3. Do answers chosen as “accepted answers” have more source code than answers not chosen?



#### (opcional) El tiempo mínimo y máximo que pasa entre cada pregunta y la primera respuesta (función TIMESTAMPDIFF() de MySQL).



#### (opcional) Usando la tabla PostTags de la sesión anterior, calcular el tiempo medio, mínimo y máximo de la primera respuesta dependiendo del Tag.

<!--
C1:

select count(*) as number_of_users, times.count from (select count(*) as count from Posts where PostTypeId = 1 group by OwnerUserId) times group by count;

C2:
select count(*) as number_of_users, times.count from (select count(*) as count from Posts where PostTypeId = 2 group by OwnerUserId) times group by count;

C3:
select * from (select distinct OwnerUserId from Posts where PostTypeId = 1) as Questioners left join (select distinct OwnerUserId from Posts where PostTypeId = 2) as Answerers

insert into new_posts_meta_2 (postId, code_text_ratio, Score, rank, percentile, postNumber, prevScore)

select PostId, code_text_ratio, Score, @curRank := IF(@prevVal=Score, @curRank, @postNumber) AS rank, 
@percentile := IF(@prevVal=Posts.Score, @percentile, (@totalPosts - @postNumber + 1)/(@totalPosts)*100) as percentile,
@postNumber := @postNumber + 1 as postNumber, 
@prevVal:=Posts.Score
from new_posts_meta inner join Posts on Posts.Id = new_posts_meta.postId, (
SELECT @curRank :=0, @prevVal:=null, @postNumber:=1, @percentile:=100
) r
where PostTypeId = 1
ORDER BY Posts.Score DESC;

-->

