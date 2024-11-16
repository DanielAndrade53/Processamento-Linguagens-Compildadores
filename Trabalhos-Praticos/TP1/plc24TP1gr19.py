import os.path
import socketserver
import webbrowser
import http.server

import re
import matplotlib.pyplot as plt
from collections import defaultdict


'''
# Lê o conteúdo de um arquivo .csv e retorna o seu conteúdo como uma string
'''
def read_csv(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found")
    except OSError as e:
        print(f"Error: An uncexpected error occured while reading this file '{filename}'.\nDetails: {e}")


'''
Processa uma string de dados, extraindo informações sobre idade, gênero, pressão arterial,
colesterol, batimentos cardíacos e doença, e retorna os dados formatados.
'''
def process_data(data):
    pattern = r'^(\d+),([MF]),(\d+),(\d+),(\d+),([01])$'
    matches = re.finditer(pattern, data, re.MULTILINE)

    processed_data = []
    for match in matches:
        age = int(match.group(1))
        gender = match.group(2)
        tension = int(match.group(3))
        cholesterol = int(match.group(4))
        heartbeat = int(match.group(5))
        has_disease = int(match.group(6))

        age_group = f"[{age - (age % 5)}-{age - (age % 5) + 4}]"
        chol_level = cholesterol - (cholesterol % 10)

        processed_data.append((age_group, gender, tension, chol_level, heartbeat, has_disease))

    return processed_data


'''
Analisa um conjunto de dados de saúde para extrair informações estatísticas sobre a presença de doenças.
'''
def analyze_data(data):
    total_diseased = sum(1 for entry in data if entry[5] == 1)

    gender_counts = defaultdict(int)
    for entry in data:
        if entry[5] == 1:
            gender_counts[entry[1]] += 1

    # A) Calcular a percentagem da Doença:
    # i) No total da Amostra:
    overall_percentage = (total_diseased / len(data)) * 100

    # ii) Por Género
    gender_percentages = {gender: (count / total_diseased) * 100 for gender, count in gender_counts.items()}

    # B) Calcular a distribuição da Doença por Escalões Etários
    # C) Calcular a distribuição da Doença por níveis de Colesterol
    age_distribution = defaultdict(int)
    chol_distribution = defaultdict(int)
    for entry in data:
        if entry[5] == 1:
            age_distribution[entry[0]] += 1
            chol_distribution[entry[3]] += 1

    # D) Determinar se há correlação entre Tensão ou Batimento Cardíaco e a ocorrência de Doença
    diseased_tension = [entry[2] for entry in data if entry[5] == 1]
    healthy_tension = [entry[2] for entry in data if entry[5] == 0]
    diseased_heartbeat = [entry[4] for entry in data if entry[5] == 1]
    healthy_heartbeat = [entry[4] for entry in data if entry[5] == 0]

    return {
        'overall_percentage': overall_percentage,
        'gender_percentages': gender_percentages,
        'age_distribution': dict(sorted(age_distribution.items())),
        'chol_distribution': dict(sorted(chol_distribution.items())),
        'tension_correlation': (diseased_tension, healthy_tension),
        'heartbeat_correlation': (diseased_heartbeat, healthy_heartbeat)
    }


'''
Cria e guarda os gráficos a partir dos resultados da análise de dados de saúde.
'''
def create_graphs(results):

    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['lines.linewidth'] = 1.6

    # -----------------------------------------------------------------------------------------

    # Percentagem de Doentes na Amostra Total
    plt.figure(figsize=(8, 8))
    plt.pie(
        [results['overall_percentage'], 100 - results['overall_percentage']],
        labels= ['Doentes', 'Saudáveis'],
        colors=['#04AA6D',
                '#FFFFFF'],
        autopct='%1.2f%%',
        startangle=90,
        wedgeprops=dict(edgecolor='black', linewidth=2.0)
    )
    plt.title('Percentagem de Doentes na Amostra Total')
    plt.savefig('percentagem_doentes.png')
    plt.close()

    plt.figure(figsize=(8, 8))
    plt.pie(
        [results['gender_percentages'].get('M', 0), results['gender_percentages'].get('F', 0)],
        labels=['Male', 'Female'],
        autopct='%1.2f%%',
        colors=['#04AA6D',
                '#FFFFFF'],
        startangle=140,
        wedgeprops=dict(edgecolor='black', linewidth=2.0)
    )
    plt.title('Percentagem de Doentes por Genero')
    plt.savefig('distribuicao_genero.png')
    plt.close()

    # ----------------------------------------------------------------------------------------------

    # Distribuição da doença por faixa etária
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        results['age_distribution'].keys(),
        results['age_distribution'].values(),
        color='#04AA6D')
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize='12',
            color='black')
    plt.title('', pad=20)
    plt.xlabel('Escalão Etário', fontsize=16, labelpad=15)
    plt.ylabel('Número de Casos', fontsize=16, labelpad=15)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('distribuicao_idade.png')
    plt.close()

    # -----------------------------------------------------------------------------------------------

    # Distribuição da doença por nível de colesterol
    plt.figure(figsize=(12, 6))
    plt.bar(
        results['chol_distribution'].keys(),
        results['chol_distribution'].values(),
        color='#04AA6D',
        width=5)
    plt.title('', fontsize=20, pad=20)
    plt.xlabel('Nível de Colesterol', fontsize=16, labelpad=15)
    plt.ylabel('Número de Casos', fontsize=16, labelpad=15)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('distribuicao_colesterol.png')
    plt.close()

    # --------------------------------------------------------------------------------------------------

    # Correlação entre tensão e batimento cardíaco (tabela chama-se boxplot)
    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [results['tension_correlation'][0], results['tension_correlation'][1]],
        tick_labels=['Com Doença', 'Saudável'],
        patch_artist=True,
        boxprops=dict(facecolor='#04AA6D'),  # Cor do box
        whiskerprops=dict(color='black'),  # Cor das "whiskers"
        capprops=dict(color='black'),  # Cor das "caps"
        medianprops=dict(color='black')  # Cor da linha mediana
    )
    plt.title('Distribuição da Tensão: Com Doença vs Saudável', fontsize=20, pad=20)
    plt.ylabel('Tensão', fontsize=16, labelpad=15)
    plt.tight_layout()
    plt.savefig('correlacao_tensao.png')
    plt.close()

    # Correlação entre batimento cardíaco e doença (tabela chama-se boxplot)
    plt.figure(figsize=(10, 6))
    plt.boxplot(
        [results['heartbeat_correlation'][0],
         results['heartbeat_correlation'][1]],
        tick_labels=['Com Doença', 'Saudável'],
        patch_artist=True,
        boxprops=dict(facecolor='#04AA6D'),  # Cor do box
        whiskerprops=dict(color='black'),  # Cor das "whiskers"
        capprops=dict(color='black'),  # Cor das "caps"
        medianprops=dict(color='black')  # Cor da linha mediana
    )
    plt.title('Distribuição do Batimento Cardíaco: Com Doença vs Saudável', fontsize=20, pad=20)
    plt.ylabel('Batimento Cardíaco', fontsize=16, labelpad=15)
    plt.tight_layout()
    plt.savefig('correlacao_batimento.png')
    plt.close()


'''
Função que gera um arquivo .json manualmente conforme o formato especificado.
'''
def generate_json(results):
    try:
        with open("report.json", "w", encoding='utf-8') as json_file:
            # Início do JSON
            json_file.write("{\n")

            # Percentagem geral
            if isinstance(results["overall_percentage"], str):
                overall_percentage = float(results["overall_percentage"].strip('%'))  # Converte para float depois de remover '%'
            else:
                overall_percentage = results["overall_percentage"]  # Assume it's already a float
            json_file.write(f'    "overall_percentage": "{overall_percentage:.2f}%",\n')

            # Percentagens de gênero
            json_file.write('    "gender_percentages": {\n')
            gender_items = []
            for gender, percentage in results['gender_percentages'].items():
                if isinstance(percentage, str):
                    gender_value = float(percentage.strip('%'))  # Converte para float depois de remover '%'
                else:
                    gender_value = percentage
                gender_items.append(f'        "{gender}": "{gender_value:.2f}%",')
            json_file.write('\n'.join(gender_items)[:-1])  # Remove ultima virgula
            json_file.write('\n    },\n')

            # Distribuição por escalão etário
            json_file.write('    "age_distribution": {\n')
            age_items = []
            for age_group, count in results['age_distribution'].items():
                age_items.append(f'        "{age_group}": {count},')
            json_file.write('\n'.join(age_items)[:-1])  # Remove ultima virgula
            json_file.write('\n    },\n')

            # Distribuição por nível de colesterol
            json_file.write('    "chol_distribution": {\n')
            chol_items = []
            for chol_level, count in results['chol_distribution'].items():
                chol_items.append(f'        "{chol_level}": {count},')
            json_file.write('\n'.join(chol_items)[:-1])  # Remove ultima virgula
            json_file.write('\n    },\n')

            # Imagens dos gráficos
            json_file.write('    "graphs": [\n')
            graphs_items = [
                '        "percentagem_doentes.png",',
                '        "distribuicao_genero.png",',
                '        "distribuicao_idade.png",',
                '        "distribuicao_colesterol.png",',
                '        "correlacao_tensao.png",',
                '        "correlacao_batimento.png"'
            ]
            json_file.write('\n'.join(graphs_items))
            json_file.write('\n    ]\n')

            # Fim do JSON
            json_file.write("}\n")

    except IOError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


'''
Função que gera um arquivo .html manualmente.
'''

def generate_html():
    html_content = f""" 
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Relatório do Processador de Registos de Doenças Cardíacas</title>
    <style>
        html {{
            scroll-behavior: smooth;
            scroll-padding-top: 30px;
        }}
        body {{
            text-align: center;
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #04AA6D;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            border-radius: 10px;
            overflow: hidden;
        }}
        th,
        td {{
            font-weight: normal;
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #04AA6D;
        }}
        td {{
            background-color: #f2f2f2;
        }}
        p {{
            padding-left: 50px;
        }}
        hr {{
            border: none;
            border-top: 2px solid black;
            margin: 20px 0;
            width: 100%;
        }}
        .navbar {{
            position: fixed;
            text-align: center;
            bottom: 20px;
            width: 40%;
            background: #04AA6D;
            padding: 10px 0;
            border-radius: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            left: 0;
            right: 0;
            margin: 0 auto;
        }}
        .navbar a {{
            color: black;
            text-decoration: none;
            padding: 10px;
        }}
        .navbar a:hover {{
            color: white;
        }}
        #gender-percentages div {{
            padding-bottom: 15px;
        }}
        .scrollable-container {{
            width: 100%;
            overflow-x: auto;
        }}
        .scrollable-container img {{
            display: block;
            max-width: none;
        }}
        .exercise-statement {{
            text-align: left;
            margin: 15px 0;
            padding: 10px;
            background-color: #f5f5f5;
            border-left: 5px solid #2aef06;
            font-style: italic;
        }}
        .team-container {{
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            flex-wrap: nowrap;
        }}
        .team-member {{
            flex: 1;
            margin: 10px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            min-width: 150px;
        }}
        .team-member h3 {{
            margin: 10px 0;
        }}
    </style>
</head>
<body>

    <div class="navbar">
        <a href="#group">GROUP</a>
        <a href="#main">MAIN</a>
        <a href="#one">ONE</a>
        <a href="#two">TWO</a>
        <a href="#three">THREE</a>
        <a href="#four">FOUR</a>
    </div>

    <h1> 3. Processsador de Registos de Doenças Cardíacas </h1>

    <div class="section About" id="group">
        <h2>Grupo de Trabalho</h2>
        <div class="team-container">
            <div class="team-member">
                <h3>Daniel Andrade <br> A100057</h3>
            </div>
            <div class="team-member">
                <h3>José Silva <br> A100105</h3>
            </div>
            <div class="team-member">
                <h3>Pedro Malainho <br> A100050</h3>
            </div>
        </div>
    </div>

    <hr>
    
     <div class="section main-Statement" id="main">
        <h2> Enunciado </h2>
        <div class="exercise-statement">
            Neste exercicio pretende-se trabalhar com um dataset gerado no âmbito
            do registo de doenças cardiacas. Construa, então, um programa Python
            para c«processar o dataset <strong>"myheart.csv"</strong> e produzir
            e produzir o solicitado nas alíneas seguintes:
        </div>
    </div>


    <div class="section section-A" id="one">
        <h2> Percentagem da Doença no total da amostra </h2>
        <div class="exercise-statement">
            Calcular a percentagem da Doença no total da amostra e por Género (considere como total <br>
            só os que estão doentes);
        </div>
        <div>
            <p id="overall-percentage"></p>
            <p id="gender-percentages"></p>
        </div>
        <div class="scrollable-container" style="display: flex; justify-content: center; gap: 10px; overflow-x: auto;">
            <img src="percentagem_doentes.png" alt="Percentagem de Doentes" style="max-width: 45%; height: auto;" />
            <img src="distribuicao_genero.png" alt="Distribuição de Doentes por Genero" style="max-width: 45%; height: auto;" />
        </div>
    </div>

    <hr>

    <div class="section section-B" id="two" >
        <h2> Distribuição da Doença por Escalões Etários </h2>
        <div class="exercise-statement">
            Calcular a distribuição da Doença por Escalões Etários. Considere os seguintes escalões: <br>
            [30-34], [35-39], [40-44], ...;
        </div>
        <table>
            <thead>
                <tr>
                    <th>Escalão Etário</th>
                    <th>Número de Casos</th>
                </tr>
            </thead>
            <tbody id="age-distribution"></tbody>
        </table>
        <div class="scrollable-container">
            <img src="distribuicao_idade.png" alt="Distribuição da Doença por Faixa Etária" />
        </div>
    </div>

    <hr>

    <div class="section section-C" id="three">
        <h2> Distribuição da Doença por Nível de Colesterol</h2>
        <div class="exercise-statement">
            Calcular a distribuição da Doença por níveis de colesterol. Considere um nível igual a um intervalo de 10 unidades,
            comece no limite inferior e crie os níveis necessários até abranger <br>
            o limite superior;
        </div>
        <p>Excluindo Valores Igual a 0 (Zero)</p>
        <table>
            <thead>
                <tr>
                    <th>Nível de Colesterol</th>
                    <th>Número de Casos</th>
                </tr>
            </thead>
            <tbody id="cholesterol-distribution"></tbody>
        </table>
        <div class="scrollable-container">
            <img src="distribuicao_colesterol.png" alt="Distribuição da Doença por Nível de Colesterol" />
        </div>
    </div>

    <hr>

    <div class="section section-D" id="four">
        <h2> Análise de Correlação</h2>
        <div class="exercise-statement">
            Determinar se há alguma correlação significativa entre a Tensão ou o Batimento e a <br>
            ocorrência de doença;
        </div>
        <p>Veja os gráficos abaixo para uma representação visual das correlações.</p>
        <div class="scrollable-container">
            <img src="correlacao_tensao.png" alt="Correlação de Tensão" />
        </div>
        <div class="scrollable-container">
            <img src="correlacao_batimento.png" alt="Correlação de Batimento Cardíaco" />
        </div>
    </div>

    <script>
        fetch('report.json')
            .then(response => response.json())
            .then(data => {{

                // Preencher a percentagem geral
                document.getElementById('overall-percentage').innerText =
                    `Percentagem Geral de Doença: ${{data.overall_percentage}}`;

                // Preencher as percentagens por gênero
                const genderList = document.getElementById('gender-percentages');
                for (const [gender, percentage] of Object.entries(data.gender_percentages)) {{
                    const genderItem = document.createElement('div');
                    genderItem.innerText = `Percentagem por Genero ${{gender}}: ${{percentage}}`;
                    genderList.appendChild(genderItem);
                }}

                // Preencher a distribuição etária
                const ageTableBody = document.getElementById('age-distribution');
                for (const [ageGroup, count] of Object.entries(data.age_distribution)) {{
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${{ageGroup}}</td><td>${{count}}</td>`;
                    ageTableBody.appendChild(row);
                }}

                // Preencher a distribuição de colesterol
                const cholTableBody = document.getElementById('cholesterol-distribution');
                for (const [cholLevel, count] of Object.entries(data.chol_distribution)) {{
                    const row = document.createElement('tr');
                    row.innerHTML = `<td>${{cholLevel}}</td><td>${{count}}</td>`;
                    cholTableBody.appendChild(row);
                }}
            }})
            .catch(error => console.error('Error fetching the report:', error));
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding='utf-8') as html_file:
        html_file.write(html_content)


def main():

    PORT = 63342

    web_dir = os.path.join(os.path.dirname(__file__))
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)

    raw_data = read_csv('myheart.csv')
    if not raw_data:
        print("The .csv file is Empty")
        return

    processed_data = process_data(raw_data)
    results = analyze_data(processed_data)
    create_graphs(results)
    generate_json(results)
    generate_html()

    webbrowser.open(f'http://localhost:{PORT}/PLC/TP1/index.html')

    print(f"Serving at port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()

