# Motor de Búsqueda Distribuido - Search Bar Client

## 📋 Descripción del Proyecto

Este proyecto implementa un **motor de búsqueda distribuido** especializado en la detección y búsqueda de objetos específicos (como carros, aviones, etc.) dentro de contenido multimedia. El sistema utiliza tecnologías de Big Data para procesar grandes volúmenes de datos de video y metadatos, proporcionando resultados de búsqueda eficientes mediante algoritmos de Page Ranking.

## 🏗️ Arquitectura del Sistema

### Backend (Núcleo del Sistema)

El backend está construido con **Flask** y actúa como el cerebro del sistema, orquestando todas las operaciones entre el cliente y el clúster distribuido:

#### Componentes Principales:

1. **Servidor Flask**
   - API RESTful que gestiona las peticiones del cliente
   - Maneja la comunicación con el clúster Hadoop/Spark
   - Procesa las consultas de búsqueda y coordina las respuestas

2. **Integración con Clúster Distribuido**
   - **Apache Spark**: Motor de procesamiento distribuido para análisis de datos en tiempo real
   - **Hadoop MapReduce**: Procesamiento batch de grandes volúmenes de datos de video
   - **Apache Hive**: Data warehouse para consultas SQL sobre metadatos estructurados
   - **HDFS (Hadoop Distributed File System)**: Almacenamiento distribuido de videos y metadatos

3. **Algoritmo de Page Ranking**
   - Implementado usando Spark para rankear la relevancia de los resultados
   - Procesa metadatos de videos para determinar la importancia relativa
   - Optimiza los resultados de búsqueda basándose en patrones de acceso

### Frontend

El frontend está desarrollado en **React** y proporciona una interfaz de usuario intuitiva:

- **Componentes React**: Interfaz modular y reutilizable
- **Barra de Búsqueda**: Input principal para consultas de objetos
- **Reproductor de Video**: Componente integrado para visualización de resultados
- **Estado Global**: Manejo eficiente del estado de la aplicación
- **Comunicación Asíncrona**: Integración con APIs del backend mediante fetch/axios

## 🔄 Flujo de Funcionamiento

### 1. Proceso de Búsqueda

```
Usuario → Interfaz React → API Flask → Clúster Hadoop/Spark → HDFS
```

#### Pasos Detallados:

1. **Entrada del Usuario**
   - El usuario ingresa una consulta (ej: "carros", "aviones")
   - React captura la entrada y la envía al backend Flask

2. **Procesamiento en el Backend**
   - Flask recibe la petición HTTP
   - Se conecta directamente al **nodo master** o cualquier **nodo worker** con acceso a HDFS
   - Ejecuta funciones pre-compiladas y optimizadas en el clúster

3. **Búsqueda Distribuida**
   - **Hive** consulta los metadatos estructurados buscando coincidencias
   - **Spark** procesa los datos en paralelo aplicando algoritmos de Page Ranking
   - **MapReduce** maneja el procesamiento batch si es necesario

4. **Recuperación de Resultados**
   - El sistema identifica videos que contienen los objetos buscados
   - Los metadatos apuntan a la ubicación exacta en HDFS
   - Se aplica ranking para ordenar resultados por relevancia

### 2. Proceso de Reproducción

```
Resultado → HDFS → Conversión Local → Descarga → Reproducción
```

#### Pasos Detallados:

1. **Selección de Video**
   - El usuario selecciona un resultado de la búsqueda
   - React envía petición para recuperar el video específico

2. **Recuperación desde HDFS**
   - Flask accede al archivo de video almacenado en HDFS
   - Se verifica la integridad y disponibilidad del archivo

3. **Procesamiento Local**
   - El video se **convierte** al formato apropiado para reproducción web
   - Se **descarga localmente** de forma temporal para optimizar la reproducción
   - Se aplican las transformaciones necesarias (codificación, compresión)

4. **Reproducción**
   - El video procesado se sirve al componente reproductor de React
   - Se proporciona streaming eficiente al usuario final

## 🚀 Tecnologías Utilizadas

### Backend Stack
- **Flask**: Framework web minimalista y flexible
- **Apache Spark**: Procesamiento distribuido y análisis en tiempo real
- **Hadoop MapReduce**: Procesamiento batch de Big Data
- **Apache Hive**: Data warehouse y consultas SQL distribuidas
- **HDFS**: Sistema de archivos distribuido
- **Python**: Lenguaje principal del backend

### Frontend Stack
- **React**: Biblioteca para interfaces de usuario
- **JavaScript/ES6+**: Lenguaje de programación del frontend
- **HTML5 Video**: Para reproducción multimedia
- **CSS3**: Estilos y diseño responsivo

### Infraestructura
- **Clúster Hadoop**: Múltiples nodos para procesamiento distribuido
- **HDFS**: Almacenamiento distribuido y replicado
- **YARN**: Gestor de recursos del clúster

## 📡 Conectividad y Acceso

### Conexiones al Clúster

El sistema está diseñado para conectarse de manera flexible:

- **Conexión al Nodo Master**: Acceso principal para coordinar operaciones
- **Conexión a Nodos Worker**: Acceso directo para operaciones específicas
- **Acceso a HDFS**: Lectura/escritura distribuida de archivos
- **Funciones Pre-compiladas**: Código optimizado listo para ejecución inmediata

### Requisitos de Red

- Conectividad TCP/IP al clúster Hadoop
- Acceso a puertos específicos de HDFS (default: 9000, 50070)
- Conexión a Spark Master (default: 7077)
- Acceso a Hive Metastore (default: 9083)

## 🎯 Casos de Uso

### Búsquedas Soportadas
- **Detección de Vehículos**: Carros, camiones, motocicletas
- **Aeronaves**: Aviones, helicópteros, drones
- **Objetos Personalizados**: Extensible para nuevas categorías

### Tipos de Consulta
- Búsqueda por objeto específico
- Búsqueda por categoría
- Filtros por metadatos (fecha, duración, calidad)
- Ordenamiento por relevancia (Page Rank)

## 🔧 Configuración y Despliegue

### Requisitos Previos
- Clúster Hadoop/Spark configurado y ejecutándose
- Python 3.8+ con Flask instalado
- Node.js 14+ para el frontend React
- Acceso de red al clúster de Big Data

### Variables de Entorno
```bash
HADOOP_CONF_DIR=/path/to/hadoop/conf
SPARK_HOME=/path/to/spark
HIVE_CONF_DIR=/path/to/hive/conf
HDFS_NAMENODE_URL=hdfs://master:9000
```

## 📊 Rendimiento y Escalabilidad

### Ventajas del Diseño Distribuido
- **Escalabilidad Horizontal**: Agregar nodos mejora el rendimiento
- **Tolerancia a Fallos**: Replicación automática en HDFS
- **Procesamiento Paralelo**: Spark distribuye la carga automáticamente
- **Cache Inteligente**: Datos frecuentemente accedidos se mantienen en memoria

### Optimizaciones
- Índices en Hive para consultas rápidas
- Particionamiento de datos por categorías de objetos
- Cache de resultados frecuentes
- Compresión de videos para reducir transferencia de datos

## 🤝 Contribución

Este proyecto forma parte de un ecosistema de Big Data más amplio y está diseñado para ser extensible y mantenible. Las contribuciones son bienvenidas, especialmente en:

- Nuevos algoritmos de detección de objetos
- Optimizaciones de rendimiento
- Mejoras en la interfaz de usuario
- Documentación y casos de prueba

---

*Proyecto desarrollado como demostración de integración entre tecnologías de Big Data y aplicaciones web modernas.*
