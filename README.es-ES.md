

Biblioteca de Python para la API de Information Tracer
----------------------------

Este repositorio de GitHub proporciona scripts en Python para interactuar con la API de Information Tracer.
Information Tracer es un sistema para recopilar publicaciones de redes sociales y generar inteligencia.


### Requisitos previos 
- Python 3
- Debes tener un token válido. Si no lo tienes, contáctanos para obtener uno.

### Descripción de nuestros diferentes endpoints de la API
1. Utiliza la API de Submit para enviar una consulta y obtener un identificador único llamado `id_hash256`
2. Utiliza la API de Status para verificar el estado de una consulta en ejecución, basándote en `id_hash256`
3. Utiliza el Endpoint de Download para obtener el resultado de una consulta, basándote en `id_hash256`

### Inicio rápido
1. Cierra este repositorio
2. `pip install requests pandas`
3. Actualiza los parámetros en [example.py](https://github.com/zhouhanc/informationtracer/blob/main/example.py), incluyendo query, start_date, end_date, token 
4. `informationtracer_token=XXX python example.py` (o añade `informationtracer_token` en bash_profile)


### Cómo construir una consulta de búsqueda

Regla 1: `AND`, `OR`, `NOT` deben estar en mayúsculas. De lo contrario, se tratarán como palabras normales en inglés.
Regla 2: Utiliza paréntesis para agrupar múltiples palabras con AND. Por ejemplo, `(Word1 AND Word2)`.
Regla 3: El límite de la consulta es de 512 caracteres. Enviar una consulta por encima del límite podría devolver resultados vacíos.

Ejemplo: `(Ukraine AND NATO) OR (Ukraine AND EU)`
Significado: Cualquier publicación que contenga "Ukraine" y "NATO" o "Ukraine" y "EU".

Ejemplo: `(Ukraine AND NATO) NOT Putin`
Significado: Cualquier publicación que contenga "Ukraine" y "NATO", sin la palabra "Putin".

Ejemplo: `from:elonmusk`
Significado: Recopila tweets creados por el usuario @elonmusk.

Ejemplo: `from:elonmusk Tesla`
Significado: Recopila tweets creados por el usuario @elonmusk, y con la palabra "tesla".


### Detalles sobre la API de Submit
Entrada: `query`, `token`, `start_date`, `end_date`

Entrada opcional: 
`twitter_sort_by`: 'time' o 'engagement' (el valor predeterminado es 'engagement', si no se especifica)
 - establece `twitter_sort_by` en 'time' para recopilar tweets en orden cronológico inverso (del más reciente al más antiguo).
 - establece `twitter_sort_by` en 'engagement' para recopilar tweets en orden inverso de la cantidad de likes.

Salida: `id_hash256` (un identificador de cadena único para esta búsqueda).

Ejemplo:
```python
import requests
SUBMIT_URL = 'https://informationtracer.com/submit'

query = 'nvidia AND stock'
token = 'YOUR_TOKEN'
start_date = '2023-11-03'
end_date = '2023-11-08'

response = requests.post(SUBMIT_URL, 
                             timeout=10,
                             json={'query': query, 
                                   'token': token,
                                   'start_date': start_date,
                                   'end_date': end_date,
                                   'twitter_sort_by': 'engagement'
                                   }                                   
                            )
if 'id_hash256' in response.json():
    id_hash256 = response.json()['id_hash256']
```


### Detalles sobre la API de Status
Entrada: `id_hash256`, `token`
Salida: json (detalle a continuación).

Ejemplo:
```python
import requests
STATUS_URL = 'https://informationtracer.com/status'

url = "{}?token={}&id_hash256={}".format(STATUS_URL, token, id_hash256)
results = requests.get(url).json()
```

__Formato de la salida__
Dado que cada recopilación puede tardar de 30 a 60 segundos, para enviar resultados parciales a los usuarios lo antes posible, proporcionamos un campo llamado `tweet_preview`. Este campo está inicialmente vacío. Cuando el sistema ha recopilado 10 tweets, `tweet_preview` contendrá una lista de diccionarios. Consulta los [detalles de la API de resultados v1](/result-api-old.md) para una explicación detallada de cada par clave-valor (`d`, `i`, `l`, ...).
```
{'status': 'started', 
 'status_percentage': '10', 
 'status_text': 'Collecting cross-platform posts...', 
 'tweet_preview': [{'d': '@Apple Unless you buy a MacBook circa 2010',
                    'i': 0, 
                    'l': 'https://twitter.com/heathdollars/status/1721998289388896312', 'n': 'heathdollars', 
                    'p': 'https://pbs.twimg.com/profile_images/1641987731181142018/tECQ8Xy1_normal.jpg', 
                    't': '2023-11-07T21:09:20', 
                    'u_d': 'join your union\n\nhttps://t.co/4sxV02E2aI', 
                    'u_id': '1000720137106866176', 
                    'u_t': '2018-05-27T12:47:27'
                    }, 
                    {...}, 
                    {...}, 
                    ...
                   ]
}
```

### API de resultados (nueva, por plataforma)
Entrada (requerida): `source`, `id_hash256`, `token`

`source` es la fuente de datos, que puede ser 'twitter', 'youtube', 'reddit', 'all'.

__Formato de la salida__
Salida: un dataframe de pandas, que se puede convertir a csv, json, etc.
- Las columnas deberían ser autoexplicativas.
- Ten en cuenta que algunas columnas (aquellas con el prefijo `country_`, `sentiment_` , `account_type_` ) solo están disponibles para usuarios premium.

```python
import pandas as pd
url = 'https://informationtracer.com/download?source={}&type=csv&id={}&token={}'.format(source, id_hash256, token)
df = pd.read_csv(url)
```


### API de resultados (v1, obsoleta)
[Detalles de la API de resultados v1](/result-api-old.md).


### Interfaz web
- Para ayudar a las personas a visualizar la información, proporcionamos una interfaz web disponible en [https://informationtracer.com](https://informationtracer.com). 
- Para visualizar una consulta que has realizado recientemente, puedes visitar `https://informationtracer.com/?result={id_hash256}`. 
- Se requiere iniciar sesión. Contáctanos y te ayudaremos a registrar una cuenta.

### Contacto / Reporte de errores
Para reportar errores o cualquier consulta, por favor contacta a Zhouhan Chen zhouhan@safelink.network.
