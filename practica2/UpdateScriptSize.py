import mysql.connector
from CodeCount import CodeCount

"""
	CREATE TABLE IF NOT EXISTS `postStats` (
	`Id` int(11) NOT NULL auto_increment,
	`postId` INT NOT NULL,
	`codeLength` INT NOT NULL,
	`length` INT NOT NULL, PRIMARY KEY  (`Id`));

"""

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='stackoverflow')


cursor = cnx.cursor()

query = ("SELECT Id, Body, Score, PostTypeId, FavoriteCount FROM Posts WHERE Id not in (select postId from new_posts_meta)")


cursor.execute(query)

p = [] 

for (id, body, score, postTypeId, favCount) in cursor:
	c = CodeCount()
	body = unicode(body)
	c.run(body)
	
	ratio = 0
	if (c.nocode_length + c.code_length >0):
		ratio = c.code_length / float(c.nocode_length + c.code_length )

	row = []
	row.append(id)
	row.append(c.nocode_length)
	row.append(c.code_length)
	row.append(ratio)
	row.append(score)
	row.append(postTypeId)
	row.append(favCount)

	p.append( row )
	

cq = cnx.cursor()
insertquery = ("insert into new_posts_meta (postId, plaintext_nocode_length, plaintext_code_length, code_text_ratio, score, postTypeId, favCount) values (%s,%s,%s,%s,%s,%s,%s)")
cq.executemany(insertquery, p)
cq.close()

cursor.close()

cnx.commit()


cnx.close()

