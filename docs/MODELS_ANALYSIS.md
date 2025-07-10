# PitStopManager - Análise de Modelos (Estado Atual)

## Modelos Django Implementados

O sistema implementa **5 entidades principais** conforme está no código atual:

### **Customer** Model (apps/customers/models.py)

**Campos Implementados**:
- `id` (AutoField) - Chave primária
- `uuid_id` (UUIDField) - UUID único para identificação externa
- `nome` (CharField) - Nome do cliente
- `telefone` (CharField) - Telefone de contato
- `created_at`, `updated_at` - Timestamps automáticos (herdado)
- `is_active`, `deleted_at` - Sistema de soft delete (herdado)

**Funcionalidades Implementadas**:
- Formatação automática de telefone através de `format_phone()`
- Sistema de soft delete herdado de `SoftDeleteModel`
- Validação e ordenação por nome
- Property `display_name` para exibição

### **Vehicle** Model (apps/vehicles/models.py)

**Campos Implementados**:
- `id` (AutoField) - Chave primária
- `uuid_id` (UUIDField) - UUID único para identificação externa
- `pk_id_cliente` (ForeignKey) - Relacionamento com Customer
- `marca` (CharField) - Marca do veículo
- `modelo` (CharField) - Modelo do veículo
- `ano` (PositiveIntegerField) - Ano do veículo
- `placa` (CharField) - Placa única do veículo
- `created_at`, `updated_at` - Timestamps automáticos (herdado)
- `is_active`, `deleted_at` - Sistema de soft delete (herdado)

**Funcionalidades Implementadas**:
- Relacionamento com Customer via ForeignKey
- Validação de placa única
- Sistema de soft delete herdado de `SoftDeleteModel`
- Ordenação por placa
- Representação string incluindo placa, marca e modelo

### **ServiceOrder** Model (apps/services/models.py)

**Campos Implementados**:
- `id` (AutoField) - Chave primária
- `uuid_id` (UUIDField) - UUID único para identificação externa
- `pk_id_carro` (ForeignKey) - Relacionamento com Vehicle
- `data_de_entrada` (DateField) - Data de entrada na oficina
- `data_de_entrega` (DateField) - Data prevista/efetiva de entrega
- `orcamento` (IntegerField) - Valor do orçamento em centavos
- `descricao_problema` (TextField) - Descrição do problema relatado
- `descricao_concerto` (TextField) - Descrição do serviço realizado
- `status` (CharField) - Status da OS com choices
- `quilometragem` (FloatField) - Quilometragem atual do veículo
- `created_at`, `updated_at` - Timestamps automáticos (herdado)
- `is_active`, `deleted_at` - Sistema de soft delete (herdado)

**Funcionalidades Implementadas**:
- Choices para status: PENDENTE, EM_ANDAMENTO, CONCLUIDA, ENTREGUE, CANCELADA
- Property `orcamento_reais` para conversão de centavos para reais
- Relacionamento com Vehicle (acesso ao customer via vehicle.customer)
- Sistema de soft delete herdado de `SoftDeleteModel`
- Ordenação por data de entrada (decrescente)

### **Product** Model (apps/inventory/models.py)

**Campos Implementados**:
- `id` (AutoField) - Chave primária
- `uuid_id` (UUIDField) - UUID único para identificação externa
- `nome` (CharField) - Nome da peça ou material
- `estoque` (IntegerField) - Quantidade em estoque
- `created_at`, `updated_at` - Timestamps automáticos (herdado)
- `is_active`, `deleted_at` - Sistema de soft delete (herdado)

**Funcionalidades Implementadas**:
- Método `update_stock()` para atualização do estoque (add/subtract)
- Validação de estoque insuficiente
- Sistema de soft delete herdado de `SoftDeleteModel`
- Representação string com nome e estoque atual
- Ordenação por nome

### **Appointment** Model (apps/scheduling/models.py)

**Campos Implementados**:
- `id` (AutoField) - Chave primária
- `uuid_id` (UUIDField) - UUID único para identificação externa
- `pk_id_ordem_de_servico` (ForeignKey) - Relacionamento com ServiceOrder
- `pk_id_carro` (ForeignKey) - Relacionamento com Vehicle
- `data_do_agendamento` (DateTimeField) - Data e hora do agendamento
- `responsavel` (CharField) - Nome do responsável pelo agendamento
- `created_at`, `updated_at` - Timestamps automáticos (herdado)
- `is_active`, `deleted_at` - Sistema de soft delete (herdado)

**Funcionalidades Implementadas**:
- Duplo relacionamento com ServiceOrder e Vehicle
- Sistema de soft delete herdado de `SoftDeleteModel`
- Representação string com ID, placa e data formatada
- Ordenação por data do agendamento

## Relacionamentos Implementados

### Relacionamentos N:1 (ForeignKey)
```python
# Customer → Vehicle (1:N)
customer.vehicles.all()  # Todos os veículos do cliente
vehicle.pk_id_cliente    # Cliente do veículo

# Vehicle → ServiceOrder (1:N)  
vehicle.service_orders.all()  # Todas as OS do veículo
service_order.pk_id_carro     # Veículo da OS

# ServiceOrder → Appointment (1:N)
service_order.appointments.all()  # Agendamentos da OS
appointment.pk_id_ordem_de_servico # OS do agendamento

# Vehicle → Appointment (1:N)
vehicle.appointments.all()    # Agendamentos do veículo
appointment.pk_id_carro       # Veículo do agendamento
```

## Modelos Base (apps/core/models.py)

### SoftDeleteModel (Classe Abstrata)
```python
class SoftDeleteModel(models.Model):
    """Modelo abstrato que implementa soft delete"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
```

**Funcionalidades**:
- Timestamps automáticos de criação e atualização
- Sistema de soft delete (marcação como inativo)
- Herdado por todos os modelos principais do sistema

## Utilitários (apps/core/utils.py)

### Formatação de Telefone
```python
def format_phone(phone):
    """Formata telefone para padrão brasileiro"""
    # Remove caracteres não numéricos
    # Aplica máscara (11) 99999-9999
    # Implementação atual simplificada
```

---

*Última atualização: 03/07/2025*
