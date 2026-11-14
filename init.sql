-- La base de datos se pobla automaticamente por medio del docker-compose.yml

CREATE DATABASE IF NOT EXISTS Regalos
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE Regalos;

DROP VIEW  IF EXISTS vista_cartas_resumen;
DROP TABLE IF EXISTS detalles_carta;
DROP TABLE IF EXISTS duendes;
DROP TABLE IF EXISTS cartas;
DROP TABLE IF EXISTS regalos;
DROP TABLE IF EXISTS ninos;


CREATE TABLE ninos (
  id_nino              INT AUTO_INCREMENT PRIMARY KEY,
  nombre               VARCHAR(100) NOT NULL,
  direccion            VARCHAR(255) NOT NULL,
  pais                 VARCHAR(80)  NOT NULL,
  puntos_comportamiento INT NOT NULL DEFAULT 0,
  lista                ENUM('lista_buena', 'lista_mala')
                       GENERATED ALWAYS AS (
                         CASE WHEN puntos_comportamiento >= 50
                              THEN 'lista_buena' ELSE 'lista_mala' END
                       ) STORED
) ENGINE=InnoDB;


CREATE TABLE regalos (
  id_regalo                       INT AUTO_INCREMENT PRIMARY KEY,
  nombre                          VARCHAR(100) NOT NULL,
  descripcion                     TEXT,
  categoria_juguete               VARCHAR(60) NOT NULL,
  puntos_comportamiento_requeridos INT NOT NULL DEFAULT 0,
  CONSTRAINT chk_puntos_req CHECK (puntos_comportamiento_requeridos >= 0)
) ENGINE=InnoDB;


CREATE TABLE cartas (
  id_carta           INT AUTO_INCREMENT PRIMARY KEY,
  id_nino            INT NOT NULL,
  fecha_recepcion    DATE NOT NULL DEFAULT (CURRENT_DATE),
  estado_preparacion ENUM('recibida', 'en_taller', 'cargada_en_trineo')
                     NOT NULL DEFAULT 'recibida',
  CONSTRAINT fk_cartas_nino
    FOREIGN KEY (id_nino) REFERENCES ninos(id_nino)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE detalles_carta (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  id_carta   INT NOT NULL,
  id_regalo  INT NOT NULL,
  cantidad   INT NOT NULL DEFAULT 1,
  CONSTRAINT chk_cantidad CHECK (cantidad > 0),
  CONSTRAINT uq_carta_regalo UNIQUE (id_carta, id_regalo),
  CONSTRAINT fk_detalles_carta
    FOREIGN KEY (id_carta)  REFERENCES cartas(id_carta)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_detalles_regalo
    FOREIGN KEY (id_regalo) REFERENCES regalos(id_regalo)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;


CREATE TABLE duendes (
  id_duende         INT AUTO_INCREMENT PRIMARY KEY,
  nombre            VARCHAR(100) NOT NULL,
  especialidad      ENUM('carpintero', 'electronica', 'empaque') NOT NULL,
  id_carta_asignada INT NULL,
  CONSTRAINT fk_duendes_carta
    FOREIGN KEY (id_carta_asignada) REFERENCES cartas(id_carta)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

-- Indices utiles
CREATE INDEX idx_cartas_nino   ON cartas(id_nino);
CREATE INDEX idx_cartas_estado ON cartas(estado_preparacion);
CREATE INDEX idx_duendes_carta ON duendes(id_carta_asignada);

CREATE VIEW vista_cartas_resumen AS
SELECT c.id_carta,
       n.nombre AS nino,
       n.pais,
       n.lista,
       c.fecha_recepcion,
       c.estado_preparacion,
       COALESCE(SUM(d.cantidad), 0) AS total_regalos
FROM cartas c
JOIN ninos n            ON n.id_nino = c.id_nino
LEFT JOIN detalles_carta d ON d.id_carta = c.id_carta
GROUP BY c.id_carta, n.nombre, n.pais, n.lista, c.fecha_recepcion, c.estado_preparacion;


INSERT INTO ninos (nombre, direccion, pais, puntos_comportamiento) VALUES
  ('Manuel Manitas',  'Carretera a Aeropuerto de Guaymas 870-Km 3, Guaymas',     'Mexico',    90),
  ('Manolo Manitas',   'Carretera a Aeropuerto de Guaymas 870-Km 3, Guaymas',    'Mexico',   35),
  ('Emma Emmerald',   '742 Evergreen Terrace',      'EE.UU.',    75);

INSERT INTO regalos (nombre, descripcion, categoria_juguete, puntos_comportamiento_requeridos) VALUES
  ('Bicicleta roja',   'Bicicleta infantil con rueditas',   'exterior',    60),
  ('Robot armable',    'Kit de robot con motores',          'electronica', 50),
  ('Casa de munecas',  'Casa de madera con muebles',        'munecas',     40),
  ('Carro de carreras','Auto a control remoto',             'vehiculos',   20);

INSERT INTO cartas (id_nino, fecha_recepcion, estado_preparacion) VALUES
  (1, '2026-11-01', 'en_taller'),
  (2, '2026-11-05', 'recibida'),
  (3, '2026-11-10', 'recibida');

INSERT INTO detalles_carta (id_carta, id_regalo, cantidad) VALUES
  (1, 1, 1),
  (1, 3, 1),
  (2, 4, 1),
  (3, 2, 1);

INSERT INTO duendes (nombre, especialidad, id_carta_asignada) VALUES
  ('Pipo',   'carpintero',  1),
  ('Tuli',   'electronica', 3),
  ('Nieve',  'empaque',     NULL);