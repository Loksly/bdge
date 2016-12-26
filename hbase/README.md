# HBASE


### Shell de hbase

El shell de hbase nos permite la ejecución de comandos sobre el gestor de la base de datos utilizando el propio cliente de línea
de comandos proporcionado por hbase. Para entrar en el shell de _hbase_ tan sólo es necesario ejecutar:

```bash
$ hbase/bin/hbase
```

## Ejercicios


### Mostrar la familia de columnas revision para la entrada ASCII de la tabla wikipedia.
```hbase
hbase> get 'wikipedia', 'ASCII', {COLUMN => 'revision',VERSIONS=>10}
```

### Mostrar las 20 primeras filas de la tabla wikipedia cuyas columnas empiecen por com.

Creo que te refieres a esto:

```hbase
hbase> scan 'wikipedia', {FILTER =>"ColumnPrefixFilter('com')",  LIMIT => 20}
```

Y no a esto:

```hbase
hbase> scan 'wikipedia', {STARTROW => 'com', FILTER => "PrefixFilter('com')",  LIMIT => 20}
```
 
### Mostrar las 20 primeras filas de la tabla wikipedia cuyas columnas empiecen por com y la clave de columna empieza por 'B'.

```hbase
hbase> scan 'wikipedia', {ROWPREFIXFILTER => 'B', FILTER => "ColumnPrefixFilter('com')",  LIMIT => 20}
```
 
### Mostrar sólo la columna revision:author de las filas de la tabla wikipedia cuya clave empiece por a y termine por a (obviando mayúsculas y minúsculas).
```hbase
hbase> scan 'wikipedia', {COLUMNS=>'revision',  FILTER => "PrefixFilter('A')"}
```
 
### Mostrar las filas de la tabla wikipedia cuya clave contenga al menos un número.
```hbase
hbase> scan 'wikipedia', {FILTER => "RowFilter(=,'regexstring:[0-9])"}
```
 
### Mostrar las filas de la tabla wikipedia cuyo autor de revisión sea Addbot.
```hbase
hbase> scan 'wikipedia', {FILTER=>"SingleColumnValueFilter('revision', 'author', =, 'binary:Addbot')"}
```
 
### Mostrar las filas de la tabla wikipedia tales que alguno de sus valores de campos de columnas sea menor que 1.
```hbase
hbase> scan 'wikipedia', {FILTER=>"ValueFilter(<, 'binary:1')",  LIMIT => 20}
```
 
### Mostrar las filas de la tabla users (sólo la columna rawdata:Location) de usuarios de España (se supondrá que su localización (columna rawdata:Location) contiene España o ES, obviando mayúsculas y minúsculas).
```hbase
hbase> scan 'users', {FILTER=>"SingleColumnValueFilter('rawdata','Location',=,'substring:ES')"}
```

Otra opción:

```hbase
hbase> scan 'users', {FILTER=>"SingleColumnValueFilter('rawdata','Location',=,'binary:Spain') OR SingleColumnValueFilter('rawdata','Location',=,'binary:España')"}
```
 
### Comparar si hay más usuarios de Santiago de Compostela que de Murcia :).
```hbase
hbase> scan 'users', {FILTER=>"SingleColumnValueFilter('rawdata','Location',=,'substring:Murcia')"}
```

```hbase
hbase> scan 'users', {FILTER=>"SingleColumnValueFilter('rawdata','Location',=,'substring:Santiago de Compostela')"}
```

Murcia: 11
Santiago de Compostela: 5
 
### Mostrar las filas de la tabla posts que hacen referencia al tag "clojure".

```hbase
hbase> scan 'posts', {FILTER=>"SingleColumnValueFilter('rawdata','Tags',=,'substring:<clojure>')"}
```
 
### (opcional): Crear una nueva tabla _poststags_ que, de forma eficiente, para cada tag, liste los Id de los posts que utilizan ese tag.


[Source shell commands](https://learnhbase.wordpress.com/2013/03/02/hbase-shell-commands/)
