# PitStop Manager

PitStop Manager é um sistema simples, open source e intuitivo para gestão de oficinas mecânicas. O projeto nasceu da necessidade real de facilitar o dia a dia de quem administra uma oficina, inspirado diretamente nos desafios enfrentados pelo meu pai ao lidar com o controle de clientes, agendamentos e organização do negócio.

## Por que o PitStop Manager?

Muitos softwares de gestão disponíveis no mercado são complexos, caros ou exigem um longo tempo de aprendizado. O PitStop Manager foi criado para ser o oposto disso: uma solução fácil, direta e acessível, que qualquer pessoa pode usar sem precisar de treinamentos extensos ou manuais complicados.

## Origem da Ideia

A ideia surgiu ao unir o útil ao agradável: além de resolver um problema familiar, o projeto também serviu como base para um trabalho acadêmico na disciplina de Programação Web. Apesar do objetivo final ser um sistema desktop ou mobile, a versão web foi escolhida como MVP (Produto Mínimo Viável) para validar a proposta e entender, na prática, se a solução realmente faz sentido para o público-alvo.

## Principais Características

- Cadastro e controle de clientes
- Agendamento de serviços
- Gestão de veículos, produtos e serviços
- Interface simples, limpa e intuitiva
- Código aberto e fácil de adaptar

## Para quem é o PitStop Manager?

Para qualquer oficina que busca uma solução descomplicada para organizar o negócio, sem precisar investir em ferramentas caras ou complexas. O foco é ser útil para quem realmente precisa, sem firulas e sem burocracia.

## Instalação e Configuração

### Pré-requisitos
- Python 3.13 ou superior
- [uv](https://docs.astral.sh/uv/) (obrigatório)
- Git

### Instalando o uv

Se você ainda não tem o uv instalado:

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configuração do projeto

1. **Clone o repositório**
   ```bash
   git clone https://github.com/LucasLimaT/PitStopManager.git
   cd pitstopmanager
   ```

2. **Instale dependências e configure o ambiente**
   ```bash
   uv sync
   ```

3. **Configure o banco de dados**
   ```bash
   task migrate
   ```

4. **Crie um superusuário (opcional)**
   ```bash
   task createsuperuser
   ```

5. **Execute o servidor**
   ```bash
   task run
   ```

6. **Acesse o sistema**
   Abra seu navegador e vá para `http://localhost:8000`

## Como Contribuir

O PitStop Manager é um projeto aberto e toda contribuição é bem-vinda! Se você acredita que softwares podem ser simples e úteis, aqui está como você pode ajudar:

### Primeiros Passos para Contribuir

1. **Fork o repositório**
   - Clique em "Fork" no GitHub para criar sua própria cópia

2. **Clone seu fork**
   ```bash
   git clone https://github.com/seu-usuario/pitstopmanager.git
   cd pitstopmanager
   ```

3. **Configure o ambiente de desenvolvimento**
   ```bash
   uv sync --group dev
   ```

4. **Crie uma branch para sua feature**
   ```bash
   git switch -c minha-nova-feature
   ```

### Desenvolvimento

- Execute os testes antes de fazer mudanças:
  ```bash
  task test
  ```

- Mantenha o código formatado:
  ```bash
  task format
  ```

- Verifique a qualidade do código:
  ```bash
  task lint
  ```

### Enviando sua Contribuição

1. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

2. **Push para seu fork**
   ```bash
   git push origin minha-nova-feature
   ```

3. **Abra um Pull Request**
   - Descreva claramente o que sua mudança faz
   - Explique por que é útil
   - Inclua capturas de tela se for uma mudança visual

### Tipos de Contribuição

- **Correção de bugs** - Sempre bem-vindas!
- **Novas funcionalidades** - Discuta primeiro em uma issue
- **Melhorias na documentação** - Documentação clara é essencial
- **Testes** - Ajude a manter a qualidade do código
- **Tradução** - Torne o sistema acessível para mais pessoas
- **Feedback e sugestões** - Compartilhe sua experiência de uso

### Reportando Problemas

Encontrou um bug? Abra uma [issue](https://github.com/seu-usuario/pitstopmanager/issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots se aplicável

### Dúvidas?

Não hesite em abrir uma issue para tirar dúvidas ou sugerir melhorias. O objetivo é tornar o PitStop Manager cada vez mais útil para quem realmente precisa.

---
