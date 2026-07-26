# Explicacao do Projeto

## Visao geral

Este projeto implementa a **Botti-Maze Notation (BMN)**, uma notacao textual compacta para representar labirintos binarios retangulares.

Na matriz do labirinto:

- `1` representa parede;
- `0` representa caminho livre.

A BMN transforma essa matriz em uma string curta, no formato:

```text
largura x altura:conteudo_base64
```

Na implementacao, o formato nao usa espacos:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=
```

Metadados opcionais podem ser adicionados ao final:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=;entrada=3,0;saida=3,11
```

## Objetivo

O objetivo do projeto e oferecer uma forma simples de serializar labirintos para armazenamento, transmissao e reconstrucao.

Isso e util em:

- jogos que precisam salvar, compartilhar ou gerar labirintos;
- estudos de algoritmos de busca de caminho, como A*;
- simulacoes com muitos mapas pequenos;
- APIs, arquivos ou URLs que precisam transportar mapas em texto.

## Como a codificacao funciona

O fluxo de codificacao parte de uma matriz binaria retangular.

Exemplo em `mazefile/mazeBin1.mz`:

```text
11101111111
10100000001
10111110101
10000010101
11111010101
10001010111
10101010001
10101011101
10100000101
10111111101
10010000001
11110111111
```

O codigo:

1. valida se a matriz nao e vazia, e retangular e contem apenas `0` e `1`;
2. junta todas as linhas em uma unica string binaria;
3. completa a string com zeros se o total de bits nao for multiplo de 8;
4. converte a string binaria para bytes;
5. codifica os bytes em Base64;
6. prefixa o resultado com `largura x altura`;
7. adiciona metadados opcionais no formato `;chave=valor`.

Para o arquivo de exemplo, a BMN gerada e:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=
```

## Como a decodificacao funciona

O processo inverso:

1. separa dimensoes e payload pelo caractere `:`;
2. interpreta largura e altura;
3. valida se o payload e Base64 valido;
4. converte os bytes para bits;
5. usa apenas `largura * altura` bits, descartando zeros de preenchimento;
6. reorganiza os bits em linhas;
7. interpreta metadados opcionais quando `decode_bmn_with_metadata` e usado.

`decode_bmn(...)` continua retornando apenas a matriz, para manter compatibilidade com o uso anterior.

## Estrutura do repositorio

- `bmn.py`: modulo principal, com leitura, validacao, codificacao, decodificacao, metadados e renderizacao SVG.
- `pyproject.toml`: configuracao para instalar o projeto como pacote Python.
- `mazefile/mazeBin1.mz`: matriz binaria de exemplo.
- `examples/encode_decode_demo.py`: demo de leitura, codificacao, decodificacao, metadados e renderizacao SVG.
- `tests/test_bmn.py`: testes automatizados da biblioteca.
- `README.md`: documentacao em ingles.
- `README_pt-br.md`: documentacao em portugues.
- `maze1.png`, `maze1matrix.png`, `binMatrix.png`: imagens ilustrativas existentes.

## Funcoes principais

### `read_maze(path)`

Le um arquivo de texto com uma matriz binaria e retorna uma matriz de inteiros. Tambem valida caracteres invalidos.

### `validate_maze(matrix)`

Garante que a matriz:

- nao seja vazia;
- nao tenha linhas vazias;
- seja retangular;
- contenha apenas `0` e `1`.

### `encode_bmn(matrix, metadata=None)`

Codifica uma matriz como BMN.

Exemplo:

```python
from bmn import encode_bmn

matrix = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
]

bmn = encode_bmn(matrix, metadata={"inicio": (0, 0), "objetivo": (2, 2)})
```

### `decode_bmn(bmn)`

Decodifica uma BMN e retorna apenas a matriz.

```python
from bmn import decode_bmn

matrix = decode_bmn("3x3:VQA=")
```

### `decode_bmn_with_metadata(bmn)`

Decodifica uma BMN e retorna matriz mais metadados.

```python
from bmn import decode_bmn_with_metadata

matrix, metadata = decode_bmn_with_metadata("3x3:VQA=;inicio=0,0")
```

### `render_maze_svg(matrix, path=None, ...)`

Renderiza uma matriz como imagem SVG. Se `path` for informado, grava o arquivo em disco.

```python
from bmn import render_maze_svg

svg = render_maze_svg(matrix, "maze.svg")
```

## Instalacao

O projeto agora pode ser instalado como pacote Python local:

```bash
pip install -e .
```

Para instalar tambem dependencias de desenvolvimento:

```bash
pip install -e ".[dev]"
```

## Como executar o demo

```bash
python examples/encode_decode_demo.py
```

O demo:

1. le `mazefile/mazeBin1.mz`;
2. gera a BMN com metadados;
3. decodifica matriz e metadados;
4. imprime a matriz reconstruida;
5. gera uma imagem SVG do labirinto.

## Como testar

```bash
pytest -q
```

Os testes cobrem:

- ciclo encode/decode;
- rejeicao de matrizes nao retangulares;
- rejeicao de valores nao binarios;
- erros mais explicativos para BMNs malformadas;
- payload Base64 invalido;
- payload curto demais para as dimensoes declaradas;
- leitura de arquivos com caracteres invalidos;
- metadados;
- renderizacao SVG.

## Melhorias implementadas

As melhorias recomendadas foram avaliadas e aplicadas assim:

- **Validacao de matrizes retangulares**: implementada em `validate_maze`.
- **Erros mais explicativos**: o parser da BMN agora gera `ValueError` com mensagens especificas.
- **Padronizacao do nome**: a documentacao usa **Botti-Maze Notation (BMN)**.
- **Pacote instalavel**: `pyproject.toml` permite `pip install -e .`.
- **Renderizacao de imagem**: `render_maze_svg` cria uma imagem SVG da matriz.
- **Metadados**: `encode_bmn` aceita metadados opcionais e `decode_bmn_with_metadata` os recupera.

## Resumo

O projeto e uma biblioteca Python pequena e instalavel para transformar labirintos binarios em strings BMN, reconstruir essas strings de volta para matrizes, anexar metadados simples e renderizar labirintos como SVG.
