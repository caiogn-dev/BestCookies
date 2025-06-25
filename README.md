# BestCookies

BestCookies é uma aplicação web desenvolvida com Django para uma loja virtual de cookies. O sistema permite que usuários naveguem por produtos, adicionem itens ao carrinho, realizem o checkout e gerenciem suas contas.

## Funcionalidades principais
- **Listagem de produtos:** Exibe todos os cookies disponíveis para compra.
- **Detalhes do produto:** Visualize informações detalhadas de cada cookie.
- **Carrinho de compras:** Adicione, visualize e gerencie os itens do carrinho.
- **Checkout:** Finalize a compra dos itens do carrinho.
- **Cadastro e login de usuários:** Crie uma conta, faça login e logout de forma segura.

## Casos de uso
1. **Usuário visitante:**
   - Visualiza a lista de cookies disponíveis.
   - Consulta detalhes de cada produto.
2. **Usuário autenticado:**
   - Adiciona produtos ao carrinho.
   - Visualiza e edita o carrinho de compras.
   - Realiza o checkout e finaliza a compra.
   - Gerencia sua conta (cadastro, login e logout).

## Como rodar o projeto
1. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute as migrações:
   ```bash
   python cookies/manage.py migrate
   ```
4. Inicie o servidor:
   ```bash
   python cookies/manage.py runserver
   ```
5. Acesse em [http://localhost:8000](http://localhost:8000)

---