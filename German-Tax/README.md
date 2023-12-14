# German Wage Tax Case-Study

This case study evaluated the german wage tax computation program w.r.t. Fairness properties.
In particular, we evaluted whether religious affiliation influences a person's wage tax.

The programs provided by the German Ministry of Finance are provided as XML files and can be downloaded [here](https://www.bmf-steuerrechner.de/interface/pseudocodes.xhtml).
For convenience, the XML files of the years 2015-2023 can also be found in the folder `./xml`.

## Requirements
- Java 8
- Python 3

## Setup
- Run `pip3 install Arpeggio==2.0.0`
- Download [`joana.ui.ifc.wala.console.jar`](https://pp.ipd.kit.edu/projects/joana/joana.ui.ifc.wala.console.jar) from the [Joana Webpage](https://pp.ipd.kit.edu/projects/joana/).

## Check the Fairness Property
To check the fairness property proceed as follows:
- Run `./generate.sh ./xml/Lohnsteuer[YEAR].xml` for a specific year.  
  This generates java files in `./java-code/` and Joana instructions in `./joana/Lohnsteuer[YEAR].joana`
- Open Joana (`java -jar joana.ui.ifc.wala.console.jar`): This should launch a GUI
- Click `load script` and pick `./joana/Lohnsteuer[YEAR].joana`
- The performance should now be performed; if Joana returns `no violations found` the fairness property is satisfied