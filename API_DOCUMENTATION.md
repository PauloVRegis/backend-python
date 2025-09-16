# API Documentation - SmartForce Go

## Status Atual

A API do SmartForce foi migrada com sucesso do Python/FastAPI para Go/Gin e está funcionando perfeitamente na porta 8000.

## Endpoints Disponíveis

### Públicos (sem autenticação)

- **GET /** - Informações da API e endpoints disponíveis
- **GET /health** - Health check do sistema
- **GET /metrics** - Métricas do Prometheus
- **GET /docs** - Status da documentação (temporário)

### Autenticação

- **POST /api/v1/auth/login** - Login de usuário
- **POST /api/v1/auth/register** - Registro de novo usuário
- **POST /api/v1/auth/refresh** - Refresh do token JWT
- **GET /api/v1/auth/me** - Informações do usuário autenticado

### Usuários (autenticado)

- **GET /api/v1/users** - Listar usuários
- **GET /api/v1/users/:id** - Obter usuário específico
- **POST /api/v1/users** - Criar usuário
- **PUT /api/v1/users/:id** - Atualizar usuário
- **DELETE /api/v1/users/:id** - Deletar usuário

### Exercícios

- **GET /api/v1/exercises** - Listar exercícios (público)
- **GET /api/v1/exercises/:id** - Obter exercício específico (público)
- **GET /api/v1/exercises/muscle-groups** - Listar grupos musculares (público)
- **POST /api/v1/exercises** - Criar exercício (autenticado)
- **PUT /api/v1/exercises/:id** - Atualizar exercício (autenticado)
- **DELETE /api/v1/exercises/:id** - Deletar exercício (autenticado)

### Professores

- **GET /api/v1/professors** - Listar professores (público)
- **GET /api/v1/professors/:id** - Obter professor específico (público)
- **POST /api/v1/professors** - Criar professor (autenticado)
- **PUT /api/v1/professors/:id** - Atualizar professor (autenticado)
- **DELETE /api/v1/professors/:id** - Deletar professor (autenticado)

### Treinos

- **GET /api/v1/trainings** - Listar treinos (autenticado)
- **GET /api/v1/trainings/:id** - Obter treino específico (autenticado)
- **POST /api/v1/trainings** - Criar treino (autenticado)
- **PUT /api/v1/trainings/:id** - Atualizar treino (autenticado)
- **DELETE /api/v1/trainings/:id** - Deletar treino (autenticado)
- **POST /api/v1/trainings/:id/exercises** - Adicionar exercício ao treino (autenticado)

## Documentação Swagger/OpenAPI

### ✅ Status Atual - ATIVO
A documentação Swagger está **FUNCIONANDO** e disponível em:
- **Interface Web**: http://localhost:8000/docs/index.html
- **Especificação JSON**: http://localhost:8000/docs/swagger.json
- **Especificação YAML**: http://localhost:8000/docs/swagger.yaml

### Arquivos de Documentação Gerados
- `/docs/docs.go` - Documentação Go gerada
- `/docs/swagger.json` - Especificação OpenAPI em JSON
- `/docs/swagger.yaml` - Especificação OpenAPI em YAML

### Acesso à Documentação

1. **Interface Swagger UI**: 
   ```
   http://localhost:8000/docs/index.html
   ```
   Interface web interativa para testar todos os endpoints da API

2. **API JSON**:
   ```
   http://localhost:8000/docs/swagger.json
   ```
   Especificação completa da API em formato JSON

3. **API YAML**:
   ```
   http://localhost:8000/docs/swagger.yaml
   ```
   Especificação completa da API em formato YAML

### Dependências Swagger Instaladas

As seguintes versões compatíveis estão sendo usadas:
```go
github.com/swaggo/gin-swagger@v1.3.0
github.com/swaggo/files@v0.0.0-20210815190702-a29dd2bc99b2
```

### Regenerar Documentação

Para atualizar a documentação após mudanças no código:
```bash
~/go/bin/swag init -g main.go -o ./docs
```

### Funcionalidades Disponíveis

✅ **Todos os endpoints documentados**
✅ **Modelos de dados com validação**
✅ **Autenticação JWT documentada**
✅ **Exemplos de request/response**
✅ **Interface interativa para testes**
✅ **Download das especificações**

## Modelos de Dados

### User
- ID, Email, Name, PasswordHash
- Timestamps: CreatedAt, UpdatedAt, DeletedAt

### Professor
- ID, Name, Email, Phone, Bio, Specialties
- Timestamps: CreatedAt, UpdatedAt, DeletedAt

### Exercise
- ID, Name, Description, MuscleGroup, Equipment, Difficulty
- Timestamps: CreatedAt, UpdatedAt, DeletedAt

### Training
- ID, Name, Description, UserID, ProfessorID
- Relationship: User, Professor, TrainingExercises
- Timestamps: CreatedAt, UpdatedAt, DeletedAt

### TrainingExercise
- ID, TrainingID, ExerciseID, Sets, Reps, Weight, RestTime, Notes
- Relationships: Training, Exercise

### TrainingRegistration
- ID, TrainingID, UserID, RegisteredAt
- Relationships: Training, User

## Autenticação

- **Tipo**: JWT (JSON Web Tokens)
- **Header**: `Authorization: Bearer <token>`
- **Algoritmo**: HS256
- **Expiração**: Configurável via variável de ambiente

## Variáveis de Ambiente

```env
# Database
DB_TYPE=sqlite # ou postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smartforce
DB_USER=postgres
DB_PASSWORD=password
DATABASE_URL=sqlite://./smartforce.db

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRATION=24h

# Server
DEBUG=true
PORT=8000

# Cache (Redis)
REDIS_URL=redis://localhost:6379
```

## Teste da API

Para testar a API, você pode usar:

```bash
# Health check
curl http://localhost:8000/health

# Informações da API
curl http://localhost:8000/

# Registrar usuário
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","name":"Teste","password":"123456"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","password":"123456"}'

# Listar exercícios (público)
curl http://localhost:8000/api/v1/exercises

# Listar professores (público)
curl http://localhost:8000/api/v1/professors
```

## Compatibilidade

✅ **Funcional**: API completa migrada e operacional
✅ **Performance**: Melhor performance que a versão Python
✅ **Recursos**: Todos os endpoints migrados
✅ **Documentação**: Swagger/OpenAPI funcionando perfeitamente
✅ **Docker**: Dockerfile pronto para deployment
✅ **Monitoring**: Métricas Prometheus funcionais
