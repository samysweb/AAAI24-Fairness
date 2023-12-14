# Running examples from the Paper
The paper uses three running examples whose java version can be found in `./org/Sample1.java` and `./c/credit.c`.

## Qualitative Case
These properties can be shown using the Java verification tool `KeY` by specifying the corresponding information-flow properties in JML (see `Sample1.java`) from which we can derive Fairness Properties.

### Requirements
- Java 17

### Setup
- Download the Java Verification Tool [KeY](https://www.key-project.org/download/)

### `credit1`
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

### `credit3`
This program is fair under certain restrictions, i.e. it satisfies Conditional Demographic Parity (more specifically be excluding `group>=6 && score >= 6 && score < 8` from the analysis).  
To show this, proceed as follows:
- Open KeY
- `File` -> `Load...` -> Choose `./org/Sample1.java`
- In the window that opens: Choose `credit3` on the left, then choose the `Non-interference contract 0`
- Click the Green Play Button in the upper left
- A window should pop up which indicates the property has been proven.

### `credit2`
This program satisfies demographic parity under the assumption that `group` and `score` are independently distributed.  
To show this, proceed as follows:
- Open KeY
- `File` -> `Load...` -> Choose `./org/Sample1.java`
- In the window that opens: Choose `credit2` on the left, then choose the `Non-interference contract 0`
- Click the Green Play Button in the upper left
- A window should pop up which indicates the property has been proven.


## Quantitative Case
We can also measure the unfairnes of these programs.
To this end, we use a tool for the quantification of properites in C programs.


### Requirements
- Docker

### Setup
- Download the Docker Image `samweb/countersharp-experiments:artifact`

### Running an analysis
To perform an analysis, we must first transform a given program into a model counting problem and then compute the model count.
To this end, proceed as follows:
- Interactively start the container's bash via:  
  `docker run -it -v $(pwd)/c:/experiments/results samweb/countersharp-experiments:artifact`
- Generate the problems for the model counter (replacing `[function name]`):
  `python3 -m counterSharp --amh /tmp/amh.dimacs --amm /tmp/amm.dimacs --asm results/CREDIT-ASM --ash /tmp/ash.dimacs --con /tmp/con.dimacs -d --function [function name] results/credit.c`
- Compute the numerator of the formula in Level 7:
  `ganak results/CREDIT-ASM` (alternatively this can be done using an approximate model counter: `approxmc results/CREDIT-ASM`)
- This number must be divided by (number of groups)\*(number of unprotected values) (in this case 10*10=100)

The `[function name]` is determined as follows:
| Problem           | `[function name]`     | Expected Spread       |
|-------------------|-----------------------|-----------------------|
| credit1           | `testfun1`            | 1.0                   |
| credit2           | `testfun2`            | 0.0                   |
| credit3           | `testfun3`            | 0.2                   |
| credit3 NonUnif\*   | `testfun3NonUniform`  | 0.3                   |

\* In this case we expanded $|\mathcal{U}|$ to 100 and thus have to divide by 1000

### Threshold comparison
The folder `./c/threshold-comparison` contains a program with a flexible threshold of the credit score which is nonetheless dependent on the group.
In this case, we have pre-generated counting problems which can be processed by `ganak` or `approxmc`

### Causal Graph
We also analyzed the credit 2 and credit 3 w.r.t. a causal model which determines the credit score based on income and zip code.
The corresponding code can be found in `./c/causal_credit.c`.
We can quantify this case as follows:
- Interactively start the container's bash via:  
  `docker run -it -v $(pwd)/c:/experiments/results samweb/countersharp-experiments:artifact`
- Generate the problems for the model counter (replacing `[function name]`):
  `python3 -m counterSharp --amh /tmp/amh.dimacs --amm /tmp/amm.dimacs --asm results/CREDIT-ASM --ash /tmp/ash.dimacs --con /tmp/con.dimacs -d --function [function name] results/causal_credit.c`
- Compute the numerator of the formula in Level 7:
  `ganak results/CREDIT-ASM` (alternatively this can be done using an approximate model counter: `approxmc results/CREDIT-ASM`)
- This number must be divided by (number of groups)\*(number of unprotected values) (in this case 2*490=980)

| Problem           | `[function name]`     | Expected Spread       |
|-------------------|-----------------------|-----------------------|
| credit2           | `testfun2`            | 0.229                   |
| credit3           | `testfun1`            | 0.267                   |