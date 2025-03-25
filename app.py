from flask import Flask, render_template, request, send_file, redirect
import pdfkit
import io
import platform
import json
import os
import signal
import sys
import threading

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para mensagens flash

# Dicionário de temas
temas = {
    1: "Você conhece bem a Deus?",
    2: "Você vai sobreviver aos últimos dias?",
    3: "Você está avançando com a organização unida de Jeová?",
    4: "Que provas temos de que Deus existe?",
    5: "Você pode ter uma família feliz!",
    6: "O dilúvio dos dias de Noé e você",
    7: "Imite a misericórdia de Jeová",
    8: "Viva para fazer a vontade de Deus",
    9: "Escute e faça o que a Bíblia diz",
    10: "Seja honesto em tudo",
    11: "Imite a Jesus e não faça parte do mundo",
    12: "Deus quer que você respeite quem tem autoridade",
    13: "Qual o ponto de vista de Deus sobre o sexo e o casamento?",
    14: "Um povo puro e limpo honra a Jeová",
    15: "‘Faça o bem a todos’",
    16: "Seja cada vez mais amigo de Jeová",
    17: "Glorifique a Deus com tudo o que você tem",
    18: "Faça de Jeová a sua fortaleza",
    19: "Como você pode saber seu futuro?",
    20: "Chegou o tempo de Deus governar o mundo?",
    21: "Dê valor ao seu lugar no Reino de Deus",
    22: "Você está usando bem o que Jeová lhe dá?",
    23: "A vida tem objetivo",
    24: "Você encontrou “uma pérola de grande valor”?",
    25: "Lute contra o espírito do mundo",
    26: "Você é importante para Deus?",
    27: "Como construir um casamento feliz",
    28: "Mostre respeito e amor no seu casamento",
    29: "As responsabilidades e recompensas de ter filhos",
    30: "Como melhorar a comunicação na família",
    31: "Você tem consciência da sua necessidade espiritual?",
    32: "Como lidar com as ansiedades da vida",
    33: "Quando vai existir verdadeira justiça?",
    34: "Você vai ser marcado para sobreviver?",
    35: "É possível viver para sempre? O que você precisa fazer?",
    36: "Será que a vida é só isso?",
    37: "Obedecer a Deus é mesmo a melhor coisa a fazer?",
    38: "Como você pode sobreviver ao fim do mundo?",
    39: "Jesus Cristo vence o mundo — Como e quando?",
    40: "O que vai acontecer em breve?",
    41: "Fiquem parados e vejam como Jeová os salvará",
    42: "O amor pode vencer o ódio?",
    43: "Tudo o que Deus nos pede é para o nosso bem",
    44: "Como os ensinos de Jesus podem ajudar você?",
    45: "Continue andando no caminho que leva à vida",
    46: "Fortaleça sua confiança em Jeová",
    47: "‘Tenha fé nas boas novas’",
    48: "Seja leal a Deus mesmo quando for testado",
    49: "Será que um dia a Terra vai ser limpa?",
    50: "Como sempre tomar as melhores decisões",
    51: "Será que a verdade da Bíblia está mudando a sua vida?",
    52: "Quem é o seu Deus?",
    53: "Você pensa como Deus?",
    54: "Fortaleça sua fé em Deus e em suas promessas",
    55: "Você está fazendo um bom nome perante Deus?",
    56: "Existe um líder em quem você pode confiar?",
    57: "Como suportar perseguição",
    58: "Quem são os verdadeiros seguidores de Cristo?",
    59: "Ceifará o que semear",
    60: "Você tem um objetivo na vida?",
    61: "Nas promessas de quem você confia?",
    62: "Onde encontrar uma esperança real para o futuro?",
    63: "Tem você espírito evangelizador?",
    64: "Como você pode ter paz verdadeira?",
    65: "Você está preparado para o futuro?",
    66: "O que a Bíblia diz sobre a vida após a morte?",
    67: "Como lidar com a dor e a perda?",
    68: "Você está vivendo de acordo com a vontade de Deus?",
    69: "Como a oração pode mudar sua vida?",
    70: "Você está se aproximando de Jeová?",
    71: "Como a Bíblia pode ajudar em tempos difíceis?",
    72: "Você está fazendo a diferença no mundo?",
    73: "Como ser um bom amigo?",
    74: "Você está cuidando do seu corpo?",
    75: "Como encontrar alegria na vida?",
    76: "Você está preparado para enfrentar desafios?",
    77: "Como a fé pode transformar sua vida?",
    78: "Você está vivendo com propósito?",
    79: "Como a gratidão pode mudar sua perspectiva?",
    80: "Você está fazendo escolhas sábias?",
    81: "Como lidar com a pressão dos colegas?",
    82: "Você está se comunicando bem com os outros?",
    83: "Como a Bíblia pode ajudar em relacionamentos?",
    84: "Você está investindo no seu crescimento pessoal?",
    85: "Como ser um líder eficaz?",
    86: "Você está aprendendo com seus erros?",
    87: "Como a humildade pode beneficiar sua vida?",
    88: "Você está buscando a verdade?",
    89: "Como a fé pode ajudar em momentos de dúvida?",
    90: "Você está se preparando para o futuro?",
    91: "Como a esperança pode mudar sua vida?",
    92: "Você está vivendo em harmonia com os outros?",
    93: "Como a compaixão pode transformar o mundo?",
    94: "Você está fazendo a diferença na sua comunidade?",
    95: "Como a paciência pode melhorar seus relacionamentos?",
    96: "Você está cuidando do seu bem-estar emocional?",
    97: "Como a sabedoria pode guiar suas decisões?",
    98: "Você está se esforçando para ser melhor?",
    99: "Como a fé pode ajudar em tempos de crise?",
    100: "Você está buscando a paz interior?",
    101: "Como a bondade pode impactar sua vida?",
    102: "Você está vivendo de acordo com seus valores?",
    103: "Como a perseverança pode levar ao sucesso?",
    104: "Você está se cercando de pessoas positivas?",
    105: "Como a honestidade pode fortalecer relacionamentos?",
    106: "Você está aprendendo a perdoar?",
    107: "Como a generosidade pode enriquecer sua vida?",
    108: "Você está se dedicando ao seu desenvolvimento espiritual?",
    109: "Como a fé pode ajudar a superar medos?",
    110: "Você está buscando a verdadeira felicidade?",
    111: "Como a disciplina pode levar ao sucesso?",
    112: "Você está se preparando para o futuro com sabedoria?",
    113: "Como a fé pode ajudar a encontrar paz interior?",
    114: "Você está vivendo de acordo com seus princípios?",
    115: "Como a empatia pode melhorar suas interações?",
    116: "Você está se esforçando para ser um bom ouvinte?",
    117: "Como a reflexão pode ajudar no autoconhecimento?",
    118: "Você está buscando a sabedoria em suas decisões?",
    119: "Como a fé pode ajudar a superar a dúvida?",
    120: "Você está se dedicando a aprender mais sobre si mesmo?",
    121: "Como a oração pode fortalecer sua conexão com Deus?",
    122: "Você está vivendo de forma autêntica?",
    123: "Como a gratidão pode mudar sua vida?",
    124: "Você está se esforçando para ser mais gentil?",
    125: "Como a fé pode ajudar a enfrentar desafios?",
    126: "Você está buscando a verdade em sua vida?",
    127: "Como a esperança pode inspirar você?",
    128: "Você está se dedicando a ajudar os outros?",
    129: "Como a fé pode trazer paz em tempos difíceis?",
    130: "Você está vivendo com propósito e intenção?",
    131: "Como a bondade pode impactar o mundo ao seu redor?",
    132: "Você está se esforçando para ser mais compreensivo?",
    133: "Como a fé pode ajudar a superar obstáculos?",
    134: "Você está buscando a felicidade em sua vida?",
    135: "Como a disciplina pode levar a resultados positivos?",
    136: "Você está se cercando de influências positivas?",
    137: "Como a honestidade pode transformar suas relações?",
    138: "Você está aprendendo a valorizar o que realmente importa?",
    139: "Como a generosidade pode enriquecer sua vida?",
    140: "Você está se dedicando a ajudar os necessitados?",
    141: "Como a fé pode ajudar a encontrar significado na vida?",
    142: "Você está vivendo de forma consciente?",
    143: "Como a gratidão pode melhorar seu bem-estar?",
    144: "Você está se esforçando para ser mais gentil com os outros?",
    145: "Como a fé pode ajudar a superar a tristeza?",
    146: "Você está buscando a verdade em suas crenças?",
    147: "Como a esperança pode motivá-lo a seguir em frente?",
    148: "Você está se dedicando a cultivar relacionamentos saudáveis?",
    149: "Como a fé pode trazer clareza em tempos de confusão?",
    150: "Você está vivendo com integridade e honestidade?",
    151: "Como a empatia pode melhorar sua vida social?",
    152: "Você está se esforçando para ser um bom amigo?",
    153: "Como a reflexão pode ajudar a entender suas emoções?",
    154: "Você está buscando a sabedoria em suas experiências?",
    155: "Como a fé pode ajudar a encontrar paz em meio ao caos?",
    156: "Você está se dedicando a aprender com seus erros?",
    157: "Como a oração pode trazer conforto em momentos difíceis?",
    158: "Você está vivendo de forma autêntica e verdadeira?",
    159: "Como a gratidão pode mudar sua perspectiva de vida?",
    160: "Você está se esforçando para ser mais solidário?",
    161: "Como a fé pode ajudar a encontrar seu propósito?",
    162: "Você está buscando a verdade em suas ações?",
    163: "Como a esperança pode inspirar suas escolhas?",
    164: "Você está se dedicando a fazer a diferença na vida dos outros?",
    165: "Como a fé pode trazer conforto em tempos difíceis?",
    166: "Você está vivendo com intenção e propósito?",
    167: "Como a bondade pode impactar sua comunidade?",
    168: "Você está se esforçando para ser mais paciente?",
    169: "Como a fé pode ajudar a enfrentar desafios diários?",
    170: "Você está buscando a felicidade em suas relações?",
    171: "Como a disciplina pode levar a um estilo de vida saudável?",
    172: "Você está se cercando de pessoas que o inspiram?",
    173: "Como a honestidade pode fortalecer sua reputação?",
    174: "Você está aprendendo a perdoar a si mesmo?",
    175: "Como a generosidade pode enriquecer sua vida?",
    176: "Você está se dedicando a ajudar os necessitados?",
    177: "Como a fé pode ajudar a encontrar significado na vida?",
    178: "Você está vivendo de forma consciente?",
    179: "Como a gratidão pode melhorar seu bem-estar?",
    180: "Você está se esforçando para ser mais gentil com os outros?",
    181: "Como a fé pode ajudar a superar a tristeza?",
    182: "Você está buscando a verdade em suas crenças?",
    183: "Como a esperança pode motivá-lo a seguir em frente?",
    184: "Você está se dedicando a cultivar relacionamentos saudáveis?",
    185: "Como a fé pode trazer clareza em tempos de confusão?",
    186: "Você está vivendo com integridade e honestidade?",
    187: "Como a empatia pode melhorar sua vida social?",
    188: "Você está se esforçando para ser um bom amigo?",
    189: "Como a reflexão pode ajudar a entender suas emoções?",
    190: "Você está buscando a sabedoria em suas experiências?",
    191: "Como a fé pode ajudar a encontrar paz em meio ao caos?",
    192: "Você está se dedicando a aprender com seus erros?",
    193: "Como a oração pode trazer conforto em momentos difíceis?",
    194: "Você está vivendo de forma autêntica e verdadeira?",
    195: "Como a gratidão pode mudar sua perspectiva de vida?",
    196: "Você está se esforçando para ser mais solidário?",
    197: "Como a fé pode ajudar a encontrar seu propósito?",
    198: "Você está buscando a verdade em suas ações?",
    199: "Como a esperança pode inspirar suas escolhas?",
    200: "Você está se dedicando a fazer a diferença na vida dos outros?"
}

# Caminho do arquivo para salvar a contagem
CONTAGEM_FILE = 'contagem.json'

# Função para carregar a contagem do arquivo
def carregar_contagem():
    if os.path.exists(CONTAGEM_FILE):
        with open(CONTAGEM_FILE, 'r') as f:
            contagem_salva = json.load(f)
            # Garante que todos os temas estejam no dicionário, mesmo que não tenham sido selecionados
            return {int(key): contagem_salva.get(str(key), 0) for key in temas.keys()}
    else:
        return {key: 0 for key in temas.keys()}

# Função para salvar a contagem no arquivo
def salvar_contagem(contagem):
    with open(CONTAGEM_FILE, 'w') as f:
        json.dump(contagem, f)

# Carrega a contagem ao iniciar o servidor
contagem_temas = carregar_contagem()

# Configuração do pdfkit para funcionar em Windows e Linux
if platform.system() == "Windows":
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
else:
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

@app.route('/', methods=['GET', 'POST'])
def index():
    tema_selecionado = None
    if request.method == 'POST':
        tema_selecionado = request.form.get('tema')
        if tema_selecionado:
            contagem_temas[int(tema_selecionado)] += 1
            salvar_contagem(contagem_temas)  # Salva a contagem após cada alteração
    return render_template('index.html', tema=tema_selecionado, temas=temas, contagem_temas=contagem_temas)

@app.route('/zerar_contagens', methods=['GET'])
def zerar_contagens():
    global contagem_temas
    contagem_temas = {key: 0 for key in temas.keys()}
    salvar_contagem(contagem_temas)  # Salva a contagem zerada
    return redirect('/')

@app.route('/gerar_pdf', methods=['GET'])
def gerar_pdf():
    rendered = render_template('pdf_template.html', contagem_temas=contagem_temas, temas=temas)
    try:
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        pdf_bytes = io.BytesIO(pdf)
        return send_file(
            pdf_bytes,
            as_attachment=True,
            download_name='contagem_temas.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return str(e), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Encerra o servidor Flask."""
    os.kill(os.getpid(), signal.SIGINT)
    return 'Servidor encerrado com sucesso!'
@app.route('/favicon.ico')
def favicon():
    return '', 404

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)  # ✅ Pronto para deploy
    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")
        sys.exit(0)