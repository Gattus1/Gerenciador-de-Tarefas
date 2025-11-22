Gerenciador de Tarefas 📝

Projeto acadêmico desenvolvido para aplicação prática de lógica, modularização, documentação e persistência de dados em Python.

Sobre o Projeto
Este sistema permite gerenciar tarefas com controle de **prioridade**, **status**, **origem**, **datas**, **arquivamento automático**, além de **persistência em arquivos JSON** e **exclusão lógica**.

O projeto segue rigorosamente todos os requisitos técnicos solicitados, incluindo:

* Modularização completa
* Uso de variáveis globais quando necessário
* Funções com docstrings detalhadas
* Tratamento de exceções
* Validação de dados
* Arquivamento automático após 7 dias
* Criação automática de arquivos JSON
* Apenas uma tarefa “Fazendo” por vez
* Debug prints para facilidade de testes
* Relatórios completos

📂 Estrutura dos Arquivos

```
|-- gerenciador_tarefas.py
|-- tarefas.json
|-- tarefas_arquivadas.json
|-- README.md
|-- Projeto_Gerenciador_Tarefas.pptx
```
🏗 Tecnologias Utilizadas

* **Python 3.8+**
* **json** (persistência de dados)
* **datetime** (manipulação de datas)
* **os** (verificação/criação de arquivos)

🚀 Funcionalidades

✔ Criar tarefas

Solicita dados do usuário e cria tarefas com ID único automático.

✔ Buscar tarefas por urgência

Retorna sempre a tarefa mais urgente disponível.

✔ Alterar prioridade

Com validação completa das opções existentes.

✔ Concluir tarefa

Adiciona data de conclusão e calcula tempo total no relatório.

✔ Excluir logicamente

O item continua salvo, mas marcado como “Excluído”.

✔ Arquivamento automático

Tarefas concluídas há mais de **7 dias** são movidas para *tarefas_arquivadas.json*.

✔ Relatórios

* Exibe informações completas
* Calcula tempo de execução
* Filtra tarefas arquivadas

✔ Persistência JSON

Arquivos criados automaticamente se não existirem.

🧪 Debug e Testes

Todas as funções exibem um print inicial:

```
Executando a função nome_da_funcao
```

Isso facilita rastrear a execução durante testes.

▶️ Como Executar o Projeto

1. Certifique-se de ter **Python 3.8+** instalado.
2. Baixe os arquivos do repositório.
3. Abra o terminal na pasta do projeto.
4. Execute:

```
python gerenciador_tarefas.py
```

5. Navegue pelo menu digital.

---

👥 Integrantes do Grupo

Preencha os nomes do seu grupo:

* Nome 1
* Nome 2
* Nome 3

🎞 Slides da Apresentação

O arquivo `.pptx` gerado automaticamente está incluído no repositório.

Você também pode baixar aqui:
👉 **Projeto_Gerenciador_Tarefas.pptx**

📜 Licença
Projeto de uso acadêmico. Livre para estudo e modificação.

🧑‍💻 Autor(es)

Grupo de Desenvolvimento – Projeto de Aplicação
