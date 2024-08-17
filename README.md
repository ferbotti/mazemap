# BottiMazeMap (BMM)

**BottiMazeMap (BMM)** é uma notação inovadora projetada para representar labirintos quadriláteros de forma compacta e eficiente. Esta notação transforma a estrutura complexa de um labirinto em um código alfanumérico conciso, facilitando seu armazenamento, transmissão e manipulação em diversos contextos computacionais.

Inspirada pela elegância e eficácia da notação FEN (Forsyth-Edwards Notation) utilizada no xadrez, a BMM aplica princípios similares de compactação e padronização para labirintos. Assim como a FEN captura o estado completo de um tabuleiro de xadrez em uma única string de texto, a BMM codifica toda a estrutura de um labirinto - incluindo suas dimensões, caminhos e paredes - em uma representação textual única.

Para contextualizar, a notação FEN no xadrez é um método padrão para descrever a posição completa de um jogo de xadrez em uma única linha de texto. Por exemplo, a posição inicial de um jogo de xadrez em FEN é representada como:

```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

Nesta notação, cada letra representa uma peça (r = torre, n = cavalo, b = bispo, q = rainha, k = rei, p = peão), os números representam espaços vazios, e as barras (/) separam as linhas do tabuleiro. Informações adicionais após o espaço incluem quem move, direitos de roque, possibilidade de en passant, e contagem de movimentos.

De maneira análoga, a BMM codifica a estrutura completa de um labirinto em uma string compacta. Por exemplo:

```
12x11:Dv9Ab6wV+rFeqNXaC39kD78=
```

Nesta notação BMM, "12x11" representa as dimensões do labirinto, enquanto a string após os dois pontos (:) é uma representação codificada e comprimida da estrutura interna do labirinto, incluindo todos os caminhos e paredes.

Assim como a FEN revolucionou a maneira como posições de xadrez são registradas e compartilhadas, a BMM visa simplificar e padronizar a representação de labirintos, tornando-os mais acessíveis para uma variedade de aplicações, desde jogos até algoritmos de pathfinding e estudos de inteligência artificial.

## Propósito e Aplicações

O BottiMazeMap (BMM) foi desenvolvido com os seguintes objetivos em mente:

1. **Criação Procedural de Labirintos**: A notação BMM facilita a geração e armazenamento de labirintos para jogos e aplicações que requerem a criação dinâmica de ambientes labirínticos.

2. **Estudo de Algoritmos de Pathfinding**: BMM proporciona uma representação compacta de labirintos, ideal para testar e estudar algoritmos de busca de caminhos, como o A* (A-star) e similares.

3. **Otimização de Processamento**: Ao compactar a representação do labirinto, o BMM contribui para um aumento significativo na velocidade de processamento em aplicações que manipulam ou analisam estruturas de labirinto.

## Exemplo de Notação

Considere a seguinte notação BMM:

```
12x11:Dv9Ab6wV+rFeqNXaC39kD78=
```

- **12x11**: Representa as dimensões do labirinto (largura x altura).
- **Dv9Ab6wV+rFeqNXaC39kD78=**: Este é o perfil compactado do labirinto.

## Descrição do Labirinto

O labirinto é reduzido a uma matriz binária, onde cada célula é representada por um dígito:

- **1**: Célula preenchida (parede).
- **0**: Célula vazia (caminho).

A matriz correspondente ao exemplo acima seria:

```
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

Este padrão binário é então compactado na notação BMM para uma representação mais curta e eficiente.

## Construção do BottiMazeMap (BMM)

A construção do BottiMazeMap (BMM) segue alguns passos específicos para transformar uma matriz que representa um labirinto em uma notação compacta e facilmente reproduzível:

1. **Leitura do Labirinto**: A matriz do labirinto é lida, onde cada linha representa uma linha da matriz e cada caractere (0 ou 1) representa uma célula (caminho ou parede).

2. **Conversão da Matriz em uma String Binária Contínua**: A matriz é convertida em uma única string binária longa.

3. **Conversão da String Binária em Bytes**: A string binária é convertida em bytes para compactação.

4. **Codificação Base64**: Os bytes são codificados em Base64 para uma representação mais compacta e transmissível.

5. **Geração da Notação Final**: A notação BMM é construída combinando as dimensões do labirinto com a string codificada em Base64.

## Vantagens do BMM

1. **Compactação Eficiente**: Reduz significativamente o espaço necessário para armazenar representações de labirintos.

2. **Facilidade de Transmissão**: A notação compacta facilita a transmissão de estruturas de labirinto em redes ou entre diferentes partes de um sistema.

3. **Aumento de Desempenho**: A representação compacta permite um processamento mais rápido em algoritmos de pathfinding e análise de labirintos.

4. **Versatilidade**: Pode ser facilmente integrado em diversos tipos de aplicações, desde jogos até sistemas de simulação e IA.

## Conclusão

O BottiMazeMap (BMM) oferece uma solução eficiente para representar labirintos de forma compacta, facilitando sua manipulação em diversos contextos computacionais. Sua aplicação em criação procedural de labirintos e no estudo de algoritmos de pathfinding demonstra sua versatilidade e utilidade prática.
