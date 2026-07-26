# Botti-Maze Notation (BMN)

**Botti-Maze Notation (BMN)** e uma notacao textual compacta para labirintos binarios retangulares.

A BMN armazena um labirinto no formato:

```text
<largura>x<altura>:<payload-base64>[;metadado=valor]
```

Na matriz binaria, `1` representa parede e `0` representa caminho livre.

## Exemplo

O labirinto de exemplo em `mazefile/mazeBin1.mz` tem 11 colunas e 12 linhas:

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

A implementacao atual codifica esse labirinto como:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=
```

Metadados podem ser adicionados sem quebrar o formato original:

```text
11x12:7/QG+sFfqxXqjV2gt/ZA+/A=;entrada=3,0;saida=3,11
```

## Instalacao

Para desenvolvimento local:

```bash
pip install -e .
```

Para desenvolvimento com testes:

```bash
pip install -e ".[dev]"
```

## Uso

```python
from bmn import (
    decode_bmn,
    decode_bmn_with_metadata,
    encode_bmn,
    read_maze,
    render_maze_svg,
)

matrix = read_maze("mazefile/mazeBin1.mz")

bmn = encode_bmn(
    matrix,
    metadata={
        "entrada": (3, 0),
        "saida": (3, 11),
        "inicio": (3, 0),
        "objetivo": (3, 11),
    },
)

decoded = decode_bmn(bmn)
decoded_with_metadata, metadata = decode_bmn_with_metadata(bmn)
svg = render_maze_svg(decoded, "maze.svg")
```

## API

- `read_maze(path)`: le um arquivo de texto contendo uma matriz binaria de labirinto.
- `validate_maze(matrix)`: valida se a matriz nao e vazia, e retangular e contem apenas `0` e `1`.
- `encode_bmn(matrix, metadata=None)`: codifica uma matriz binaria valida como BMN.
- `decode_bmn(bmn)`: decodifica BMN de volta para matriz, ignorando metadados opcionais por compatibilidade.
- `decode_bmn_with_metadata(bmn)`: decodifica BMN e retorna `(matrix, metadata)`.
- `render_maze_svg(matrix, path=None, ...)`: renderiza a matriz como imagem SVG e opcionalmente grava em disco.

## Validacao

O codificador rejeita:

- matrizes vazias;
- linhas com larguras diferentes;
- linhas vazias;
- valores diferentes de `0` ou `1`.

O decodificador gera erros `ValueError` explicativos para:

- separador `:` ausente;
- dimensoes invalidas;
- payload ausente;
- payload Base64 invalido;
- payload curto demais para as dimensoes declaradas;
- segmentos de metadados malformados.

## Demo

```bash
python examples/encode_decode_demo.py
```

O demo le `mazefile/mazeBin1.mz`, imprime a string BMN, decodifica o resultado, imprime os metadados, reconstrui a matriz e renderiza um SVG.

## Testes

```bash
pytest -q
```

## Por que BMN?

A BMN e inspirada por notacoes compactas de estado, como a FEN do xadrez. O objetivo e tornar estruturas de labirinto faceis de armazenar, transmitir, comparar e reconstruir em jogos, simulacoes, experimentos de busca de caminho e estudos de IA.
