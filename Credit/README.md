# Running examples from the Paper
The paper uses three running examples whose java version can be found in `./org/Sample1.java`.
These properties can be shown using the Java verification tool `KeY` by specifying the corresponding information-flow properties in JML (see `Sample1.java`) from which we can derive Fairness Properties

## Requirements
- Java 17

## Setup
- Download the Java Verification Tool [KeY](https://www.key-project.org/download/)

## `credit1`
This program clearly discriminates againt people from Group 0.
To formally show this, proceed as follows:
- Open KeY
- `File` -> `Load...` -> Choose `./org/Sample1.java`
- In the window that opens: Choose `credit1` on the left, then choose the `Non-interference contract 0`
- Click `Start Proof`
- Click the Green Play Button in the upper left
- At some point the proof gets stuck
- Click `Proof` -> `Search for a counterexample`
- The SMT solver finds a concrete violation of the information-flow property which can be inspected by clicking on `Info`

## `credit2`
This program is fair under certain restrictions, i.e. it satisfies Conditional Demographic Parity (more specifically be excluding `group>=6 && score >= 6 && score < 8` from the analysis).  
To show this, proceed as follows:
- Open KeY
- `File` -> `Load...` -> Choose `./org/Sample1.java`
- In the window that opens: Choose `credit2` on the left, then choose the `Non-interference contract 0`
- Click the Green Play Button in the upper left
- A window should pop up which indicates the property has been proven.

## `credit3`
This program satisfies demographic parity under the assumption that `group` and `score` are independently distributed.  
To show this, proceed as follows:
- Open KeY
- `File` -> `Load...` -> Choose `./org/Sample1.java`
- In the window that opens: Choose `credit3` on the left, then choose the `Non-interference contract 0`
- Click the Green Play Button in the upper left
- A window should pop up which indicates the property has been proven.