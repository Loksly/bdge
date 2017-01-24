

### RQ1:

#### Framework de agregación:

```mongodb
db.posts.aggregate([
	{$match: { PostTypeId: 1} },
	{$group: {_id: "$OwnerUserId", count:{$sum: 1}  }},
	{$group: { _id: "$count", howmany: {$sum: 1}}}
]);
```

#### Map/Reduce:

```mongodb
db.rq1_.drop();
db.rq1.drop();
db.posts.mapReduce(
	function(){
		emit(this.OwnerUserId, 1);
	},
	function(key, values){
		return Array.sum(values);
	},
	{
		query:{ PostTypeId: 1 },
		out: "rq1_"
	}
);
db.rq1_.mapReduce(
	function(){
		emit(this.value, 1);
	},
	function(key, values){
		return Array.sum(values);
	},
	{
		out: "rq1"
	}
);
db.rq1_.drop();
```

### RQ2:

#### Framework de agregación:

```mongodb
db.posts.aggregate([
	{$match: { PostTypeId: 2} },
	{$group: {_id: "$OwnerUserId", count:{$sum: 1}  }},
	{$group: { _id: "$count", howmany: {$sum: 1}}}
]);
```

#### Map/Reduce:
```mongodb
db.rq2_.drop();
db.rq2.drop();
db.posts.mapReduce(
	function(){
		emit(this.OwnerUserId, 1);
	},
	function(key, values){
		return Array.sum(values);
	},
	{
		query:{ PostTypeId: 2 },
		out: "rq2_"
	}
);
db.rq2_.mapReduce(
	function(){
		emit(this.value, 1);
	},
	function(key, values){
		return Array.sum(values);
	},
	{
		out: "rq1"
	}
);
db.rq2_.drop();
```


### RQ3:

### Framework de agregación:

```mongodb
db.posts.aggregate([
	{
		'$match':
			{ 'PostTypeId': { '$in': [1, 2] } } },
	{
		'$group': {
			_id: "$OwnerUserId",
			'numPreguntas': {'$sum': { '$mod': ["$PostTypeId", 2] } } ,
			'numRespuestas': {'$sum': { '$ceil': {'$divide': ['$PostTypeId', 2] } } }
		}
	},
	{
		'$project': {
			'percentQuestions': {
				'$ceil':
					{
						$multiply: [
						100,
							{ $divide: ['$numRespuestas', {'$add': ['$numPreguntas', '$numRespuestas'] }  ] }
						]
					}
				}
		}
	},
	{$group: { _id: "$percentQuestions", howmany: {$sum: 1}}}
]);

```


#### Map/Reduce:

```mongodb
db.rq3_.drop();
db.rq3.drop();
db.posts.mapReduce(
    function(){
        var obj = {
            numPreguntas: (this.PostTypeId === 1) ? 1 : 0,
            numRespuestas: (this.PostTypeId === 2) ? 1 : 0
        };

        emit(this.OwnerUserId, obj);
    },
    function(key, values){
        var obj = {
            numPreguntas: 0,
            numRespuestas: 0
        };
        for(var i = 0, j = values.length; i < j; i++){
            obj.numPreguntas += values[i].numPreguntas;
            obj.numRespuestas += values[i].numRespuestas; 
        }
    },
    {
        query:{ PostTypeId: { $in: [1, 2] } },
        out: "rq3_",
        finalize: function(key, value){
            var numPreguntasYRespuestas = value.numPreguntas + value.numRespuestas;
            return Math.ceil(100 * value.numPreguntas / numPreguntasYRespuestas);
        }
    }
);
db.rq3_.mapReduce(
    function(){
        emit(this.value, 1);
    },
    function(key, values){
        return Array.sum(values);
    },
    {
        out: "rq3"
    }
);
```
