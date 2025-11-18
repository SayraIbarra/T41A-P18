
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    intereses TEXT[]
);


CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    precio DECIMAL(10,2),
    etiquetas TEXT[]
);


CREATE TABLE amigos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    amigo_id INTEGER
);


CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    puesto TEXT,
    jefe_id INTEGER
);


CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    conexiones_directas INTEGER[]
);

CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    ciudad_origen INTEGER,
    ciudad_destino INTEGER,
    distancia INTEGER
);
