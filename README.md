# Botti-Maze Notation (BMN)
 
**Botti-Maze Notation (BMN)** is an innovative notation designed to represent quadrilateral mazes in a compact and efficient manner. This notation transforms the complex structure of a maze into a concise alphanumeric code, making it easier to store, transmit, and manipulate in various computational contexts.

Inspired by the elegance and efficiency of the Forsyth-Edwards Notation (FEN) used in chess, BMN applies similar principles of compression and standardization to mazes. Just as FEN captures the complete state of a chessboard in a single string of text, BMN encodes the entire structure of a maze—including its dimensions, paths, and walls—into a unique textual representation.

To provide context, FEN notation in chess is a standard method for describing the complete position of a chess game in a single line of text. For example, the initial position of a chess game in FEN is represented as:


```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```
In this notation, each letter represents a piece (r = rook, n = knight, b = bishop, q = queen, k = king, p = pawn), numbers represent empty squares, and slashes (/) separate the rows of the board. Additional information after the space includes the side to move, castling rights, en passant availability, and move count.

Similarly, BMN encodes the complete structure of a maze into a compact string. For example:

<img src="https://github.com/ferbotti/mazemap/blob/main/maze1.png?raw=true" alt="Exemplo de Imagem" width="100" height="100"/>

```
12x11:Dv9Ab6wV+rFeqNXaC39kD78=
```
In this BMN notation, "12x11" represents the maze's dimensions, while the string after the colon (:) is an encoded and compressed representation of the maze's internal structure, including all paths and walls.

Just as FEN revolutionized the way chess positions are recorded and shared, BMN aims to simplify and standardize the representation of mazes, making them more accessible for a variety of applications, from games to pathfinding algorithms and artificial intelligence studies.

## Purpose and Applications

Botti-Maze Notation (BMN) was developed with the following goals in mind:

1.  **Procedural Maze Creation**: BMN notation facilitates the generation and storage of mazes for games and applications that require dynamic creation of labyrinthine environments.

2.  **Study of Pathfinding Algorithms**: BMN provides a compact representation of mazes, ideal for testing and studying pathfinding algorithms like A* (A-star) and similar ones.

3.  **Processing Optimization**: By compacting the maze's representation, BMN contributes to a significant increase in processing speed in applications that manipulate or analyze maze structures.

## Notation Example

Consider the following BMN notation:

```
12x11:Dv9Ab6wV+rFeqNXaC39kD78=
```

-  **12x11**: Represents the dimensions of the maze (width x height).

-  **Dv9Ab6wV+rFeqNXaC39kD78=**: This is the compressed profile of the maze.

## Maze Description

<img src="https://github.com/ferbotti/mazemap/blob/main/maze1matrix.png?raw=true" alt="Exemplo de Imagem" width="150" height="150"/>

The maze is reduced to a binary matrix, where each cell is represented by a digit:

-  **1**: Filled cell (wall).

-  **0**: Empty cell (path).

The matrix corresponding to the above example would be:

<img src="https://github.com/ferbotti/mazemap/blob/main/binMatrix.png?raw=true" alt="Exemplo de Imagem" width="200" height="200"/>

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


This binary pattern is then compacted into BMN notation for a shorter and more efficient representation.

## Construction of Botti-Maze Notation (BMN)

The construction of Botti-Maze Notation (BMN) follows specific steps to transform a matrix representing a maze into a compact and easily reproducible notation:

1.  **Maze Reading**: The maze matrix is read, where each row represents a line of the matrix, and each character (0 or 1) represents a cell (path or wall).

2.  **Conversion of the Matrix into a Continuous Binary String**: The matrix is converted into a single long binary string.

3.  **Conversion of the Binary String into Bytes**: The binary string is converted into bytes for compression.

4.  **Base64 Encoding**: The bytes are encoded in Base64 for a more compact and transmittable representation.

5.  **Generation of the Final Notation**: The BMN notation is constructed by combining the maze dimensions with the Base64-encoded string.

## Advantages of BMN

1.  **Efficient Compression**: Significantly reduces the space required to store maze representations.

2.  **Ease of Transmission**: The compact notation facilitates the transmission of maze structures over networks or between different parts of a system.

3.  **Performance Enhancement**: The compact representation allows for faster processing in pathfinding algorithms and maze analysis.

4.  **Versatility**: Can be easily integrated into various types of applications, from games to simulation systems and AI.

## Conclusion  

Botti-Maze Notation (BMN) offers an efficient solution for representing mazes compactly, making them easier to manipulate in various computational contexts. Its application in procedural maze creation and the study of pathfinding algorithms demonstrates its versatility and practical utility.
