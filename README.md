# Graph Theory Project

## Students:
- Cyprien Gibault
- Raphaël Bonny
- Axel Stoltz

## Course:
- Graph Theory

## Institution:
- EFREI Paris Panthéon Assas

## Description
This software is developed as part of the Graph Theory course assignment at EFREI Paris. It is designed to handle scheduling problems by analyzing constraint tables presented in `.txt` format, transforming these tables into graphs, and performing several computations to assist in project scheduling tasks.

## Features
- **Load and Display Graphs**: Reads constraint tables from `.txt` files and displays them as graphs.
- **Graph Validations**: Checks graphs for the absence of cycles and negative-weight edges.
- **Scheduling Computations**:
  - Computes the ranks of all vertices.
  - Calculates the earliest and latest possible start times for tasks (dates) and the slack time (floats).
  - Identifies and displays critical paths.

## Dependencies
To run this program, ensure you have the following libraries installed:
- Python (3.6 or higher)
- NetworkX
- Matplotlib
- Tabulate

You can install these with pip:
```bash
pip install networkx matplotlib tabulate
```
## How to Run

### Clone the Repository:
```bash
git clone https://github.com/akksel1/graph-theory-S6.git
cd graph-theory-S6
```

### Running the Program:
Navigate to the project directory.
Run the program using Python.

```bash
python INT1-1-main.py
```
Using the Software:
Upon launch, the program will prompt you to choose a constraint table from the available .txt files in the 'test-files' directory.
Follow on-screen prompts to perform graph analyses and computations.

## File Structure

- **main.py**: Entry point of the program.
- **/test-files**: Directory containing all test .txt files.
- **graph.py** : Contains all logic for graph operations.
- **menu.py** : Handles user interaction and menu options.
- **utilities.py** : Contains usefull functions

## Execution Traces
Execution Traces are available on the ***execution.txt*** file.


**This project is a collaborative effort among all listed students. Each member has contributed to the development and testing to ensure the program meets the assignment requirements.**
## License

The software is provided "as is", without warranty of any kind.