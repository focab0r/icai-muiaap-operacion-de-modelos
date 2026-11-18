
# Soluciones para la Semana 9 clase 01

## M1

1. El campo que aparece en `leaky` y no en `public` es `threshold_config`
2. Porque utiliza `response_model`, que filtra aquellos campos no especificados en `PublicScore`.
3. Sí, aparece

## M2

- `{"age": 30, "income": 1000}`

| -       | /v1/scores | /v1/nada  | /v1/boom   |
|---------|------------|-----------|------------|
| status  | 200        | 404       | 405        |
| code    | -          | not_found | http_error |
| fields  | -          | -         | -          |

- `{"age": "treinta", "income": 1000}`

| -       | /v1/scores       | /v1/nada  | /v1/boom   |
|---------|------------------|-----------|------------|
| status  | 422              | 404       | 405        |
| code    | validation_error | not_found | http_error |
| fields  | age              | -         | -          |

- `{"age": 30}`

| -       | /v1/scores       | /v1/nada  | /v1/boom   |
|---------|------------------|-----------|------------|
| status  | 200              | 404       | 405        |
| code    | validation_error | not_found | http_error |
| fields  | income           | -         | -          |

2. Si comentas el decorador de `handle_validation`, se devuelve el error de la apicación, lo cual puede ser peligroso porque da información innecesaria del sistema.

## M3

Hecho, se ha modificado el archivo correspondiente y el de test.

## M4

2. Lo que hace es activar los errores del servidor. Cuando sucede uno de ellos, el servidor crashea.
3. Se ha añadido la función