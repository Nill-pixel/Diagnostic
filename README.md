# Medical Diagnosis By X-ray And Symptoms

## Sumário

- [Sobre](#sobre)
- [Começando](#comecando)
- [Utilização](#utilizacao)
- [Implantação](#implantacao)
- [Contribuição](../CONTRIBUTING.md)
- [Licença](#licenca)

## Sobre <a name="sobre"></a>

Este projeto implementa uma aplicação web utilizando Flask para implantar um modelo de aprendizado profundo para classificação de imagens. O modelo, treinado em um conjunto de dados de imagens de raio-X de tórax, faz previsões para determinar se uma imagem mostra sinais de COVID-19, Pneumonia ou está Normal. A aplicação permite aos usuários fazer upload de uma imagem e receber previsões no formato JSON. Além disso, uma interface desktop de usuário foi desenvolvida usando Flet para consumir essa API.

## Começando <a name="comecando"></a>

Estas instruções vão ajudar você a obter uma cópia do projeto e executá-lo em sua máquina local para desenvolvimento e testes. Consulte [implantação](#implantacao) para notas sobre como implantar o projeto em um sistema ao vivo.

### Pré-requisitos

Certifique-se de ter os seguintes itens instalados:

- Python (versão >= 3.6)
- TensorFlow
- Flask
- numpy
- PIL (Pillow)
- requests
- flet
- jupyter

Você pode instalá-los usando pip:

```bash
pip install tensorflow flask numpy pillow requests flet jupyter
```

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Nill-pixel/Diagnostic.git
cd diagnostic
```

2. Baixe o arquivo do modelo pré-treinado (`CNN_model.keras`) no diretório `src/api/models`.

### Utilização <a name="utilizacao"></a>

#### API

1. Navegue até o diretório da API:

```bash
cd src/api
```

2. Execute o notebook da API:

```bash
jupyter notebook api.ipynb
```

3. Siga as instruções no notebook para iniciar o servidor Flask.

#### Interface

1. Navegue até o diretório da interface:

```bash
cd src/interface
```

2. Execute o arquivo `Main.py` para iniciar a interface Flet:

```bash
flet Main.py -d
```

3. Utilize a interface para consumir a API e visualizar as previsões de maneira mais amigável. A interface permite fazer o upload de imagens de raio-X e exibe os resultados em um gráfico de pizza utilizando o componente `PieChart`.

## Implantação <a name="implantacao"></a>

Para implantar este projeto em um ambiente ao vivo, siga estas etapas:

1. Certifique-se de que você possui um servidor com suporte a Python.

2. Instale os pré-requisitos no servidor conforme mencionado na seção de pré-requisitos.

3. Clone o repositório no servidor e navegue até o diretório do projeto:

```bash
git clone https://github.com/Nill-pixel/Diagnostic.git
cd diagnostic
```

4. Baixe o arquivo do modelo pré-treinado (`CNN_model.keras`) no diretório `src/api/models`.

5. No servidor, execute o notebook da API para iniciar o servidor Flask:

```bash
cd src/api
jupyter notebook api.ipynb
```

6. Para a interface, configure um serviço para executar o script `Main.py` e certifique-se de que ele possa acessar a API:

```bash
cd src/interface
flet Main.py -d
```

## Licença <a name="licenca"></a>

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
