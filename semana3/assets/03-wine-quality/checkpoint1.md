## Ejercicios

1. Qué campo identifica la muestra?

El campo `sample_id`.

2. ¿Qué once campos consume el modelo?

sample_id,fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,ph,sulphates,alcohol

3. Proponed una nueva columna que el contrato debería rechazar.

Va a rechazar `amount`.

4. Proponed dos valores inválidos y explicad por qué.

La primera opción es `fixed_acidity`. Un stirng supondría un dato inválido. Por otra parte, un string que no sea del tipo red-NUM también sería inválido en `sample_id`.