A little puzzle game with Bayesian Inference.

# Features
- using Bayesian Inference to solve the little puzzle
- computing the posterior probabilities for all grids
- a game with GUI is provided 

# GAME:
- A board with 4 by 4 grid
- 4 "*" are placed on the board with one of the patterns
- the goal is to find all "*" with minimum steps.

### patterns
- `horizontal line` x 4
    ```
    * * * *
    ```
- `vertical line` x 4
    ```
    *
    *
    *
    *
    ```
- `diagonal line` x 2
    ```
    *
      *
        *
          *
    ```
- `2 x 2 rectangle` x 9
    ```
    * *
    * *
    ```
- `rhombus` x 4
    ```
      *
    *   *
      *
    ```

### demo steps
- beginning
    ```
    ? ? ? ?
    ? ? ? ?
    ? ? ? ?
    ? ? ? ?
    ```
- step one: click (1, 1)
    ```
    * ? ? ?
    ? ? ? ?
    ? ? ? ?
    ? ? ? ?
    ```
    - if there is a "*" on (1, 1)

# MODES
### game mode
- find all the hidden "*"
- you can show the probabilities as your will
- using the MOUSE CLICK

### solver mode 
- show the probabilities changes
- using the MOUSE RIGHT CLICK

# INSTALL
```sh
$ git clone 
$ pip install grid-puzzle/
```

# RUN
```sh
python -m grid_puzzle
```