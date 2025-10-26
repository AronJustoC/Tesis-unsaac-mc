# Capítulo 3: Fabricación del Modelo a Escala del Puente Bailey

## 3.1 Introducción

El proceso de fabricación del modelo a escala del puente Bailey requiere una metodología rigurosa que garantice la precisión dimensional y la funcionalidad mecánica del conjunto. La característica modular del diseño original se mantiene mediante un sistema de componentes estandarizados que se interconectan a través de uniones mecánicas desmontables, replicando a escala las especificaciones técnicas del puente real.

## 3.2 Metodología de Fabricación

### 3.2.1 Consideraciones de Diseño para Manufactura (DFM)

- Selección de tolerancias dimensionales
  - Se implementan las tolerancias según normas ISO 2768-m para tolerancias generales
  - Tolerancias específicas críticas según ISO 286-1 para ajustes de precisión
  - Rugosidad superficial según ISO 1302 para superficies de contacto
- Análisis de procesos de manufactura disponibles
  - Evaluación de capacidades de máquinas CNC disponibles
  - Análisis de precisión alcanzable en procesos de corte
  - Selección de procesos según complejidad geométrica
- Optimización de geometrías para fabricación
  - Simplificación de formas manteniendo funcionalidad
  - Estandarización de elementos repetitivos
  - Consideraciones para minimizar desperdicios

### 3.2.2 Planificación del Proceso

1. Modelado CAD/CAM

   - Desarrollo de modelos 3D paramétricos en SolidWorks
     El modelado tridimensional del puente Bailey se realizó utilizando SolidWorks 2023, aplicando una escala 1:10 y respetando las especificaciones técnicas del manual militar FM 5-277. Se inició con el modelado de los componentes estructurales principales:

     - Paneles laterales tipo Bailey M2
     - Vigas transversales de soporte
     - Sistemas de arriostramiento y rigidización
     - Conectores y elementos de unión

     Para cada componente se establecieron las relaciones paramétricas que garantizan:

     - Intercambiabilidad entre módulos
     - Tolerancias dimensionales según ISO 2768-m
     - Ajustes según sistema ISO de tolerancias
       [Insertar figura 3.1: Modelo 3D del panel Bailey]

   - Generación de planos de fabricación
     Los planos se desarrollaron siguiendo la norma ISO 128-1:2020 para dibujo técnico, incluyendo:

     - Vistas principales y auxiliares
     - Detalles constructivos y de unión
     - Tablas de materiales y especificaciones
     - Tolerancias geométricas según ISO 1101
       [Insertar figura 3.2: Plano de fabricación del panel]

   - servicio de corte CNC
     Se generaron los planos de trayectoria para corte láser, elaboracion propia mientras que el resto se paso lo realizo el servicio externo:
     - Trayectorias de corte
     - Velocidades de avance
     - Potencia del láser según espesor
     - Secuencia de mecanizado

2. Selección de procesos de manufactura

   - Matriz de decisión para procesos críticos
     Se evaluaron los siguientes criterios (1-5):

     | Proceso         | Precisión | Costo | Tiempo | Acabado | Total |
     | --------------- | --------- | ----- | ------ | ------- | ----- |
     | Corte láser CNC | 5         | 3     | 4      | 5       | 17    |
     | Corte plasma    | 3         | 4     | 3      | 3       | 13    |
     | Corte mecánico  | 2         | 5     | 2      | 2       | 11    |

     Para soldadura:

     | Proceso | Control | Costo | Resist. | Acabado | Total |
     | ------- | ------- | ----- | ------- | ------- | ----- |
     | MIG     | 4       | 4     | 5       | 4       | 17    |
     | Punto   | 3       | 3     | 3       | 3       | 12    |
     | TIG     | 5       | 2     | 5       | 5       | 17    |
     | Arco    | 3       | 5     | 4       | 3       | 15    |

   - Evaluación económica de procesos
     Costos estimados por módulo (en soles):
     - Corte láser CNC: S/. 1600.00
     - Soldadura MIG: S/. 280.00
     - Soldadura por arco: S/. 250.00
     - Acabado superficial: S/. 200.00
     - Ensamblaje: S/. 200.00
   - Disponibilidad de equipamiento
     Principales talleres en Cusco con capacidad validada:
     - METAL SUR E.I.R.L: Corte láser CNC
     - ACEROS Y SERVICIOS E.I.R.L: Soldadura MIG/TIG
     - FAMAIC S.A.C: Mecanizado CNC
       [Fuente: Directorio Industrial Cámara de Comercio Cusco, 2024]

3. Secuencia de fabricación

   - Diagrama de flujo del proceso
     [Insertar figura 3.3: Diagrama de flujo]

     1. Recepción y control de materiales
     2. Corte CNC de componentes
     3. Verificación dimensional
     4. Preparación de juntas
     5. Soldadura de subconjuntos
     6. Control de calidad
     7. Ensamblaje de módulos
     8. Verificación final

   - Hojas de ruta por componente
     Ejemplo para panel lateral:

     1. Corte de perfiles principales
     2. Verificación dimensional
     3. Preparación de juntas
     4. Soldadura de diagonales
     5. Control de deformaciones
     6. Acabado superficial
     7. Inspección final

   - Puntos de control dimensional
     Verificación según ISO 13920:
     - Longitud total: ±1mm
     - Paralelismo: 0.5mm
     - Perpendicularidad: 0.5mm
     - Planitud: 0.8mm

4. Control dimensional

   - Protocolo de medición
     Equipos utilizados:
     - Calibrador digital (±0.02mm)
     - Micrómetro digital (±0.01mm)
     - Escuadras de precisión
     - Niveles digitales
   - Verificación de tolerancias
     Puntos críticos:
     - Distancia entre nodos
     - Alineación de conectores
     - Paralelismo de caras
     - Planitud de superficies
   - Registro y documentación
     Formato estandarizado incluyendo:
     - Dimensiones nominales
     - Medidas reales
     - Desviaciones
     - Acciones correctivas

## 3.3 Especificaciones Técnicas

### 3.3.1 Características Técnicas y Dimensionales

#### 3.3.1.1 Perfiles del Panel Principal

- Montantes verticales y diagonales:

  - Original: 80 x 40 mm (ASTM A36)
  - Escala 1:10: 8 x 4 mm
  - Tolerancia dimensional: ISO 2768-m
  - Paralelismo: 0.05 mm
  - Perpendicularidad: 0.1 mm

- Montantes horizontales:
  - Original: 100 x 40 mm (ASTM A36)
  - Escala 1:10: 10 x 4 mm
  - Tolerancia dimensional: ISO 2768-m
  - Planicidad: 0.1 mm
  - Rectitud: 0.05 mm

#### 3.3.1.2 Sistema de Arriostramiento

- Perfiles rectangulares:
  - Original: 78 x 40 mm (ASTM A36)
  - Escala 1:10: 7.8 x 4 mm
  - Tolerancia geométrica: ISO 1101
  - Paralelismo entre caras: 0.08 mm
  - Acabado superficial: Ra 3.2 μm

### 3.3.2 Selección de Materiales

- Propiedades mecánicas requeridas
  - Resistencia a la tracción: 400 MPa mín.
  - Límite elástico: 250 MPa mín.
  - Elongación: 20% mín.
- Maquinabilidad

  - Índice de maquinabilidad > 50%
  - Dureza: 150-180 HB
  - Velocidad de corte recomendada

- Disponibilidad comercial

  - Proveedores certificados
  - Trazabilidad de materiales
  - Certificados de calidad

- Análisis costo-beneficio
  - Evaluación técnico-económica
  - Vida útil estimada
  - Costos de procesamiento

## 3.6 Documentación Técnica

### 3.6.1 Planos de Fabricación

Los planos de fabricación constituyen la documentación fundamental para la manufactura del modelo a escala del puente Bailey, desarrollados bajo las normas ISO 128 y 129. Se incluyen:

#### 3.6.1.1 Planos Generales

- PG-001: Vista general del puente ensamblado
- PG-002: Disposición de módulos principales
- PG-003: Sistema de coordenadas y referencias

#### 3.6.1.2 Planos de Detalle

- PD-001: Panel principal
  - Geometría de montantes
  - Uniones y conexiones
  - Detalles de soldadura
- PD-002: Sistema de arriostramiento
  - Elementos transversales
  - Puntos de anclaje
- PD-003: Vigas tipo H
  - Perfil estructural
  - Detalles de alas y alma

### 3.6.2 Hojas de Proceso

#### 3.6.2.1 Procesos de Manufactura

- HP-001: Panel Principal
  - Operación: **\_\_\_**
  - Máquina: **\_\_\_**
  - Herramientas: **\_\_\_**
  - Parámetros: **\_\_\_**
- HP-002: Sistema de Arriostramiento
  - Operación: **\_\_\_**
  - Máquina: **\_\_\_**
  - Herramientas: **\_\_\_**
  - Parámetros: **\_\_\_**

#### 3.6.2.2 Secuencias de Ensamblaje

- SE-001: Ensamblaje de paneles
  - Paso 1: **\_\_\_**
  - Paso 2: **\_\_\_**
  - Herramientas requeridas: **\_\_\_**
- SE-002: Montaje de arriostramientos
  - Paso 1: **\_\_\_**
  - Paso 2: **\_\_\_**
  - Herramientas requeridas: **\_\_\_**

### 3.6.3 Registros de Control

#### 3.6.3.1 Formatos de Inspección Dimensional

- FI-001: Panel Principal

  - Dimensión crítica 1: **\_\_\_** (±0.1mm)
  - Dimensión crítica 2: **\_\_\_** (±0.1mm)
  - Paralelismo: **\_\_\_**
  - Perpendicularidad: **\_\_\_**

- FI-002: Sistema de Arriostramiento
  - Dimensión crítica 1: **\_\_\_** (±0.1mm)
  - Dimensión crítica 2: **\_\_\_** (±0.1mm)
  - Alineación: **\_\_\_**

#### 3.6.3.2 Control de Calidad

- CC-001: Verificación de Soldaduras

  - Tipo de inspección: **\_\_\_**
  - Criterios de aceptación: **\_\_\_**
  - Resultados: **\_\_\_**

- CC-002: Pruebas de Ajuste
  - Puntos de verificación: **\_\_\_**
  - Tolerancias permitidas: **\_\_\_**
  - Resultados: **\_\_\_**

#### 3.6.3.3 Registro de No Conformidades

- NC-001: Formato de No Conformidad
  - Descripción: **\_\_\_**
  - Causa raíz: **\_\_\_**
  - Acción correctiva: **\_\_\_**
  - Verificación: **\_\_\_**

### 3.6.4 Certificaciones y Validaciones

#### 3.6.4.1 Certificados de Material

- CM-001: Propiedades mecánicas
  - Material: **\_\_\_**
  - Resistencia: **\_\_\_**
  - Dureza: **\_\_\_**
  - Lote: **\_\_\_**

#### 3.6.4.2 Validación de Procesos

- VP-001: Verificación de procedimientos
  - Proceso: **\_\_\_**
  - Parámetros validados: **\_\_\_**
  - Resultados: **\_\_\_**
  - Fecha: **\_\_\_**
