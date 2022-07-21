import traceback
import spacy as sp
import wikipedia
import falcon

nlp = sp.load('pt_core_news_sm')
wikipedia.set_lang("pt")

class SeparadorResource():

  def on_post(self, req, resp):
    try:

      body = req.media

      source = body['source']
      text = body['text']

      if source == 'w':
        text = SeparadorUtils.get_from_wikipedia(text)
      elif source == 'a':
        text = SeparadorUtils.get_from_file(text)
      elif source == 'i':
        text = text

      if not text or source not in ('w', 'a', 'i'):
        resp.media = {
          'success': False,
          'payload': None,
          'error': 'Nenhum texto fornecido'
        }
        resp.status = falcon.HTTP_400
        return

      res = SeparadorUtils.process(text)
      resp.media = {
        'success': True,
        'payload': res,
        'error': None
      }
      resp.status = falcon.HTTP_200
    except Exception as e:
      traceback.print_exc()
      print(str(e), flush=True)
      resp.status = falcon.HTTP_500
    finally:
      print('Separador ended')

class SeparadorUtils:

  @staticmethod
  def get_from_wikipedia(page: str):
    page = wikipedia.page(page)
    content = page.content
    return content

  @staticmethod
  def get_from_file(filename: str):
    file = None
    try:
      file = open(filename, 'r')
      content = file.read()
      return content
    finally:
      if file is not None:
        file.close()

  @staticmethod
  def process(text: str):
    doc = nlp(text)
    # Listar verbos do texto
    verbos = [token.lemma_ for token in doc if token.pos_ == 'VERB']
    print(f"Qtd. de verbos: {len(verbos)}")
    print(f"Verbos: {set(verbos)}")

    # Listar conjunções do texto
    conj = [token.lemma_ for token in doc if token.pos_ == 'CCONJ']
    print(f"Qtd. de conjunções: {len(conj)}")
    print(f"Conjunções: {set(conj)}")

    # Listar substantivos próprios
    sub_prop = [token.lemma_ for token in doc if token.pos_ == 'PROPN']
    print(f"Qtd. de subs. próprios: {len(sub_prop)}")
    print(f"Subs. próprios: {set(sub_prop)}")

    # Listar substantivos comuns
    sub_com = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    print(f"Qtd. de subs. comuns: {len(sub_com)}")
    print(f"Subs. comuns: {set(sub_com)}")

    # Listar pronomes
    pron = [token.lemma_ for token in doc if token.pos_ == 'PRON']
    print(f"Qtd. de pronomes: {len(pron)}")
    print(f"Pronomes: {set(pron)}")

    return {
      'VERB': [len(verbos), list(set(verbos))],
      'CCONJ': [len(conj), list(set(conj))],
      'PROPN': [len(sub_prop), list(set(sub_prop))],
      'NOUN': [len(sub_com), list(set(sub_com))],
      'PRON': [len(pron), list(set(pron))]
    }