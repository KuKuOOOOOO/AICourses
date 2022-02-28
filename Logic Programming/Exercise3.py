from kanren import run, eq, membero, var, conde
from kanren import Relation, facts

#--------------------------------Define logic gate--------------------------------
def Log_AND(a, b):
    #AND
    o = var()
    Truth = Relation()
    facts(Truth, (0, 0, 0),
                 (0, 1, 0),
                 (1, 0, 0),
                 (1, 1, 1))
    Output = run(1, o, Truth(a, b, o))
    return TupleToStringToInt(Output)

def Log_XOR(a, b):
    #XOR
    o = var()
    Truth = Relation()
    facts(Truth, (0, 0, 0),
                 (0, 1, 1),
                 (1, 0, 1),
                 (1, 1, 0))
    Output = run(1, o, Truth(a, b, o))
    return TupleToStringToInt(Output)

def Log_OR(a, b):
    #OR
    o = var()
    Truth = Relation()
    facts(Truth, (0, 0, 0),
                 (0, 1, 1),
                 (1, 0, 1),
                 (1, 1, 1))
    Output = run(1, o, Truth(a, b, o))
    return TupleToStringToInt(Output)

#---------------------Tuple convert to string and int----------------------------
def TupleToStringToInt(Tuple):
    Tuple_str = ''.join(str(v) for v in Tuple)
    Tuple_int = int(Tuple_str)
    return Tuple_int

def Gate_TupTOInt(Tuple, Function):
    Tuple = run(1, Tuple, eq(Tuple, Function))
    Tuple = TupleToStringToInt(Tuple)
    return Tuple

#--------------------Define full-adder sum and cout circuits----------------------
def Full_Adder_Sum(A, B, Ci):
    S = var()
    G1 = var()
    # A XOR B = G1
    G1 = run(1, G1, eq(G1, Log_XOR(A, B)))
    G1 = TupleToStringToInt(G1)
    # G1 XOR Ci = Sum
    Sum = run(1, S, eq(S, Log_XOR(G1, Ci)))
    return TupleToStringToInt(Sum)

def Full_Adder_Cout(A, B, Ci):
    Co = var()
    G1 = var()
    G2 = var()
    G3 = var()
    # A XOR B = G1
    G1 = Gate_TupTOInt(G1, Log_XOR(A, B))
    # Ci AND G1 = G2
    G2 = Gate_TupTOInt(G2, Log_AND(Ci, G1))
    # A AND B = G3
    G3 = Gate_TupTOInt(G3, Log_AND(A, B))
    # G2 OR G3 = C
    Cout = run(1, Co, eq(Co, Log_OR(G2, G3)))
    return TupleToStringToInt(Cout)

#--------------------------------Main function---------------------------------------
# Initial input
a = ''
b = ''
Ci = ''
# User input and check vaious errors
while a == '' and b == '' and Ci == '':
    try:
        a, b, Ci = map(int, input("請輸入A, B, Ci(1 or 0):").split())
        if( (a > 1 or a < 0) or (b > 1 or b < 0) or (Ci > 1 or Ci < 0)):
            print("請輸入1 or 0之二進位數字!!")
            a = ''
            b = ''
            Ci = ''
            continue
    except ValueError:
        print("請輸入1 or 0之二進位數字!!")
        a = ''
        b = ''
        Ci = ''
        continue
# Show Sum and Cout
print("Sum = {0}, Cout = {1}".format(Full_Adder_Sum(a, b, Ci), Full_Adder_Cout(a, b, Ci)))