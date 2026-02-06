# Modulo 09: Cloud Engineering con LocalStack

**Curso:** Big Data con Python - De Cero a Produccion
**Profesor:** Juan Marcelo Gutierrez Miranda | @TodoEconometria

---

## Objetivo del Modulo

Aprender a disenar, construir y desplegar infraestructura cloud **sin gastar un centavo**
usando LocalStack, el simulador completo de AWS. Al finalizar, tendras las mismas
habilidades que se usan en produccion real, pero probadas localmente.

**Filosofia:** "Si funciona en LocalStack, funciona en AWS"

---

## Por que LocalStack?

### El Problema Tradicional

```
Estudiante quiere aprender AWS:
  1. Crea cuenta AWS → Pide tarjeta de credito
  2. Free tier tiene limites confusos
  3. Un error = factura inesperada
  4. Miedo a experimentar
  5. Aprende poco, gasta mucho
```

### La Solucion LocalStack

```
Estudiante con LocalStack:
  1. docker compose up → Listo
  2. Sin limites, sin tarjeta
  3. Errores = reinicia contenedor
  4. Libertad total para experimentar
  5. Aprende todo, gasta $0
```

### Que Simula LocalStack?

| Servicio AWS | LocalStack | Uso en Big Data |
|--------------|------------|-----------------|
| **S3** | 100% | Data Lake, almacenamiento |
| **Lambda** | 100% | Procesamiento serverless |
| **Kinesis** | 100% | Streaming de datos |
| **DynamoDB** | 100% | Base NoSQL |
| **SQS/SNS** | 100% | Mensajeria |
| **IAM** | Parcial | Permisos (simplificado) |
| **CloudWatch** | Parcial | Logs y metricas |

---

## Contenido del Modulo

| Seccion | Tema | Que aprenderas |
|---------|------|----------------|
| 9.1 | Introduccion a Cloud y LocalStack | Conceptos cloud, instalacion LocalStack |
| 9.2 | S3: Data Lake Local | Buckets, objetos, versionado, lifecycle |
| 9.3 | Lambda + S3: Pipeline Event-Driven | Funciones serverless, triggers |
| 9.4 | Terraform con LocalStack | Infraestructura como Codigo (IaC) |
| 9.5 | Kinesis: Streaming sin Kafka | Alternativa AWS a Kafka |
| 9.6 | De Local a Real | Como migrar a AWS real |

---

## 9.1 Introduccion a Cloud y LocalStack

### Que es "La Nube"?

La nube no es magia. Son **servidores de otras empresas** que alquilas por tiempo:

```
Tu laptop                    La Nube (AWS)
---------                    -------------
- 16 GB RAM                  - Ilimitada RAM (pagas por uso)
- 1 TB disco                 - Ilimitados discos (pagas por GB)
- 1 GPU                      - 1000 GPUs (pagas por hora)
- Siempre encendida          - Enciendes cuando necesitas
- Tu la mantienes            - Ellos la mantienen
```

### Los 3 Modelos de Servicio

```
┌─────────────────────────────────────────────────────────────┐
│                    TU RESPONSABILIDAD                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  On-Premise     IaaS          PaaS          SaaS           │
│  (Tu server)    (AWS EC2)     (AWS Lambda)  (Gmail)        │
│                                                             │
│  ┌─────────┐    ┌─────────┐   ┌─────────┐   ┌─────────┐    │
│  │Aplicacion│   │Aplicacion│  │Aplicacion│  │         │    │
│  ├─────────┤   ├─────────┤   │         │   │         │    │
│  │ Runtime │   │ Runtime │   │         │   │         │    │
│  ├─────────┤   ├─────────┤   ├─────────┤   │         │    │
│  │   OS    │   │   OS    │   │         │   │ TODO    │    │
│  ├─────────┤   ├─────────┤   │         │   │INCLUIDO │    │
│  │ Server  │   │         │   │         │   │         │    │
│  ├─────────┤   │         │   │         │   │         │    │
│  │ Network │   │         │   │         │   │         │    │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘    │
│                                                             │
│  Tu manejas     Tu manejas   Tu manejas    Tu usas         │
│  TODO           app + OS     solo app      y ya            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Instalacion de LocalStack

**Requisitos:**
- Docker Desktop instalado y corriendo
- Python 3.9+ (para awscli-local)
- 4 GB RAM libres

**docker-compose.localstack.yml:**

```yaml
services:
  localstack:
    image: localstack/localstack:3.0
    container_name: bigdata_localstack
    hostname: localstack
    ports:
      - "4566:4566"           # Gateway unificado
      - "4510-4559:4510-4559" # Servicios externos
    environment:
      - SERVICES=s3,lambda,kinesis,dynamodb,sqs,sns,iam,logs
      - DEBUG=0
      - PERSISTENCE=1         # Mantiene datos entre reinicios
      - LAMBDA_EXECUTOR=docker
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - localstack_data:/var/lib/localstack
      - /var/run/docker.sock:/var/run/docker.sock
      - ./lambdas:/opt/code/localstack/lambdas
    networks:
      - bigdata_network

volumes:
  localstack_data:
    name: bigdata_localstack_data

networks:
  bigdata_network:
    name: bigdata_curso_network
    external: true
```

### Configurar AWS CLI para LocalStack

```bash
# Instalar awscli-local (wrapper para LocalStack)
pip install awscli-local

# Verificar instalacion
awslocal --version

# Probar conexion
awslocal s3 ls
# (lista vacia, aun no hay buckets)
```

**Diferencia clave:**
- `aws s3 ls` → Conecta a AWS real (necesita credenciales)
- `awslocal s3 ls` → Conecta a LocalStack (localhost:4566)

### Verificar que LocalStack Funciona

```bash
# Levantar LocalStack
docker compose -f docker-compose.localstack.yml up -d

# Verificar servicios activos
curl http://localhost:4566/_localstack/health | python -m json.tool

# Respuesta esperada:
{
  "services": {
    "s3": "running",
    "lambda": "running",
    "kinesis": "running",
    ...
  }
}
```

---

## 9.2 S3: Data Lake Local

### Que es S3?

**S3 = Simple Storage Service** = El disco duro infinito de la nube.

```
S3 Estructura:
├── bucket-ventas/              ← Bucket (como una carpeta raiz)
│   ├── 2024/                   ← Prefijo (no son carpetas reales)
│   │   ├── enero/
│   │   │   └── ventas.parquet  ← Objeto (el archivo real)
│   │   └── febrero/
│   │       └── ventas.parquet
│   └── raw/
│       └── ventas.csv
└── bucket-logs/
    └── app.log
```

**Conceptos clave:**
- **Bucket:** Contenedor de objetos (nombre unico globalmente en AWS real)
- **Objeto:** El archivo + metadatos
- **Prefijo:** Simulacion de carpetas (S3 es plano, no tiene carpetas reales)
- **Key:** Ruta completa del objeto (`2024/enero/ventas.parquet`)

### Crear y Usar Buckets

```bash
# Crear bucket
awslocal s3 mb s3://datalake-curso

# Listar buckets
awslocal s3 ls

# Subir archivo
awslocal s3 cp datos/ventas.csv s3://datalake-curso/raw/

# Listar contenido del bucket
awslocal s3 ls s3://datalake-curso/raw/

# Descargar archivo
awslocal s3 cp s3://datalake-curso/raw/ventas.csv descargado.csv

# Sincronizar carpeta completa
awslocal s3 sync ./datos/ s3://datalake-curso/data/
```

### Usar S3 desde Python (boto3)

```python
"""
s3_operaciones.py
Operaciones basicas con S3 usando boto3 + LocalStack
"""
import boto3
import pandas as pd
from io import BytesIO

# Configurar cliente S3 para LocalStack
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',           # LocalStack acepta cualquier valor
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Crear bucket
s3.create_bucket(Bucket='datalake-curso')
print("Bucket creado!")

# Subir archivo
s3.upload_file(
    Filename='datos/ventas.csv',
    Bucket='datalake-curso',
    Key='raw/ventas.csv'
)
print("Archivo subido!")

# Listar objetos
response = s3.list_objects_v2(Bucket='datalake-curso')
for obj in response.get('Contents', []):
    print(f"  {obj['Key']} - {obj['Size']} bytes")

# Leer CSV directamente desde S3 a Pandas
obj = s3.get_object(Bucket='datalake-curso', Key='raw/ventas.csv')
df = pd.read_csv(BytesIO(obj['Body'].read()))
print(f"\nDataFrame cargado: {len(df)} filas")

# Guardar Parquet en S3
buffer = BytesIO()
df.to_parquet(buffer, index=False)
buffer.seek(0)
s3.put_object(
    Bucket='datalake-curso',
    Key='processed/ventas.parquet',
    Body=buffer.getvalue()
)
print("Parquet guardado en S3!")
```

### Arquitectura Data Lake con S3

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAKE EN S3                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  s3://datalake-curso/                                       │
│  │                                                          │
│  ├── raw/                    ← BRONCE: Datos crudos         │
│  │   ├── ventas_2024.csv         (tal cual llegan)          │
│  │   ├── clientes.json                                      │
│  │   └── logs/                                              │
│  │                                                          │
│  ├── processed/              ← PLATA: Datos limpios         │
│  │   ├── ventas.parquet          (validados, tipados)       │
│  │   └── clientes.parquet                                   │
│  │                                                          │
│  └── curated/                ← ORO: Datos listos            │
│      ├── kpis_diarios.parquet    (agregados, metricas)      │
│      └── dashboard_data.parquet                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Ejercicio 9.2: Data Lake Local

**Objetivo:** Construir un mini Data Lake con las 3 capas.

```python
"""
ejercicio_9_2_datalake.py
Construir Data Lake Bronze/Silver/Gold en S3 local
"""
import boto3
import pandas as pd
from io import BytesIO

# Configurar S3
s3 = boto3.client('s3', endpoint_url='http://localhost:4566',
                  aws_access_key_id='test', aws_secret_access_key='test')

BUCKET = 'datalake-ejercicio'

def crear_estructura():
    """Crear bucket y estructura de carpetas"""
    s3.create_bucket(Bucket=BUCKET)
    print(f"Bucket {BUCKET} creado")

def bronze_ingesta(archivo_local, destino_s3):
    """Capa Bronze: Ingestar datos crudos"""
    s3.upload_file(archivo_local, BUCKET, f'raw/{destino_s3}')
    print(f"Bronze: {archivo_local} → s3://{BUCKET}/raw/{destino_s3}")

def silver_limpieza(origen_key, destino_key):
    """Capa Silver: Limpiar y transformar"""
    # Leer de Bronze
    obj = s3.get_object(Bucket=BUCKET, Key=f'raw/{origen_key}')
    df = pd.read_csv(BytesIO(obj['Body'].read()))

    # Limpiar
    df = df.dropna()
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]

    # Guardar en Silver como Parquet
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    s3.put_object(Bucket=BUCKET, Key=f'processed/{destino_key}', Body=buffer.getvalue())
    print(f"Silver: {len(df)} filas limpias → s3://{BUCKET}/processed/{destino_key}")
    return df

def gold_agregacion(origen_key, destino_key, grupo, metricas):
    """Capa Gold: Agregar para analytics"""
    # Leer de Silver
    obj = s3.get_object(Bucket=BUCKET, Key=f'processed/{origen_key}')
    df = pd.read_parquet(BytesIO(obj['Body'].read()))

    # Agregar
    df_agg = df.groupby(grupo).agg(metricas).reset_index()

    # Guardar en Gold
    buffer = BytesIO()
    df_agg.to_parquet(buffer, index=False)
    buffer.seek(0)
    s3.put_object(Bucket=BUCKET, Key=f'curated/{destino_key}', Body=buffer.getvalue())
    print(f"Gold: Agregado por {grupo} → s3://{BUCKET}/curated/{destino_key}")
    return df_agg

if __name__ == '__main__':
    # 1. Crear estructura
    crear_estructura()

    # 2. Bronze: Ingestar CSV crudo
    bronze_ingesta('datos/ventas_ejemplo.csv', 'ventas_2024.csv')

    # 3. Silver: Limpiar
    df_clean = silver_limpieza('ventas_2024.csv', 'ventas.parquet')

    # 4. Gold: Agregar ventas por categoria
    df_kpis = gold_agregacion(
        'ventas.parquet',
        'kpis_categoria.parquet',
        grupo='categoria',
        metricas={'monto': ['sum', 'mean', 'count']}
    )

    print("\n--- Data Lake completado ---")
    print(df_kpis)
```

---

## 9.3 Lambda + S3: Pipeline Event-Driven

### Que es AWS Lambda?

Lambda = **Codigo sin servidor**. Tu escribes una funcion, AWS la ejecuta cuando ocurre un evento.

```
Modelo tradicional:                Modelo Lambda:
------------------                 --------------
1. Alquilas servidor 24/7          1. Subes funcion
2. Instalas dependencias           2. Defines trigger (evento)
3. Despliegas codigo               3. Se ejecuta solo cuando hay evento
4. Pagas aunque nadie use          4. Pagas solo por ejecucion
5. Escalas manualmente             5. Escala automaticamente
```

### Anatomia de una Funcion Lambda

```python
"""
mi_lambda.py
Estructura basica de una funcion Lambda
"""

def handler(event, context):
    """
    Punto de entrada de Lambda.

    Args:
        event: Datos del evento que disparo la funcion
               (ej: nuevo archivo en S3, mensaje SQS, etc.)
        context: Informacion del entorno de ejecucion
                 (tiempo restante, memoria, etc.)

    Returns:
        Respuesta de la funcion (dict, string, etc.)
    """
    # Tu logica aqui
    nombre_archivo = event['Records'][0]['s3']['object']['key']

    print(f"Procesando: {nombre_archivo}")

    # Hacer algo con el archivo...
    resultado = procesar_archivo(nombre_archivo)

    return {
        'statusCode': 200,
        'body': f'Procesado: {nombre_archivo}'
    }
```

### Pipeline Event-Driven: S3 → Lambda → S3

```
┌─────────────────────────────────────────────────────────────┐
│              PIPELINE EVENT-DRIVEN                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Usuario                S3 (raw/)              Lambda      │
│   -------                ---------              ------      │
│      │                      │                     │         │
│      │  sube CSV            │                     │         │
│      │─────────────────────>│                     │         │
│      │                      │                     │         │
│      │                      │  evento: PutObject  │         │
│      │                      │────────────────────>│         │
│      │                      │                     │         │
│      │                      │         procesa     │         │
│      │                      │         CSV         │         │
│      │                      │                     │         │
│      │                      │    guarda Parquet   │         │
│      │                      │<────────────────────│         │
│      │                      │                     │         │
│   S3 (processed/)           │                     │         │
│   tiene el Parquet          │                     │         │
│   automaticamente           │                     │         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Crear Lambda en LocalStack

**1. Escribir la funcion (lambdas/procesar_csv.py):**

```python
"""
procesar_csv.py
Lambda que convierte CSV a Parquet automaticamente
"""
import boto3
import pandas as pd
from io import BytesIO
import json

# Configurar cliente S3 (dentro de LocalStack)
s3 = boto3.client('s3', endpoint_url='http://localhost:4566')

def handler(event, context):
    """Procesa CSV subido a S3 y genera Parquet"""

    # Extraer info del evento S3
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    print(f"Evento recibido: s3://{bucket}/{key}")

    # Solo procesar CSVs en raw/
    if not key.startswith('raw/') or not key.endswith('.csv'):
        return {'statusCode': 200, 'body': 'Ignorado (no es CSV en raw/)'}

    try:
        # Leer CSV desde S3
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(BytesIO(obj['Body'].read()))
        print(f"CSV leido: {len(df)} filas, {len(df.columns)} columnas")

        # Limpiar datos
        df = df.dropna()
        df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]

        # Generar key de destino
        nombre_archivo = key.split('/')[-1].replace('.csv', '.parquet')
        key_destino = f"processed/{nombre_archivo}"

        # Guardar como Parquet
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        s3.put_object(Bucket=bucket, Key=key_destino, Body=buffer.getvalue())

        print(f"Parquet guardado: s3://{bucket}/{key_destino}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'origen': key,
                'destino': key_destino,
                'filas': len(df)
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}
```

**2. Empaquetar la Lambda:**

```bash
# Crear directorio de empaquetado
mkdir -p lambdas/package
cd lambdas/package

# Instalar dependencias
pip install pandas pyarrow -t .

# Copiar codigo
cp ../procesar_csv.py .

# Crear ZIP
zip -r ../procesar_csv.zip .

cd ../..
```

**3. Desplegar en LocalStack:**

```bash
# Crear funcion Lambda
awslocal lambda create-function \
    --function-name procesar-csv \
    --runtime python3.11 \
    --handler procesar_csv.handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --zip-file fileb://lambdas/procesar_csv.zip \
    --timeout 60 \
    --memory-size 256

# Verificar
awslocal lambda list-functions
```

**4. Configurar trigger S3:**

```bash
# Dar permiso a S3 para invocar Lambda
awslocal lambda add-permission \
    --function-name procesar-csv \
    --statement-id s3-trigger \
    --action lambda:InvokeFunction \
    --principal s3.amazonaws.com \
    --source-arn arn:aws:s3:::datalake-curso

# Configurar notificacion en el bucket
awslocal s3api put-bucket-notification-configuration \
    --bucket datalake-curso \
    --notification-configuration '{
        "LambdaFunctionConfigurations": [{
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:procesar-csv",
            "Events": ["s3:ObjectCreated:*"],
            "Filter": {
                "Key": {
                    "FilterRules": [
                        {"Name": "prefix", "Value": "raw/"},
                        {"Name": "suffix", "Value": ".csv"}
                    ]
                }
            }
        }]
    }'
```

**5. Probar el pipeline:**

```bash
# Subir CSV a raw/
awslocal s3 cp datos/ventas.csv s3://datalake-curso/raw/

# La Lambda se ejecuta automaticamente!
# Ver logs
awslocal logs filter-log-events \
    --log-group-name /aws/lambda/procesar-csv

# Verificar que se creo el Parquet
awslocal s3 ls s3://datalake-curso/processed/
# Deberia mostrar: ventas.parquet
```

---

## 9.4 Terraform con LocalStack

### Que es Terraform?

Terraform = **Infraestructura como Codigo (IaC)**

```
Sin Terraform:                     Con Terraform:
--------------                     --------------
1. Click en consola AWS            1. Escribes archivo .tf
2. Configuras manualmente          2. terraform plan (preview)
3. Repites en cada entorno         3. terraform apply (ejecuta)
4. No hay historial                4. Git trackea cambios
5. Dificil reproducir              5. Mismo resultado siempre
```

### Instalar Terraform

```bash
# Windows (winget)
winget install HashiCorp.Terraform

# macOS (brew)
brew install terraform

# Linux
sudo apt-get install terraform

# Verificar
terraform --version
```

### Configurar Terraform para LocalStack

**main.tf:**

```hcl
# ==================================================================
# TERRAFORM + LOCALSTACK
# Infraestructura como Codigo para nuestro Data Lake
# ==================================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configurar provider para LocalStack
provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"

  # Forzar a usar LocalStack en lugar de AWS real
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3     = "http://localhost:4566"
    lambda = "http://localhost:4566"
    iam    = "http://localhost:4566"
    sqs    = "http://localhost:4566"
    sns    = "http://localhost:4566"
  }
}

# ==================================================================
# S3: DATA LAKE
# ==================================================================

resource "aws_s3_bucket" "datalake" {
  bucket = "datalake-terraform"

  tags = {
    Environment = "desarrollo"
    Proyecto    = "curso-bigdata"
  }
}

resource "aws_s3_bucket_versioning" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Crear "carpetas" (prefijos)
resource "aws_s3_object" "raw" {
  bucket = aws_s3_bucket.datalake.id
  key    = "raw/"
  source = "/dev/null"  # Objeto vacio para crear prefijo
}

resource "aws_s3_object" "processed" {
  bucket = aws_s3_bucket.datalake.id
  key    = "processed/"
  source = "/dev/null"
}

resource "aws_s3_object" "curated" {
  bucket = aws_s3_bucket.datalake.id
  key    = "curated/"
  source = "/dev/null"
}

# ==================================================================
# IAM: ROL PARA LAMBDA
# ==================================================================

resource "aws_iam_role" "lambda_role" {
  name = "lambda-s3-processor-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "lambda-s3-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.datalake.arn,
          "${aws_s3_bucket.datalake.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# ==================================================================
# LAMBDA: PROCESADOR CSV
# ==================================================================

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambdas/package"
  output_path = "${path.module}/lambdas/procesar_csv.zip"
}

resource "aws_lambda_function" "procesar_csv" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "procesar-csv-terraform"
  role             = aws_iam_role.lambda_role.arn
  handler          = "procesar_csv.handler"
  runtime          = "python3.11"
  timeout          = 60
  memory_size      = 256
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      BUCKET_DESTINO = aws_s3_bucket.datalake.id
    }
  }
}

# Permiso para que S3 invoque Lambda
resource "aws_lambda_permission" "s3_trigger" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.procesar_csv.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.datalake.arn
}

# Notificacion S3 → Lambda
resource "aws_s3_bucket_notification" "lambda_trigger" {
  bucket = aws_s3_bucket.datalake.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.procesar_csv.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.s3_trigger]
}

# ==================================================================
# OUTPUTS
# ==================================================================

output "bucket_name" {
  value = aws_s3_bucket.datalake.id
}

output "lambda_arn" {
  value = aws_lambda_function.procesar_csv.arn
}

output "instrucciones" {
  value = <<-EOT

    Pipeline desplegado! Para probar:

    1. Subir CSV:
       awslocal s3 cp datos/test.csv s3://${aws_s3_bucket.datalake.id}/raw/

    2. Ver Parquet generado:
       awslocal s3 ls s3://${aws_s3_bucket.datalake.id}/processed/

  EOT
}
```

### Comandos Terraform

```bash
# Inicializar (descarga providers)
terraform init

# Ver que se va a crear (preview)
terraform plan

# Crear infraestructura
terraform apply

# Ver estado actual
terraform show

# Destruir todo
terraform destroy
```

### Flujo de Trabajo IaC

```
┌─────────────────────────────────────────────────────────────┐
│              FLUJO TERRAFORM                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. ESCRIBIR         2. PLANIFICAR       3. APLICAR       │
│   -----------         -------------       ----------        │
│                                                             │
│   main.tf             terraform plan      terraform apply   │
│   ┌─────────┐        ┌─────────────┐     ┌─────────────┐   │
│   │ bucket  │   →    │ + bucket    │  →  │ Creando...  │   │
│   │ lambda  │        │ + lambda    │     │ Bucket OK   │   │
│   │ iam     │        │ + iam role  │     │ Lambda OK   │   │
│   └─────────┘        │ 3 to add    │     │ IAM OK      │   │
│                      └─────────────┘     │ 3 created   │   │
│                                          └─────────────┘   │
│                                                             │
│   4. VERSION CONTROL                                        │
│   ------------------                                        │
│                                                             │
│   git add main.tf                                          │
│   git commit -m "feat: agregar lambda procesador"          │
│   git push                                                  │
│                                                             │
│   → Historial completo de TODA tu infraestructura          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9.5 Kinesis: Streaming sin Kafka

### Kafka vs Kinesis

| Aspecto | Kafka | Kinesis |
|---------|-------|---------|
| **Proveedor** | Open source | AWS |
| **Gestion** | Tu lo operas | AWS lo opera |
| **Escalado** | Manual | Automatico |
| **Precio** | $0 (tu infra) | Por shard/hora |
| **Latencia** | Muy baja (<10ms) | Baja (~200ms) |
| **Ecosistema** | Enorme | AWS nativo |

**Cuando usar cual:**
- **Kafka:** Multi-cloud, latencia critica, control total
- **Kinesis:** AWS puro, simplicidad, serverless

### Arquitectura Kinesis

```
┌─────────────────────────────────────────────────────────────┐
│                    KINESIS DATA STREAMS                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Productores          Stream              Consumidores      │
│  -----------          ------              ------------      │
│                                                             │
│  ┌─────────┐         ┌──────────────┐                      │
│  │ App 1   │────────>│  Shard 1     │────>┌─────────┐      │
│  └─────────┘         ├──────────────┤     │ Lambda  │      │
│                      │  Shard 2     │────>└─────────┘      │
│  ┌─────────┐         ├──────────────┤                      │
│  │ IoT     │────────>│  Shard 3     │────>┌─────────┐      │
│  └─────────┘         └──────────────┘     │ Spark   │      │
│                                           │Streaming│      │
│  ┌─────────┐                              └─────────┘      │
│  │ Web     │──────────────────────────────────┐            │
│  └─────────┘                                  │            │
│                                           ┌───▼─────┐      │
│                                           │ Firehose│      │
│                                           │ → S3    │      │
│                                           └─────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Crear Stream en LocalStack

```bash
# Crear stream con 2 shards
awslocal kinesis create-stream \
    --stream-name eventos-economicos \
    --shard-count 2

# Verificar
awslocal kinesis describe-stream --stream-name eventos-economicos
```

### Productor Kinesis (Python)

```python
"""
kinesis_productor.py
Enviar eventos economicos a Kinesis
"""
import boto3
import json
import random
from datetime import datetime
import time

# Cliente Kinesis para LocalStack
kinesis = boto3.client(
    'kinesis',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

STREAM_NAME = 'eventos-economicos'

def generar_evento():
    """Genera evento economico simulado"""
    return {
        'timestamp': datetime.now().isoformat(),
        'indicador': random.choice(['PIB', 'Inflacion', 'Desempleo', 'TasaInteres']),
        'pais': random.choice(['ARG', 'BRA', 'CHL', 'MEX', 'COL']),
        'valor': round(random.uniform(-5, 10), 2),
        'fuente': 'simulador'
    }

def enviar_evento(evento):
    """Envia evento a Kinesis"""
    response = kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(evento).encode('utf-8'),
        PartitionKey=evento['pais']  # Particionar por pais
    )
    return response['SequenceNumber']

if __name__ == '__main__':
    print(f"Enviando eventos a {STREAM_NAME}...")

    while True:
        evento = generar_evento()
        seq = enviar_evento(evento)
        print(f"[{evento['timestamp']}] {evento['indicador']} {evento['pais']}: {evento['valor']} (seq: {seq[:20]}...)")
        time.sleep(1)
```

### Consumidor Kinesis (Python)

```python
"""
kinesis_consumidor.py
Leer eventos de Kinesis
"""
import boto3
import json
import time

kinesis = boto3.client(
    'kinesis',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

STREAM_NAME = 'eventos-economicos'

def obtener_shards():
    """Obtiene lista de shards del stream"""
    response = kinesis.describe_stream(StreamName=STREAM_NAME)
    return [s['ShardId'] for s in response['StreamDescription']['Shards']]

def consumir_shard(shard_id):
    """Consume eventos de un shard"""
    # Obtener iterator (desde el inicio)
    iterator_response = kinesis.get_shard_iterator(
        StreamName=STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'  # Desde el principio
        # Otras opciones: LATEST, AT_TIMESTAMP
    )
    iterator = iterator_response['ShardIterator']

    print(f"Consumiendo shard {shard_id}...")

    while iterator:
        response = kinesis.get_records(ShardIterator=iterator, Limit=100)

        for record in response['Records']:
            evento = json.loads(record['Data'].decode('utf-8'))
            print(f"  [{evento['pais']}] {evento['indicador']}: {evento['valor']}")

        iterator = response.get('NextShardIterator')
        time.sleep(1)

if __name__ == '__main__':
    shards = obtener_shards()
    print(f"Stream tiene {len(shards)} shards")

    # Consumir primer shard (en produccion usarias threads)
    consumir_shard(shards[0])
```

### Kinesis + Lambda (Event Source Mapping)

```bash
# Crear Lambda consumidora
awslocal lambda create-function \
    --function-name procesar-kinesis \
    --runtime python3.11 \
    --handler kinesis_lambda.handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --zip-file fileb://lambdas/kinesis_lambda.zip

# Conectar Kinesis → Lambda
awslocal lambda create-event-source-mapping \
    --function-name procesar-kinesis \
    --event-source-arn arn:aws:kinesis:us-east-1:000000000000:stream/eventos-economicos \
    --starting-position TRIM_HORIZON \
    --batch-size 100
```

---

## 9.6 De Local a Real

### La Promesa de LocalStack

Todo lo que hiciste en LocalStack funciona en AWS real **cambiando solo la URL del endpoint**.

### Diferencias Practicas

| Aspecto | LocalStack | AWS Real |
|---------|------------|----------|
| **Endpoint** | `localhost:4566` | Default (quitar endpoint_url) |
| **Credenciales** | `test/test` | IAM real (access key + secret) |
| **Persistencia** | Docker volume | AWS infraestructura |
| **Costos** | $0 | Segun uso |
| **Limites** | Sin limites | Quotas por servicio |
| **IAM** | Simplificado | Completo y critico |
| **Networking** | Red Docker | VPCs, subnets, security groups |

### Migracion de Codigo

**LocalStack (desarrollo):**

```python
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',  # ← Quitar esta linea
    aws_access_key_id='test',              # ← Usar credenciales reales
    aws_secret_access_key='test',
    region_name='us-east-1'
)
```

**AWS Real (produccion):**

```python
# Usa credenciales de ~/.aws/credentials o variables de entorno
s3 = boto3.client('s3', region_name='us-east-1')
```

### Patron Recomendado: Variables de Entorno

```python
"""
cliente_s3.py
Cliente S3 que funciona en LocalStack y AWS
"""
import boto3
import os

def get_s3_client():
    """Crea cliente S3 segun entorno"""
    endpoint = os.environ.get('AWS_ENDPOINT_URL')

    if endpoint:
        # LocalStack (desarrollo)
        return boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
    else:
        # AWS real (produccion)
        return boto3.client(
            's3',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

# Uso
s3 = get_s3_client()
s3.list_buckets()
```

**Configuracion por entorno:**

```bash
# .env.local (desarrollo)
AWS_ENDPOINT_URL=http://localhost:4566
AWS_REGION=us-east-1

# .env.prod (produccion)
AWS_REGION=us-east-1
# No hay AWS_ENDPOINT_URL → usa AWS real
```

### Terraform: LocalStack → AWS

**variables.tf:**

```hcl
variable "environment" {
  description = "Entorno de despliegue"
  type        = string
  default     = "local"  # local | dev | prod
}

variable "localstack_endpoint" {
  description = "Endpoint de LocalStack"
  type        = string
  default     = "http://localhost:4566"
}
```

**providers.tf:**

```hcl
provider "aws" {
  region = "us-east-1"

  # Configuracion condicional segun entorno
  skip_credentials_validation = var.environment == "local"
  skip_metadata_api_check     = var.environment == "local"
  skip_requesting_account_id  = var.environment == "local"

  dynamic "endpoints" {
    for_each = var.environment == "local" ? [1] : []
    content {
      s3     = var.localstack_endpoint
      lambda = var.localstack_endpoint
      iam    = var.localstack_endpoint
    }
  }
}
```

**Uso:**

```bash
# LocalStack
terraform apply -var="environment=local"

# AWS real (dev)
terraform apply -var="environment=dev"

# AWS real (prod)
terraform apply -var="environment=prod"
```

### Checklist Pre-Produccion

Antes de pasar a AWS real:

- [ ] Configurar credenciales IAM (no usar root)
- [ ] Crear VPC y subnets apropiadas
- [ ] Configurar security groups
- [ ] Habilitar encryption at rest (S3, RDS)
- [ ] Configurar CloudWatch alarms
- [ ] Establecer presupuesto y alertas de costo
- [ ] Revisar IAM policies (principio de minimo privilegio)
- [ ] Habilitar CloudTrail para auditoria
- [ ] Configurar backups automaticos
- [ ] Probar en entorno de staging antes de produccion

---

## Proyecto Final: Pipeline Cloud Completo

### Descripcion

Construir un pipeline de datos completo usando LocalStack que simule un sistema de produccion real.

### Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│           PIPELINE CLOUD - OBSERVATORIO ECONOMICO           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Simulador]      [Kinesis]       [Lambda]        [S3]     │
│      │               │               │              │       │
│      │  eventos      │   batch       │   parquet    │       │
│      │──────────────>│──────────────>│─────────────>│       │
│      │               │               │              │       │
│                                                 ┌───┴───┐   │
│                                                 │ raw/  │   │
│  [API]           [Lambda]        [DynamoDB]    │ proc/ │   │
│      │               │               │          │ cur/  │   │
│      │  consulta     │   busca       │          └───────┘   │
│      │──────────────>│──────────────>│                      │
│                                                             │
│  TODO DESPLEGADO CON TERRAFORM                              │
│  TODO SIMULADO EN LOCALSTACK                                │
│  $0 DE COSTO                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Entregables

1. **docker-compose.yaml** - LocalStack + servicios auxiliares
2. **main.tf** - Infraestructura completa en Terraform
3. **lambdas/** - Funciones Lambda (procesador, API)
4. **simulador/** - Generador de eventos economicos
5. **README.md** - Documentacion y comandos

### Criterios de Evaluacion

| Componente | Peso | Descripcion |
|------------|------|-------------|
| S3 Data Lake | 20% | Estructura Bronze/Silver/Gold |
| Lambda Functions | 25% | Procesamiento automatico |
| Kinesis Stream | 20% | Ingesta en tiempo real |
| Terraform IaC | 25% | Todo como codigo |
| Documentacion | 10% | README claro, comandos funcionan |

---

## Recursos

### Documentacion Oficial

- [LocalStack Docs](https://docs.localstack.cloud/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/)

### Herramientas Utiles

- **awscli-local:** `pip install awscli-local`
- **tflocal:** `pip install terraform-local` (wrapper Terraform para LocalStack)
- **LocalStack Desktop:** GUI para LocalStack (opcional)

---

**Curso:** Big Data con Python - De Cero a Produccion
**Profesor:** Juan Marcelo Gutierrez Miranda | @TodoEconometria
**Hash ID:** 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
**Metodologia:** Ejercicios progresivos con datos reales y herramientas profesionales

**Referencias academicas:**
- Amazon Web Services. (2024). AWS Well-Architected Framework. AWS Documentation.
- HashiCorp. (2024). Terraform: Infrastructure as Code. HashiCorp Learn.
- LocalStack. (2024). LocalStack Documentation. LocalStack Cloud.
- Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly Media.
- Reis, J., & Housley, M. (2022). Fundamentals of Data Engineering. O'Reilly Media.
