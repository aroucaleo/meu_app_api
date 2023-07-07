# API - GESTOR DE CRISES

Este projeto tem como objetivo desenvolvimento de um getor de crises empresarial

 **PUC-RIO - Desenvolvimento Full Stack Básico Sprint I - por: Leonardo Arouca** 

---

## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É expressamente necessário o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Comando para instalar as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para execução da API rodar o comando abaixo:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Quando houver mudanças no código fonte , para reiniciar o servidor , deverá ser executado o parâmetro reload, que reiniciará o servidor automaticamente. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no seu navegador visualizar o status da API em execução.
