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
    24: "Você encontrou 'uma pérola de grande valor'?",
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
    45: "Siga o caminho da vida",
    46: "Fortaleça sua confiança em Jeová",
    47: "(Indisponível)",
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
    64: "Você ama os prazeres ou a Deus?",
    65: "Como podemos ser pacíficos num mundo cheio de ódio",
    66: "Você também vai participar na colheita?",
    67: "Medite na Bíblia e nas criações de Jeová",
    68: "‘Continue a perdoar uns aos outros liberalmente’",
    69: "Por que mostrar amor abnegado?",
    70: "Por que Deus merece sua confiança?",
    71: "‘Mantenha-se desperto’ — Por que e como?",
    72: "O amor identifica os cristãos verdadeiros",
    73: "Você tem 'um coração sábio'?",
    74: "Os olhos de Jeová estão em todo lugar",
    75: "Mostre que você apoia o direito de Jeová governar",
    76: "Princípios bíblicos — Podem nos ajudar a lidar com os problemas atuais?",
    77: "“Sempre mostrem hospitalidade”",
    78: "Sirva a Jeová com um coração alegre",
    79: "Você vai escolher ser amigo de Deus?",
    80: "Você baseia sua esperança na ciência ou na Bíblia?",
    81: "Quem está qualificado para fazer discípulos?",
    82: "(Indisponível)",
    83: "Tempo de julgamento da religião",
    84: "Escapará do destino deste mundo?",
    85: "Boas notícias num mundo violento",
    86: "Como orar a Deus e ser ouvido por ele?",
    87: "Qual é a sua relação com Deus?",
    88: "Por que viver de acordo com os padrões da Bíblia?",
    89: "Quem tem sede da verdade, venha!",
    90: "Faça o máximo para alcançar a verdadeira vida!",
    91: "A presença do Messias e seu domínio",
    92: "O papel da religião nos assuntos do mundo",
    93: "Desastres naturais — Quando vão acabar?",
    94: "A religião verdadeira atende às necessidades da sociedade humana",
    95: "Não seja enganado pelo ocultismo",
    96: "O que vai acontecer com as religiões?",
    97: "Permaneçamos inculpes em meio a uma geração pervertida",
    98: "“A cena deste mundo está mudando”",
    99: "Por que você pode confiar na Bíblia",
    100: "Como fazer amizades fortes e verdadeiras",
    101: "Jeová é o “Grandioso Criador”",
    102: "Preste atenção à “palavra profética”",
    103: "Pode-se encontrar alegria em servir a Deus",
    104: "Pais, vocês estão construindo com materiais à prova de fogo?",
    105: "Somos consolados em todas as nossas tribulações",
    106: "Arruinar a Terra provocará retribuição divina",
    107: "Você está treinando bem a sua consciência?",
    108: "Você pode encarar o futuro com confiança!",
    109: "O Reino de Deus está próximo",
    110: "Deus vem primeiro na vida familiar bem sucedida",
    111: "É possível que a humidade seja completamente curada?",
    112: "(Indisponível)",
    113: "Jovens — Como vocês podem ter uma vida feliz?",
    114: "Apreço pelas maravilhas da criação de Deus",
    115: "Como proteger nos contra os laços de Satanás",
    116: "Escolha sabiamente com quem irá associar se!",
    117: "Como vencer o mal com o bem",
    118: "Olhemos os jovens do ponto de vista de Jeová",
    119: "Por que é benéfico que os cristãos vivam separados do mundo",
    120: "Por que se submeter à regência de Deus agora",
    121: "Uma família mundial que será salva da destruição",
    122: "Paz global — De onde virá?",
    123: "Por que os cristãos têm de ser diferentes",
    124: "Razões para crer que a Bíblia é de autoria divina",
    125: "Por que a humanidade precisa de resgate",
    126: "Quem se salvará?",
    127: "O que acontece quando morremos?",
    128: "É o inferno um lugar de tormento ardente?",
    129: "O que a Bíblia diz sobre a Trindade?",
    130: "A Terra permanecerá para sempre",
    131: "(Indisponível)",
    132: "(Indisponível)",
    133: "Tem importância o que cremos sobre a nossa origem?",
    134: "Devem os cristãos guardar o sábado?",
    135: "A santidade da vida e do sangue",
    136: "Será que Deus aprova o uso de imagens na adoração?",
    137: "Ocorreram realmente os milagres da Bíblia?",
    138: "Viva com bom juízo num mundo depravado",
    139: "Sabedoria divina num mundo científico",
    140: "Quem é realmente Jesus Cristo?",
    141: "Quando terão fim os gemidos da criação humana?",
    142: "Por que refugiar se em Jeová",
    143: "Confie no Deus de todo consolo",
    144: "Uma congregação leal sob a liderança de Cristo",
    145: "Quem é semelhante a Jeová, nosso Deus?",
    146: "Use a educação para louvar a Jeová",
    147: "Confie no poder salvador de Jeová",
    148: "Você tem o mesmo conceito de Deus sobre a vida?",
    149: "O que significa 'andar com Deus'?",
    150: "Este mundo está condenado à destruição?",
    151: "Jeová é 'uma altura protetora' para seu povo",
    152: "Armagedom — Por que e quando?",
    153: "Tenha bem em mente o 'atemorizante dia'!",
    154: "O governo humano é pesado na balança",
    155: "Chegou a hora do julgamento de Babilônia?",
    156: "O Dia do Juízo — Tempo de temor ou de esperança?",
    157: "Como os verdadeiros cristãos adornam o ensino divino",
    158: "Seja corajoso e confie em Jeová",
    159: "Como encontrar segurança num mundo perigoso",
    160: "Mantenha a identidade cristã!",
    161: "Por que Jesus sofreu e morreu?",
    162: "Seja liberto deste mundo em escuridão",
    163: "Por que temer o Deus verdadeiro?",
    164: "Será que Deus ainda está no controle?",
    165: "Os valores de quem você preza?",
    166: "Como enfrentar o futuro com fé e coragem",
    167: "Ajamos sabiamente num mundo insensato",
    168: "Você pode sentir se seguro neste mundo atribulado!",
    169: "Por que ser orientado pela Bíblia?",
    170: "Quem está qualificado para governar a humanidade?",
    171: "Poderá viver em paz agora — E para sempre!",
    172: "Que reputação você tem perante Deus?",
    173: "Existe uma religião verdadeira do ponto de vista de Deus?",
    174: "Quem se qualificará para entrar no novo mundo de Deus?",
    175: "O que prova que a Bíblia é autêntica?",
    176: "Quando haverá verdadeira paz e segurança?",
    177: "Onde encontrar ajuda em tempos de aflição?",
    178: "Ande no caminho da integridade",
    179: "Rejeite as fantasias do mundo, empenhe-se pelas realidades do Reino",
    180: "A ressurreição — Por que essa esperança deve ser real para você",
    181: "Já é mais tarde do que você imagina?",
    182: "O que o Reino de Deus está fazendo por nós agora?",
    183: "Desvie seus olhos do que é fútil",
    184: "A morte é o fim de tudo?",
    185: "Será que a verdade influencia sua vida?",
    186: "Sirva em união com o povo feliz de Deus",
    187: "Por que um Deus amoroso permite a maldade?",
    188: "Você confia em Jeová?",
    189: "Ande com Deus e receba bênçãos para sempre",
    190: "Como se cumprirá a promessa de perfeita felicidade familiar",
    191: "Como o amor e a fé vencem o mundo",
    192: "Você está no caminho para a vida eterna?",
    193: "Os problemas de hoje logo serão coisa do passado",
    194: "Como a sabedoria de Deus nos ajuda"
}

# Configuração de caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTAGEM_FILE = os.path.join(BASE_DIR, 'contagem.json')

# Configuração do pdfkit
if platform.system() == "Windows":
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
else:
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

def carregar_contagem():
    try:
        if os.path.exists(CONTAGEM_FILE):
            with open(CONTAGEM_FILE, 'r') as f:
                contagem_salva = json.load(f)
                return {int(k): contagem_salva.get(str(k), 0) for k in temas.keys()}
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {k: 0 for k in temas.keys()}

def salvar_contagem(contagem):
    with open(CONTAGEM_FILE, 'w') as f:
        json.dump({str(k): v for k, v in contagem.items()}, f)

# Inicializa a contagem no início
contagem_temas = carregar_contagem()

@app.route('/', methods=['GET', 'POST'])
def index():
    global contagem_temas
    temas_selecionados = []
    
    if request.method == 'POST':
        temas_selecionados = request.form.getlist('temas')
        if temas_selecionados:
            for tema in temas_selecionados:
                if tema.isdigit():
                    tema_id = int(tema)
                    if tema_id in contagem_temas:
                        contagem_temas[tema_id] += 1
            salvar_contagem(contagem_temas)
    
    return render_template('index.html', 
                         temas=temas, 
                         contagem_temas=contagem_temas,
                         temas_selecionados=[int(t) for t in temas_selecionados if t.isdigit()])

@app.route('/zerar_contagens')
def zerar_contagens():
    global contagem_temas
    contagem_temas = {k: 0 for k in temas.keys()}
    salvar_contagem(contagem_temas)
    return redirect('/')

@app.route('/gerar_pdf')
def gerar_pdf():
    try:
        rendered = render_template('pdf_template.html', 
                                temas=temas, 
                                contagem_temas=contagem_temas)
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        return send_file(
            io.BytesIO(pdf),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='contagem_temas.pdf'
        )
    except Exception as e:
        print(f"Erro ao gerar PDF: {str(e)}")
        return "Erro ao gerar PDF", 500

@app.route('/favicon.ico')
def favicon():
    return '', 404

if __name__ == '__main__':
    # Garante que o arquivo de contagem existe ao iniciar
    if not os.path.exists(CONTAGEM_FILE):
        salvar_contagem({k: 0 for k in temas.keys()})
    
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=False)
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
        sys.exit(0)
