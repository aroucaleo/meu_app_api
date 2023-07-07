from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Crise
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Gestor de crises empresarial", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
crise_tag = Tag(name="Gestor de Crises", description="Adição, visualização e remoção de crises à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/crise', tags=[crise_tag],
          responses={"200": CriseViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_crise(form: CriseSchema):
    """Adiciona uma nova Crise à base de dados

    Retorna uma representação das crises.
    """
    crise = Crise(
        data_crise=form.data_crise,
        nome=form.nome,
        prazo=form.prazo,
        detalhes=form.detalhes
        )
    logger.debug(f"Adicionando uma crise de nome: '{crise.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(crise)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado uma crise de nome: '{crise.nome}'")
        return apresenta_crise(crise), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Uma crise do mesmo nome já foi salva na base :/"
        logger.warning(f"Erro ao adicionar uma crise '{crise.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar uma nova crise :/"
        logger.warning(f"Erro ao adicionar uma crise '{crise.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/crises', tags=[crise_tag],
         responses={"200": ListagemCriseSchema, "404": ErrorSchema})
def get_crise():
    """Faz a busca por todas as Crises cadastradas

    Retorna uma representação da listagem de crises.
    """
    logger.debug(f"Coletando crises da base de dados ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    crises = session.query(Crise).order_by(Crise.prazo.asc()).all()

    if not crises:
        # se não há crises cadastradas
        return {"crises": []}, 200
    else:
        logger.debug(f"%d crises econtrados" % len(crises))
        # retorna a representação de uma crise
        print(crises)
        return apresenta_crises(crises), 200


@app.delete('/crise', tags=[crise_tag],
            responses={"200": CriseDelSchema, "404": ErrorSchema})
def del_crise(query: CriseBuscaSchema):
    """Deleta uma  Crise a partir do nome da crise informada

    Retorna uma mensagem de confirmação da remoção.
    """
    crise_nome = unquote(unquote(query.nome))
    print(crise_nome)
    logger.debug(f"Deletando dados sobre crise #{crise_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Crise).filter(Crise.nome == crise_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado crise #{crise_nome}")
        return {"mesage": "Crise removida", "id": crise_nome}
    else:
        # se a crise não foi encontrado
        error_msg = "Crise não encontrado na base :/"
        logger.warning(f"Erro ao deletar crise #'{crise_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
