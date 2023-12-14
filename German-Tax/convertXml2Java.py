#!/usr/bin/python3

import re
import sys

from os.path import basename, abspath

import re

import subprocess

import arpeggio


def build_expr_parser():
    grammar = open("grammar.txt").read()
    from arpeggio.cleanpeg import ParserPEG
    parser = ParserPEG(grammar, "start", debug=False)
    return parser


exprParser = build_expr_parser()

SCALE = 1e4

class CalcVisitor(arpeggio.PTNodeVisitor):
    def visit_number(self, node, children):
        if mode:
            number = int(float(arpeggio.text(node))*SCALE)
            return str(number)+"L"
        else:
            return arpeggio.text(node)

    def visit_id(self, node, children):
        return arpeggio.text(node)

    def visit_multiply(self, node, children):
        return "(% *" + children[0] + ")/" + str(int(SCALE))

    def visit_add(self, node, children):
        return "+" + children[0]

    def visit_subtract(self, node, children):
        return "-" + children[0]

    def visit_divide(self, node, children):
        if len(children) >= 2:
            dir = "up" if children[2] == "BigDecimal.ROUND_UP" else "down"
            if not mode:
                return f"round_{dir}(% / {children[0]}, {children[1]})"
            else:
                return f"(% / {children[0]})*{int(SCALE)}"
        return "/" + children[0]

    def visit_compareTo(self, node, children):
        cmp = children[1]
        value = int(children[2][:-1])
        other = children[0]
        # TODO check simplify algorithm here
        if value == 0:
            if cmp == '==':
                return f"(% == {other})"
            elif cmp == '!=':
                return f"(% != {other})"
            elif cmp == '>=':
                return f"(% >= {other})"
            elif cmp == '<=':
                return f"(% <= {other})"
        elif value < 0:
            if cmp == '==':
                return f"(% < {other})"
            elif cmp == '<=':
                return f"(% < {other})"
        elif value > 0:
            if cmp == '==':
                return f"(% > {other})"
            elif cmp == '>=':
                return f"(% > {other})"
        return f"compareTo(%, {other}, {value})"

    def visit_valueOf(self, node, children):
        #print("Found valueOf")
        #print(children)
        return children[0]

    def visit_longValue(self, node, children):
        return "%"

    def visit_methods(self, node, children):
        return children[0]

    def visit_call(self, node, children):
        text = children[0]
        for c in children[1:]:
            if c[0] in "+-*/":
                text = f"({text}{c})"
            else:
                text = c.replace("%", text)
        return text

    def visit_var(self, node, children):
        if children == ['BigDecimal', 'ZERO']:
            return "0"

        if children == ['BigDecimal', 'ONE']:
            return str(SCALE)

        if len(children) == 2:
            return '.'.join(children)

        return children[0]

    def visit_arrayAccess(self, node, children):
        return children[0] + "[" + children[1] + "]"

    def visit_newBD(self, node, children):
        return children[0]

    def visit_term0(self, node, children):
        return children[0]

    def visit_term90(self, node, children):
        if len(children) == 1:
            return children[0]
        else:
            return "("+(' / '.join(children))+") * "+str(int(pow(SCALE, len(children)-1)))

    def visit_term91(self, node, children):
        if len(children) == 1:
            return children[0]
        else:
            return "("+(' * '.join(children))+") / "+str(int(pow(SCALE, len(children)-1)))

    def visit_term100(self, node, children):
        if len(children) == 1:
            return children[0]
        else:
            return ' - '.join(children)
    
    def visit_term101(self, node, children):
        if len(children) == 1:
            return children[0]
        else:
            return ' +- '.join(children)

    def visit_term110(self, node, children):
        return ' '.join(children)

    def visit_term120(self, node, children):
        return ' '.join(children)

    def visit_term130(self, node, children):
        return ' && '.join(children)

    def visit_term140(self, node, children):
        return ' || '.join(children)

    def visit_setScale(self, node, children):
        global mode
        dir = "up" if children[1] == "BigDecimal.ROUND_UP" else "down"
        if mode:
            return "%"
        else:
            return f"round_{dir}(%, {children[0]})"

    def visit_expression(self, node, children):
        return children[0]
    
    def visit_array_expression(self, node, children):
        result = "{"
        result += ", ".join(children)
        result += "}"
        return result

    def visit_assign(self, node, children):
        return ' = '.join(children)

    def visit_start(self, node, children):
        return children[0]


def replace(regex, replacement,multiline=False):
    global text
    if multiline:
        r = re.compile(regex, re.DOTALL | re.MULTILINE)
    else:
        r = re.compile(regex, re.DOTALL)
    text = re.sub(regex, replacement, text)


def translateExpr(x):
    v = parse(x.group(1))
    #print(f"{v}\n{x.group(1)}\n\n", file=sys.stderr)
    return f"{v};"


def translateIfExpr(x):
    b = parse(x.group(1))
    #print(f"{b}\n{x.group(1)}\n\n", file=sys.stderr)
    return f"if({b})"


def parse(value):
    value = value.replace("&lt;", "<")
    value = value.replace("&gt;", ">")
    value = value.replace("&amp;", "&")
    try:
        structure = exprParser.parse(value)
    except:
        raise ValueError(f"Error parsing {value}")
    result = arpeggio.visit_parse_tree(structure, CalcVisitor(debug=False))
    # print(structure)
    return result

all_inputs = []

def translate_default_val_public(x):
    assignment = ""
    if mode:
        number = int(float(x.group(3))*SCALE)
        assignment = str(number)+"L"
    else:
        assignment = x.group(3) 
    return f"public {x.group(2)} {x.group(1)} = {assignment};"

def translate_default_val_private(x):
    assignment = ""
    if mode:
        number = int(float(x.group(3))*SCALE)
        assignment = str(number)+"L"
    else:
        assignment = x.group(3) 
    return f"private {x.group(2)} {x.group(1)} = {assignment};"

def translate_default_val_const(x):
    assignment = ""
    if mode:
        assignment = parse(x.group(3))
        #assignment=x.group(3)
        #number = int(float(x.group(3))*SCALE)
        #assignment = str(number)+"L"
    else:
        assignment = x.group(3) 
    return f"public static final {x.group(2)} {x.group(1)} = {assignment};"


def translate_default_val_input(x):
    assignment = ""
    all_inputs.append(x.group(1))
    if mode:
        number = int(float(x.group(3))*SCALE)
        assignment = str(number)+"L"
    else:
        assignment = x.group(3) 
    return f"public {x.group(2)} {x.group(1)} = {assignment};"

def translate_input(x):
    all_inputs.append(x.group(1))
    return f"public {x.group(2)} {x.group(1)};"

mode = sys.argv[2] == "int"

file_path = sys.argv[1]

with open(file_path, encoding='utf-8-sig') as fh:
    text = fh.read()

replace(r'<!--', r'/*')
replace(r'-->', r'*/')
replace(r'<PAP [^>]*>','')
if mode:
    replace(r'new BigDecimal\((.*)\)', r'\1')
    replace(r'BigDecimal.ZERO', '0')
    replace(r'BigDecimal.ONE', str(int(SCALE)))
    replace(r'BigDecimal.TEN', str(int(SCALE*10)))
else:
    replace(r'new BigDecimal\((.*)\)', r'(double) \1')
    replace(r'BigDecimal.ZERO', '0.0')
    replace(r'BigDecimal.ONE', '1.0')
    replace(r'BigDecimal.TEN', '10.')
replace(r'regex_test="" regex_transform=""', r'')
replace(r'<INPUT name="(.*)" type="(.*)" default="(.*)"\s*/>', translate_default_val_input)
replace(r'<INPUT name="(.*)" type="(.*)"\s*/>', translate_input)
replace(r'<OUTPUT name="(.*)" type="(.*)" default="(.*)"/>', translate_default_val_public)
replace(r'<OUTPUT name="(.*)" type="(.*)"/>', r'public \2 \1;')
replace(r'<INTERNAL name="(.*)" type="(.*)" default="(.*)"/>', translate_default_val_public)
replace(r'<INTERNAL name="(.*)" type="(.*)"/>', r'private \2 \1;')
replace(r'<CONSTANT name="(.*)"\s+type="(.*)"\s+\n?\s*value="(([^"]*\n?)*)"/>', translate_default_val_const,multiline=True)
replace(r'<CONSTANT name="(.*)"\s+type="(.*)"/>', r'public static final \2 \1;', multiline=True)
replace(r'<IF expr\s*=\s*"(?P<c>.*)"\s*>', translateIfExpr)
replace(r'<THEN>', r'{')
replace(r'</THEN>', r'}')
replace(r'<ELSE>', r'else {')
replace(r'</ELSE>', r'}')
replace(r'<EVAL exec\s*=\s*"(.*)"\s*/>', translateExpr)
replace(r'<METHOD name="(.*)">', r'void \1() { ')
replace(r'</METHOD>', '}')
replace(r'</METHODS>', '')
replace(r'</IF>', '')
replace(r'</PAP>', '')
replace(r'</INPUTS>', '')
replace(r'</OUTPUTS>', '')
replace(r'</CONSTANTS>', '')
replace(r'<CONSTANTS>', '')
replace(r'<OUTPUTS type="STANDARD">', '')
replace(r'<OUTPUTS type="DBA">', '')
replace(r'<INTERNALS>', '')
replace(r'</INTERNALS>', '')
replace(r'</VARIABLES>', '')
replace(r'<METHODS>', '')
replace(r'<MAIN>', "int main() {\n   //%INPUT%")
replace(r'</MAIN>', "//%OUTPUT%\nreturn 0; }")
replace(r'<EXECUTE\s+method\s*=\s*"(.*)"\s*/>', r'\1();')
replace(r'<PAP name="Lohnsteuer2022Big" version="1.0" versionNummer="1.0">', '')
replace(r'<VARIABLES>', '')
replace(r'<INPUTS>', '')
replace(r'BigDecimal\.valueOf\s*\(([0-9.]*)\)', r'(double)\1')
# replace(r'\((.*)\).compareTo\((.*)\) <= (.*)', r'(\1) - \2 <= \3')
# replace(r'(.*).compareTo\((.*)\) <= (.*)', r'\1 - \2 <= \3')
replace(r'BigDecimal\[\] (.*?) =', r'BigDecimal \1[] =')
replace(r'BigDecimal', r'double')

if mode:
    replace(r'\bdouble\b', 'long')
    replace(r'\bint\b', 'long')
    replace(r'_double', '_long')
    #replace(r'\b\d+(\.\d*)?\b', lambda x: str(int(float(x.group()) * 1000)))
    # replace(r'\b\d+(\.\d*)?\b', lambda x: str(int(float(x.group()) * 1)))
    replace(r'round_(up|down)\((.*), \d+\)', r'\2')
    replace(r'\[K\]', f"[(int)(K/{int(SCALE)}L)]") # access to arrays
    replace(r'\[J\]', f"[(int)(J/{int(SCALE)}L)]") # access to arrays

class_name = basename(file_path).replace('.xml', '')

with open(f"java-code/{class_name}.java","w") as fh:
    fh.write(f"public final class {class_name} {{")
    fh.write(text)
    fh.write(f"}}")

java_path = abspath("./java-code")

print(subprocess.check_output(['javac', f"{java_path}/{class_name}.java", '-d', f"{java_path}"]))

with open(f"java-code/{class_name}Main.java", "w") as fh:
    fh.write("""
public class {class_name}Main {{
    public static native long nondetInt();

    // @Source(tags = "1", level = "high") 
    public static long makeInputHigh(long x) {{
        return x;
    }}

    // @Sink(tags = "1", level = "low")
    public static void printLow(long i) {{
        System.out.println(i);
    }}
    
    public static void init_vars({class_name} instance) {{
    """.format(class_name=class_name))
    for i in all_inputs:
        fh.write(f"        instance.{i} = nondetInt();\n")      
    fh.write("""
    }}

    public static void info_flow({class_name} instance) {{
        init_vars(instance);
        instance.R = makeInputHigh(nondetInt());
        //this.LSTLZZ = 0;
        instance.main();
        /*  Fuer den Lohnzahlungszeitraum einzubehaltende Lohnsteuer in Cents  */
        printLow(instance.LSTLZZ);
        /*  Fuer den Lohnzahlungszeitraum einzubehaltender Solidaritaetszuschlag
                        in Cents  */
        printLow(instance.SOLZLZZ);
        /*  Solidaritätszuschlag für sonstige Bezüge  */
        printLow(instance.SOLZS);
        /*  Solidaritätszuschlag für die Vergütung für mehrjährige Tätigkeit  */
        printLow(instance.SOLZV);
        /*  Lohnsteuer für sonstige Bezüge  */
        printLow(instance.STS);
        /*  Lohnsteuer für die Vergütung für mehrjährige Tätigkeit und der tarifermäßigt zu besteuernden
                        Vorteile bei Vermögensbeteiligungen in Cent  */
        printLow(instance.STV);
        /*  Für den Lohnzahlungszeitraum berücksichtigte Beiträge des Arbeitnehmers zur
                        privaten Basis-Krankenversicherung und privaten Pflege-Pflichtversicherung  */
        printLow(instance.VKVLZZ);
        /*  Für den Lohnzahlungszeitraum berücksichtigte Beiträge des Arbeitnehmers
                        zur privaten Basis-Krankenversicherung und privaten Pflege-Pflichtversicherung (ggf.
                        */
        printLow(instance.VKVSONST);
        
    }}

    public static void main(String[] args) {{
        {class_name} instance = new {class_name}();
        info_flow(instance);
    }}
}}
""".format(class_name=class_name))
    
print(subprocess.check_output(['javac', f"{java_path}/{class_name}Main.java", '-d', f"{java_path}", '-cp', java_path]))

with open(f"joana/{class_name}.joana", "w") as fh:
    fh.write("""
setClasspath {java_path}
searchEntries
selectEntry {class_name}Main.main([Ljava/lang/String;)V
setExceptionAnalysis IGNORE_ALL
buildSDG
source {class_name}Main.makeInputHigh(J)J->p1 high
sink {class_name}Main.printLow(J)V->p1 low
run
""".format(class_name=class_name,java_path=java_path))

# def test(input, expected):
#     actual = parse(input)
#     if actual.replace(' ', '') != expected.replace(' ', ''):
#         print("ACTUAL:   ", actual)
#         print("EXPRECTED:", expected)
#         raise AssertionError()
#
# test("ZRE4.subtract(ZVBEZ).compareTo(ZAHL1000) == -1", "((ZRE4-ZVBEZ) < ZAHL1000)")
# test("ANP = ANP.add(ZRE4).subtract(ZVBEZ).setScale(0,BigDecimal.ROUND_UP)",
#      "ANP=round_up(((ANP + ZRE4) - ZVBEZ),0)")
#
# test("BigDecimal.valueOf(5.5).divide(ZAHL100)", "(5.5/ZAHL100)")
#
# test("SOLZLZZ = SOLZLZZ.add(STS.multiply(BigDecimal.valueOf(5.5).divide(ZAHL100))).setScale(0, BigDecimal.ROUND_DOWN)",
#      "SOLZLZZ = round_down((SOLZLZZ+(STS*(5.5/ZAHL100))), 0)")
