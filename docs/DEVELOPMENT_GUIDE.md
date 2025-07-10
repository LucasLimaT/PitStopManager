# PitStopManager - Guia de Desenvolvimento

## Setup e Configuração do Ambiente

### Pré-requisitos
- Python 3.13+
- UV (gerenciador de dependências moderno)
- Git
- Editor de código (VS Code recomendado)

### Instalação do Ambiente
```bash
# Clone do repositório
git clone https://github.com/LucasLimaT/PitStopManager.git
cd PitStopManager

# Configuração do ambiente virtual com UV
uv sync

# Executar migrações
task migrate

# Criar superusuário
task createsuperuser

# Executar servidor de desenvolvimento
task run
```

### Comandos Úteis

#### Desenvolvimento
```bash
task run      # Servidor desenvolvimento (port 8000)
task shell    # Shell Django interativo
task check    # Verificações do Django
```

#### Banco de Dados
```bash
task makemigrations    # Criar migrações
task migrate           # Aplicar migrações
task showmigrations    # Mostrar status das migrações
```

#### Qualidade de Código
```bash
uv run task test                   # Executar testes
task collectstatic    # Coletar arquivos estáticos
task dbshell          # Shell do banco de dados
```

#### Formatação e Qualidade de Código
```bash
task format           # Formatação automática e Ordenação de imports
task lint             # Análise estática de código
```

```

## Arquitetura de Desenvolvimento

### Padrões de Código

#### Nomenclatura
```python
# Models: PascalCase
class ServiceOrder(SoftDeleteModel):
    pass

# Fields: snake_case
uuid_id = models.UUIDField(...)
created_at = models.DateTimeField(...)

# Methods: snake_case
def create_service_order(self):
    pass

# Properties: snake_case
@property
def total_amount(self):
    pass

# Constants: UPPER_CASE
STATUS_CHOICES = [
    ('PENDING', 'Pendente'),
    ('IN_PROGRESS', 'Em Andamento'),
]
```

#### Estrutura de Apps
```
apps/
├── core/                      # Funcionalidades base
│   ├── models.py             # TimeStampedModel, SoftDeleteModel, ActiveManager
│   ├── utils.py              # format_phone e outros utilitários
│   ├── views.py              # Views base
│   ├── urls.py               # URLs do core
│   └── admin.py              # Configuração admin base
└── {domain}/                  # App específico do domínio
    ├── models.py             # Modelos do domínio
    ├── views.py              # CRUD do domínio
    ├── forms.py              # Formulários do domínio
    ├── admin.py              # Admin do domínio
    ├── urls.py               # URLs do domínio
    └── migrations/           # Migrações do banco
```

### Boas Práticas Implementadas

#### 1. Models (Exemplo Real do Projeto)
```python
class Vehicle(SoftDeleteModel):
    """
    Modelo para veículos dos clientes
    Implementa soft delete e auditoria temporal
    """
    # UUID para referência externa
    uuid_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True, 
        verbose_name="UUID"
    )
    
    # Relacionamentos sempre com verbose_name
    pk_id_cliente = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Cliente'
    )
    
    # Campos com validação
    placa = models.CharField(
        max_length=8,
        unique=True,
        verbose_name='Placa',
        help_text='Placa do veículo'
    )
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']
        db_table = 'vehicles_vehicle'
    
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
```
        # Validações específicas
    
    def save(self, *args, **kwargs):
        """Hook de salvamento"""
        self.full_clean()  # Força validação
        super().save(*args, **kwargs)
```

#### 2. Views (Exemplo Baseado no Projeto)
```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        return Customer.objects.filter(is_active=True).order_by('nome')

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'customers/customer_form.html'
    fields = ['nome', 'telefone']
    success_url = reverse_lazy('customers:customer_list')
```

#### 3. Forms (Estrutura do Projeto)
```python
from django import forms
from apps.customers.models import Customer
from apps.core.utils import format_phone

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['nome', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
        }
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        return format_phone(telefone)
```

## Fluxos de Desenvolvimento

### Adicionando Nova Funcionalidade

#### 1. Criar Feature Branch
```bash
git switch -c feature/nova-funcionalidade
```

#### 2. Implementar Model (se necessário)
```python
# Em apps/domain/models.py
class NovoModel(SoftDeleteModel):
    """Documentação do modelo"""
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # ... campos específicos
    
    class Meta:
        verbose_name = 'Novo Model'
        verbose_name_plural = 'Novos Models'
        ordering = ['campo_ordenacao']
```

#### 3. Criar e Aplicar Migração
```bash
task makemigrations
task migrate
```

#### 4. Implementar Views
```python
# Em apps/domain/views.py
class NovoModelListView(LoginRequiredMixin, ListView):
    model = NovoModel
    template_name = 'domain/novo_model_list.html'
```

#### 5. Configurar URLs
```python
# Em apps/domain/urls.py
from django.urls import path
from . import views

app_name = 'domain'
urlpatterns = [
    path('novo-model/', views.NovoModelListView.as_view(), name='novo_model_list'),
]
```

#### 6. Criar Templates
```html
<!-- templates/domain/novo_model_list.html -->
{% extends 'base.html' %}
{% block title %}Novo Model - Lista{% endblock %}
{% block content %}
<!-- Conteúdo específico -->
{% endblock %}
```

#### 7. Configurar Admin
```python
# Em apps/domain/admin.py
from django.contrib import admin
from .models import NovoModel

@admin.register(NovoModel)
class NovoModelAdmin(admin.ModelAdmin):
    list_display = ['campo1', 'campo2', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['campo1', 'campo2']
```

#### 8. Escrever Testes
```python
# Em tests/test_domain.py
import pytest
from apps.domain.models import NovoModel

@pytest.mark.django_db
class TestNovoModel:
    def test_create_novo_model(self):
        novo_model = NovoModel.objects.create(
            campo1='valor1',
            campo2='valor2'
        )
        assert novo_model.campo1 == 'valor1'
```

### Workflow de Git

#### Branch Strategy
```bash
main                    # Produção
├── develop            # Desenvolvimento
│   ├── feature/xyz   # Novas funcionalidades
│   ├── bugfix/abc    # Correções
│   └── hotfix/123    # Correções urgentes
```

#### Commit Convention
```bash
# Tipos de commit
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: manutenção

# Exemplos
feat(customers): adicionar validação de CPF
fix(inventory): corrigir cálculo de estoque
docs(readme): atualizar instruções de instalação
```

## Debugging e Troubleshooting

### Debug Local
```python
# Em development.py
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# Configuração do Debug Toolbar
if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### Logging Personalizado
```python
# Em settings/base.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {  # Logs dos nossos apps
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### Problemas Comuns e Soluções

#### 1. Erro de Migração
```bash
# Reset completo das migrações (CUIDADO!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
task makemigrations
task migrate
```

#### 2. Problemas de Dependências
```bash
# Reinstalar ambiente
rm -rf .venv
uv sync
```

#### 3. Problemas de Cache
```bash
# Limpar cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
```

#### 4. Problemas de Estáticos
```bash
# Recompilar estáticos
uv run task collectstatic --clear
```

## Deployment

### Preparação para Produção

#### 1. Variáveis de Ambiente
```bash
# .env.production
SECRET_KEY=sua_secret_key_segura
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgresql://user:pass@localhost/pitstop_prod
SENTRY_DSN=https://...
```

#### 2. Configuração do Servidor
```python
# settings/production.py
import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database PostgreSQL
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

#### 3. Docker Configuration
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar UV
RUN pip install uv

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências Python
RUN uv sync --frozen

# Copiar código
COPY . .

# Coletar arquivos estáticos
RUN uv run task collectstatic --noinput

# Exposar porta
EXPOSE 8000

# Comando de inicialização
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### 4. Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/pitstop
    depends_on:
      - db
    volumes:
      - ./media:/app/media
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: pitstop
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Monitoramento e Manutenção

### Health Checks
```python
# apps/core/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Endpoint para verificar saúde da aplicação"""
    try:
        # Verificar conexão com banco
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
```

### Backup Strategy
```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/pitstop"

# Backup do banco
pg_dump $DATABASE_URL > "$BACKUP_DIR/db_backup_$DATE.sql"

# Backup dos arquivos de media
tar -czf "$BACKUP_DIR/media_backup_$DATE.tar.gz" media/

# Manter apenas últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Monitoramento com Sentry
```python
# settings/production.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
        sentry_logging,
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

## Performance

### Otimização de Queries
```python
# Usando select_related e prefetch_related
ServiceOrder.objects.select_related(
    'customer', 'vehicle', 'mechanic'
).prefetch_related(
    'service_items__service_type',
    'used_parts__product'
)

# Agregações no banco
from django.db.models import Count, Sum
orders_stats = ServiceOrder.objects.aggregate(
    total_orders=Count('id'),
    total_revenue=Sum('labor_total')
)
```

### Cache Strategy
```python
# settings/production.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Uso em views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutos
def dashboard_view(request):
    # View com cache
    pass
```

## 📊 Adequação ao Diagrama ER Atualizado

### Estrutura de Entidades Principais

O desenvolvimento deve seguir rigorosamente a estrutura definida no diagrama ER:

#### 🏢 CLIENTE (Customer Model)
```python
# Campos obrigatórios conforme ER
pk_id = models.AutoField(primary_key=True)      # int - chave primária
uuid_id = models.UUIDField(unique=True)         # UUID único
nome = models.CharField(max_length=100)         # string - nome
telefone = models.CharField(max_length=20)      # string - telefone

# Relacionamento: Um cliente possui vários carros (1:N)
# Acesso: customer.vehicles.all()
```

#### 🚗 CARRO (Vehicle Model)  
```python
# Campos obrigatórios conforme ER
pk_id = models.AutoField(primary_key=True)      # int - chave primária
uuid_id = models.UUIDField(unique=True)         # UUID único
pk_id_cliente = models.ForeignKey(Customer)     # int FK para cliente
marca = models.CharField(max_length=50)         # string - marca
modelo = models.CharField(max_length=50)        # string - modelo
ano = models.IntegerField()                     # int - ano
placa = models.CharField(max_length=8)          # string - placa

# Relacionamento: Pertence a um cliente (N:1)
# Acesso: vehicle.customer
```

#### 🔧 ORDEM_DE_SERVICO (ServiceOrder Model)
```python
# Campos obrigatórios conforme ER
pk_id = models.AutoField(primary_key=True)      # int - chave primária
uuid_id = models.UUIDField(unique=True)         # UUID único
pk_id_carro = models.ForeignKey(Vehicle)        # int FK para carro
data_de_entrega = models.DateField()            # date - entrega
data_de_entrada = models.DateField()            # date - entrada
orcamento = models.IntegerField()               # int - orçamento (centavos)
descricao_concerto = models.TextField()         # string - descrição conserto
descricao_problema = models.TextField()         # string - descrição problema
status = models.CharField(max_length=20)        # string - status
quilometragem = models.FloatField()             # float - quilometragem

# Relacionamento: Pertence a um carro (N:1)
# Acesso: service_order.vehicle, service_order.vehicle.customer
```

#### 📦 PECAS_E_MATERIAIS (Product/UsedPart Models)
```python
# Product (Catálogo)
pk_id = models.AutoField(primary_key=True)      # int - chave primária  
uuid_id = models.UUIDField(unique=True)         # UUID único
nome = models.CharField(max_length=100)         # string - nome
estoque = models.IntegerField()                 # int - quantidade estoque

# UsedPart (Uso em OS)
pk_id = models.AutoField(primary_key=True)      # int - chave primária
uuid_id = models.UUIDField(unique=True)         # UUID único
pk_id_ordem_de_servico = models.ForeignKey(ServiceOrder) # FK para OS
produto = models.ForeignKey(Product)            # FK para produto
quantidade = models.IntegerField()              # int - quantidade usada

# Relacionamento: Utilizada em ordens de serviço (N:1)
# Acesso: used_part.service_order, service_order.used_parts.all()
```

#### 📅 AGENDAMENTO (Appointment Model)
```python
# Campos obrigatórios conforme ER
pk_id = models.AutoField(primary_key=True)      # int - chave primária
uuid_id = models.UUIDField(unique=True)         # UUID único
pk_id_ordem_de_servico = models.ForeignKey(ServiceOrder) # FK para OS
pk_id_carro = models.ForeignKey(Vehicle)        # FK para carro
data_do_agendamento = models.DateTimeField()    # timestamp - data/hora
responsavel = models.CharField(max_length=100)  # string - responsável

# Relacionamentos: Pertence a OS e Carro (N:1)
# Acesso: appointment.service_order, appointment.vehicle
```

### Padrões de Desenvolvimento para ER

#### 1. Nomenclatura de Campos
- **pk_id**: Sempre `id = models.AutoField(primary_key=True)`
- **uuid_id**: Sempre `uuid_id = models.UUIDField(unique=True)`
- **FKs**: Usar nome descritivo: `customer`, `vehicle`, `service_order`

#### 2. Relacionamentos
```python
# ForeignKey sempre com related_name
customer = models.ForeignKey(
    Customer,
    on_delete=models.CASCADE,
    related_name='vehicles',  # customer.vehicles.all()
    verbose_name='Cliente'
)

# Acesso aos relacionamentos
vehicle.customer                    # N:1 direto
customer.vehicles.all()            # 1:N reverso
service_order.used_parts.all()     # 1:N com peças
```

#### 3. Validações Específicas
```python
def clean(self):
    """Validações específicas por entidade"""
    # CLIENTE: Validar CPF/CNPJ
    if self.tipo_pessoa == 'PF':
        self.documento = validate_cpf(self.documento)
    
    # VEHICLE: Validar ano e placa
    if self.ano < 1900 or self.ano > timezone.now().year + 1:
        raise ValidationError('Ano inválido')
    
    # SERVICE_ORDER: Validar datas lógicas  
    if self.data_de_entrega <= self.data_de_entrada:
        raise ValidationError('Data de entrega deve ser posterior à entrada')
```

## 📚 Referencias

### Documentação Django
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Best Practices](https://djangobook.com/)
- [Samuel Gonçalves (canal no youtube sobre o Django)](https://www.youtube.com/@SamuelGoncalvesPython/videos)
- [Codepen (alguns exemplos de components)](codepen.io)
- [Slides e videos disponibilizados no ava e no suap](https://ava.cba.ifmt.edu.br/pluginfile.php/476549/mod_resource/content/6/Introdu%C3%A7%C3%A3o%20ao%20Django%20-%20oficial.pdf)
- [Bootstrap official docs](https://getbootstrap.com/docs/5.3/components/card/)

### Ferramentas de Desenvolvimento
- **IDE**: VS Code
- **VS Code Extensions**: Python, Django, GitLens, Auto Rename Tag
- **Controle de Versão**: Git + GitHub
- **Database**: SQLite
- **Gerenciador de Dependências**: UV (Python package manager)
- **Framework**: Django 5.2
- **Linguagem**: Python 3.13
- **Templates**: HTML5 + Bootstrap 5.3.0 (CSS framework) + JavaScript (Vanilla)
- **CSS Framework**: Bootstrap 5.3.0 (via CDN) + CSS customizado responsivo
- **Icons**: Font Awesome 6.4.0 (via CDN)
- **Form Enhancement**: django-widget-tweaks
- **Image Processing**: Pillow
- **Configuration**: os.getenv() (variáveis de ambiente nativas do Python)
- **Code Quality**: Black (formatação), isort (imports), flake8 (linting)
- **Task Automation**: taskipy (via pyproject.toml)

### Padrões de Código
- **PEP 8**: Guia de estilo Python
- **Django Coding Style**: Convenções Django
- **Clean Code**: Princípios de código limpo

---

*Última atualização: 02/07/2025*
