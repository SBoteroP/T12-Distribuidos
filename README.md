# Calculadora Distribuida con gRPC en Python

Este proyecto implementa una **calculadora distribuida** utilizando **gRPC en Python**.  
Se distribuyen los cálculos en diferentes servidores para **balancear la carga** y mejorar la eficiencia.

## Estructura del Taller

El sistema consta de los siguientes componentes:

- **Cliente (`client.py`)**: Envía solicitudes de cálculo al servidor de cálculo.
- **Servidor de Cálculo (`server_calculo.py`)**: Recibe solicitudes del cliente y las delega a los servidores de operación.
- **Servidor de Operación 1 (`server_op1.py`)**: Realiza operaciones matemáticas.
- **Servidor de Operación 2 (`server_op2.py`)**: Realiza operaciones matemáticas.
- **Definición de Protocolo (`archivo.proto`)**: Define los mensajes y servicios gRPC.

### 1️⃣ Instalar Dependencias

Ejecuta el siguiente comando para instalar los paquetes necesarios:

```sh
pip install grpcio grpcio-tools
```

### 2️⃣ Compilar el Archivo `.proto`

Es necesario **compilar `archivo.proto`** para generar los archivos Python necesarios:

```sh
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. archivo.proto
```

Esto generará los siguientes archivos:

- `archivo_pb2.py`
- `archivo_pb2_grpc.py`

### 3️⃣ Ejecutar los Servidores

Debes iniciar los servidores en **diferentes máquinas** o en **diferentes terminales**.

#### En la Máquina 1 (o Terminal 1):
```sh
python3 server_op1.py 50051 192.168.1.100
```

#### En la Máquina 2 (o Terminal 2):
```sh
python3 server_op2.py 50052 192.168.1.101
```

#### En la Máquina 3 (o Terminal 3):
```sh
python3 server_calculo.py
```

### 4️⃣ Ejecutar el Cliente

Ejecuta el cliente desde cualquier máquina y **conéctalo al servidor de cálculo**:

```sh
python3 client.py
```

Luego, ingresa una expresión matemática con **tres valores y dos operaciones**, por ejemplo:

```
190 * 2000 / 5
```

El cliente dividirá la operación en **dos pasos** y delegará el cálculo entre los servidores.

---

## 📌 Ejemplo de Salida

#### **Cliente (`client.py`):**
```
Ingrese una expresión con tres operaciones (ej: '20 * 10 / 2') o 'q' para salir: 10 * 5 - 2
Resultado final: 10 * 5 - 2 = 48
```

#### **Servidor de Operación 1 (`server_op1.py`):**
```
Procesando: 10 * 5 = 50
```

#### **Servidor de Operación 2 (`server_op2.py`):**
```
Procesando: 50 - 2 = 48
```

