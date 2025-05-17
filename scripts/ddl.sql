-- Tabla de usuarios
CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL,
    contrasena TEXT NOT NULL
);

-- Tabla de notas
CREATE TABLE nota (
    id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME NOT NULL,
    categoria TEXT NOT NULL,
    enlaces TEXT,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
