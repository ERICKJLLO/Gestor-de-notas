# Gestor de Notas

El objetivo de este proyecto es desarrollar una aplicación para la gestión de notas personales y
profesionales. Las funcionalidades que la aplicación debe tener son:

1. Crear una nota: La aplicación debe permitir a los usuarios crear una nota en el sistema
2. Editar una nota: La aplicación debe permitir a los usuarios editar una nota existente en
el sistema
3. Eliminar una nota: La aplicación debe permitir a los usuarios eliminar una nota
existente en el sistema
4. Iniciar sesión: La aplicación debe permitir a los usuarios iniciar sesión en el sistema con
un usuario ya existente
5. Crear cuenta: Los usuarios deben poder darse de alta en el sistema
6. Cambiar contraseña: El sistema debe permitir a los usuarios cambiar sus contraseñas
cuando ellos lo deseen.

Una nota debe estar compuesta por los siguientes datos:

1. El título de la nota
2. El contenido de la nota
3. Fecha de creación de la nota
4. Categoría de la nota
5. Enlaces a otras notas

**Nota**:Cada usuario al crear su cuenta e iniciar sesión debe poder ver sus notas y solo sus notas, no
las notas creadas por los otros usuarios.

## Diagrama de Clases

![alt text](assets/DiagramaUML.drawio.png)

## Pruebas Implementadas

A continuación, se presentan las pruebas organizadas por funcionalidad y tipo de prueba.

### **1. Crear Nota**

Pruebas Normales

| #  | Descripción                             | Datos de entrada                          | Resultado esperado |
|----|-----------------------------------------|-------------------------------------------|--------------------|
| 1  | Crear una nota con datos válidos        | Título: "Trabajo", Contenido: "Pendiente" | Nota creada        |
| 2  | Crear una nota con categoría específica | Categoría: "Personal"                     | Nota creada        |
| 3  | Crear una nota con caracteres normales  | Título: "Tarea", Contenido: "Matemáticas" | Nota creada        |

Pruebas Extremas

| #  | Descripción                          | Datos de entrada       | Resultado esperado |
|----|--------------------------------------|------------------------|--------------------|
| 4  | Crear nota con título largo          | Título: 200 caracteres | Nota creada        |
| 5  | Crear nota con título vacío          | Título: ""             | Nota creada        |
| 6  | Crear nota con caracteres especiales | Título: "@#*!"         | Nota creada        |

Pruebas de Error

| #  | Descripción                        | Datos de entrada               | Resultado esperado        |
|----|------------------------------------|--------------------------------|---------------------------|
| 7  | Crear nota sin título ni contenido | Título: "", Contenido: ""      | Lanza `CamposVaciosError` |
| 8  | Crear nota duplicada               | Título: "Trabajo" ya existente | Lanza `NotaYaExisteError` |
| 9  | Crear nota sin usuario             | Usuario: None                  | Lanza `CamposVaciosError` |

### **2. Editar Nota**

Pruebas Normales

| #  | Descripción                  | Datos de entrada                     | Resultado esperado |
|----|------------------------------|--------------------------------------|--------------------|
| 10 | Editar título de una nota    | Nuevo título: "Nuevo Titulo"         | Nota editada       |
| 11 | Editar contenido de una nota | Nuevo contenido: "Texto Actualizado" | Nota editada       |
| 12 | Editar categoría de una nota | Nueva categoría: "Importante"        | Nota editada       |

Pruebas Extremas

| #  | Descripción                           | Datos de entrada       | Resultado esperado |
|----|---------------------------------------|------------------------|--------------------|
| 13 | Editar nota con título largo          | Título: 200 caracteres | Nota editada       |
| 14 | Editar nota con título vacío          | Título: ""             | Nota editada       |
| 15 | Editar nota con caracteres especiales | Título: "#$@!"         | Nota editada       |

Pruebas de Error

| #  | Descripción                     | Datos de entrada              | Resultado esperado            |
|----|---------------------------------|-------------------------------|-------------------------------|
| 16 | Editar nota inexistente         | Índice: 5 (no existe)         | Lanza `NotaNoEncontradaError` |
| 17 | Editar nota con datos inválidos | Título: None, Contenido: None | Lanza `EdicionInvalidaError`  |
| 18 | Editar nota sin usuario         | Usuario: None                 | Lanza `NotaNoEncontradaError` |

### **3. Eliminar Nota**

Pruebas Normales

| #  | Descripción                         | Datos de entrada | Resultado esperado |
|----|-------------------------------------|------------------|--------------------|
| 19 | Eliminar una nota existente         | Índice: 0        | Nota eliminada     |
| 20 | Agregar varias notas y eliminar una | Índice: 1        | Nota eliminada     |
| 21 | Eliminar última nota de la lista    | Índice: -1       | Nota eliminada     |

Pruebas Extremas

| #  | Descripción                          | Datos de entrada    | Resultado esperado |
|----|--------------------------------------|---------------------|--------------------|
| 22 | Eliminar una nota con título largo   | Índice: 0           | Nota eliminada     |
| 23 | Eliminar una nota con título vacío   | Índice: 1           | Nota eliminada     |
| 24 | Eliminar todas las notas una por una | Índices: 0, 1, 2... | Notas eliminadas   |

Pruebas de Error

| #  | Descripción                                    | Datos de entrada | Resultado esperado               |
|----|------------------------------------------------|------------------|----------------------------------|
| 25 | Intentar eliminar una nota inexistente         | Índice: 10       | Lanza `NotaNoEncontradaError`    |
| 26 | Intentar eliminar una nota de otro usuario     | Índice: 0        | Lanza `EliminacionInvalidaError` |
| 27 | Intentar eliminar una nota sin sesión iniciada | Índice: 0        | Lanza `EliminacionInvalidaError` |

### **4. Iniciar Sesión**

Pruebas Normales

| #  | Descripción                                       | Datos de entrada                             | Resultado esperado |
|----|---------------------------------------------------|----------------------------------------------|--------------------|
| 28 | Iniciar sesión con usuario y contraseña correctos | Usuario: "usuario1", Contraseña: "password1" | Inicio exitoso     |
| 29 | Iniciar sesión con usuario recién creado          | Usuario: "nuevo", Contraseña: "clave123"     | Inicio exitoso     |
| 30 | Iniciar sesión y verificar usuario                | Usuario: "usuario2", Contraseña: "pass456"   | Inicio exitoso     |

Pruebas Extremas

| #  | Descripción                              | Datos de entrada                       | Resultado esperado |
|----|------------------------------------------|----------------------------------------|--------------------|
| 31 | Iniciar sesión con nombre largo          | Usuario: 50 caracteres                 | Inicio exitoso     |
| 32 | Iniciar sesión con caracteres especiales | Usuario: "@user#", Contraseña: "p@ss!" | Inicio exitoso     |
| 33 | Iniciar sesión con contraseña larga      | Contraseña: 100 caracteres             | Inicio exitoso     |

Pruebas de Error

| #  | Descripción                              | Datos de entrada                             | Resultado esperado                 |
|----|------------------------------------------|----------------------------------------------|------------------------------------|
| 34 | Iniciar sesión con contraseña incorrecta | Usuario: "usuario1", Contraseña: "wrongpass" | Lanza `CredencialesInvalidasError` |
| 35 | Iniciar sesión con usuario inexistente   | Usuario: "desconocido"                       | Lanza `UsuarioNoEncontradoError`   |
| 36 | Iniciar sesión con campos vacíos         | Usuario: "", Contraseña: ""                  | Lanza `CamposVaciosError`          |

### **5. Crear Cuenta**

Pruebas Normales

| #  | Descripción                                | Datos de entrada                             | Resultado esperado |
|----|--------------------------------------------|----------------------------------------------|--------------------|
| 37 | Registrar un nuevo usuario                 | Usuario: "usuario2", Contraseña: "password2" | Registro exitoso   |
| 38 | Registrar un usuario con contraseña válida | Usuario: "user123", Contraseña: "securepass" | Registro exitoso   |
| 39 | Registrar un usuario con nombre corto      | Usuario: "aa", Contraseña: "clave123"        | Registro exitoso   |

Pruebas Extremas

| #  | Descripción                                    | Datos de entrada                       | Resultado esperado |
|----|------------------------------------------------|----------------------------------------|--------------------|
| 40 | Registrar un usuario con nombre largo          | Usuario: 100 caracteres                | Registro exitoso   |
| 41 | Registrar un usuario con caracteres especiales | Usuario: "@user!", Contraseña: "$p@ss" | Registro exitoso   |
| 42 | Registrar un usuario con nombre vacío          | Usuario: "", Contraseña: "password"    | Registro exitoso   |

Pruebas de Error

| #  | Descripción                          | Datos de entrada                | Resultado esperado           |
|----|--------------------------------------|---------------------------------|------------------------------|
| 43 | Registrar un usuario duplicado       | Usuario: "usuario1"             | Lanza `UsuarioYaExisteError` |
| 44 | Registrar un usuario sin contraseña  | Usuario: "user", Contraseña: "" | Lanza `CamposVaciosError`    |
| 45 | Registrar un usuario con datos nulos | Usuario: None, Contraseña: None | Lanza `CamposVaciosError`    |

### **6. Cambiar Contraseña**

Pruebas Normales

| #  | Descripción                                  | Datos de entrada             | Resultado esperado |
|----|----------------------------------------------|------------------------------|--------------------|
| 46 | Cambiar la contraseña de un usuario          | Contraseña: "nueva_password" | Cambio exitoso     |
| 47 | Cambiar contraseña y verificar               | Contraseña: "segura123"      | Cambio exitoso     |
| 48 | Cambiar contraseña y volver a iniciar sesión | Contraseña: "clave_456"      | Cambio exitoso     |

Pruebas Extremas

| #  | Descripción                                  | Datos de entrada           | Resultado esperado |
|----|----------------------------------------------|----------------------------|--------------------|
| 49 | Cambiar contraseña a una larga               | Contraseña: 100 caracteres | Cambio exitoso     |
| 50 | Cambiar contraseña con caracteres especiales | Contraseña: "Pa$$w0rd!@#"  | Cambio exitoso     |
| 51 | Cambiar contraseña a una muy corta           | Contraseña: "x"            | Cambio exitoso     |

Pruebas de Error

| #  | Descripción                                  | Datos de entrada     | Resultado esperado               |
|----|----------------------------------------------|----------------------|----------------------------------|
| 52 | Cambiar contraseña vacía                     | Contraseña: ""       | Lanza `ContrasenaInvalidaError`  |
| 53 | Cambiar contraseña de un usuario inexistente | Usuario: "no_existe" | Lanza `UsuarioNoEncontradoError` |
| 54 | Cambiar contraseña a `None`                  | Contraseña: None     | Lanza `ContrasenaInvalidaError`  |
