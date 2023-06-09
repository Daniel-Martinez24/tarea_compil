ERR = -1
ACP = 99
idx = 0
cERR = False
tok = ''
lex = ''
bPrinc = False
ren = 1
colu = 0
pTipos = []

cTipo = ["E=E", "A=A", "R=R", "L=L", "R=E",
        "E+E", "E+R", "R+E", "R+R", "A+A",
        "E-E", "E-R", "R-E", "R-R",
        "E*E", "E*R", "R*E", "R*R",
        "E/E", "E/R", "R/E", "R/R",
        "E\37E", "-E", "-R",
        "LyL", "LoL", "noL",
        "E>E", "R>E", "E>R", "R>R",
        "E<E", "R<E", "E<R", "R<R",
        "E>=E", "R>=E", "E>=R", "R>=R",
        "E<=E", "R<=E", "E<=R", "R<=R",
        "E<>E", "R<>E", "E<>R", "R<>R", "A<>A",
        "E==E", "R==E", "E==R", "R==R", "A==A"
]

tipoR = ["",  "",  "",  "",  "",
        "E", "R", "R", "R", "A",
        "E", "R", "R", "R",
        "E", "R", "R", "R",
        "R", "R", "R", "R",
                                          "E", "E", "R",
                                          "L", "L", "L",
                                          "L", "L", "L", "L",
                                          "L", "L", "L", "L",
                                          "L", "L", "L", "L",
                                          "L", "L", "L", "L",
                                          "L", "L", "L", "L", "L",
                                          "L", "L", "L", "L", "L"
]

def buscaTipo(cadt):
    for i in range(55):
        if cTipo[i]==cadt: return i
    return -1


class objPrgm():
    def __init__(self, nom, cls, tip, dim1, dim2, apv) -> None:
        self.nombre = nom
        self.clase = cls
        self.tipo = tip
        self.dim1 = dim1
        self.dim2 = dim2
        self.apv = apv

class TabSimb():
    arreglo = []
    def inserSimbolo(self, nom, cls, tip, dim1, dim2, apv):
        obj = objPrgm(nom, cls, tip, dim1, dim2, apv)
        self.arreglo.append( obj )

    def buscaSimbolo(self, ide):
        for x in self.arreglo:
            if x.nom == ide: return x
        return None
    
    def grabaTabla(self, archSal):
        with open(archSal, 'r') as aSal:
            if aSal == None: return 

        with open(archSal, 'w') as aSal:
            for x in tabSimb:
                aSal.write(x.nom +',' + x.clas + ',' + x.tip + ',' + \
                           x.dim1 + ','+ x.dim2 + ',#')
            aSal.close()
        return

class codigo():
    def __init__(self, mnem, dir1, dir2):
        self.mnemo = mnem
        self.dir1 = dir1
        self.dir2 = dir2
linCod = 1    
class Programa():
    cod = []
    def insCodigo(self, mnemo, dir1, dir2):
        global linCod
        x = codigo(mnemo, dir1, dir2)
        self.cod[linCod] = x
        linCod = linCod + 1


tabSimb = TabSimb()  

prgm = Programa()

pilaTipos = []

def erra(terr, desc):
    global ren, colu
    global cERR
    print('['+str(ren)+']'+'['+str(colu)+']', terr, desc)
    cERR = True

matran=[
    #let  dig  del  opa   <    >    =    .   "
    [1,   2,   6,   5,    10,  8,   7,  ERR, 12], #0
    [1,   1,   ACP, ACP, ACP, ACP, ACP, ACP,ACP], #1
    [ACP, 2,   ACP, ACP, ACP, ACP, ACP,  3, ACP], #2
    [ERR, 4,   ERR, ERR, ERR, ERR, ERR, ERR,ERR], #3
    [ACP, 4,   ACP, ACP, ACP, ACP, ACP, ACP,ACP], #4
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,ACP], #5
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,ACP], #6
    [ACP, ACP, ACP, ACP, ACP, ACP,  9,  ACP,ACP], #7
    [ACP, ACP, ACP, ACP, ACP, ACP,  9,  ACP,ACP], #8
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,ACP], #9
    [ACP, ACP, ACP, ACP, ACP, 11,    9, ACP,ACP], #10
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,ACP], #11
    [12,   12,  12,  12,  12,  12,  12,  12, 13], #12
    [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,ACP]  #13
]

tipo = ['nulo', 'entero', 'decimal', 'palabra', 'logico']
opl = ['no', 'y', 'o']
ctl= ['verdadero', 'falso']
key= ['constante', 'desde', 'si', 'hasta', 'mientras', 'entero', 'decimal', 'regresa', 'hacer',
      'palabra', 'logico', 'nulo', 'sino', 'incr' 'imprime', 'imprimenl', 'lee', 'repite', 'que']
opar=['+', '-', '*', '/', '%', '^']
deli=[';', ',', '(',')', '{', '}', '[', ']', ':']
delu=[' ', '\t', '\n']
opRl = ['<', '>', '<=', '>=', '<>']
tkCts = ['Ent', 'Dec', 'CtA', 'CtL']
entrada = ''
def colCar(x):
    if x == '_' or x.isalpha(): return 0 
    if x.isdigit(): return 1
    if x in deli: return 2
    if x in opar: return 3
    if x == '<': return 4   
    if x == '>': return 5   
    if x == '=': return 6   
    if x == '.': return 7
    if x == '"': return 8
    if x in delu: return 15
    erra('Error Lexico', x + ' simbolo no valido en Alfabeto')
    return ERR


def scanner():
    global entrada, ERR, ACP, idx, ren, colu
    estado = 0
    lexema = ''
    c = ''
    col = 0
    while idx < len(entrada) and \
          estado != ERR and estado != ACP: 
          c = entrada[idx]
          idx = idx + 1
          if c == '\n':
              colu = 0
              ren = ren + 1

          col = colCar(c)
          if estado == 0 and col == 15: 
            continue;
          if col >= 0 and col <= 8 or col == 15:
            if col == 15 and estado != 12: 
                estado = ACP
            if col >=0 and col <= 8:
                estado = matran[estado][col]
            if estado != ERR and estado != ACP and col != 15 or col == 15 and estado == 12:
                estA = estado
                lexema = lexema + c
            
            if c != '\n': colu = colu + 1

    if estado != ACP and estado != ERR: estA = estado;
    token = 'Ntk'
    if estado == ACP and col != 15: 
        idx = idx - 1
        colu = colu - 1

    if estado != ERR and estado != ACP:
        estA = estado

    if lexema in key: token = 'Res'
    elif lexema in opl: token = 'OpL'
    elif lexema in ctl: token = 'CtL'
    else: token = 'Ide'

    if estA == 2: token = 'Ent'
    elif estA == 4: token = 'Dec'
    elif estA == 5: token = 'OpA'
    elif estA == 6: token = 'Del'
    elif estA == 7: token = 'OpS'
    elif estA in [8, 9 , 10 , 11]: token = 'OpR'
    elif estA == 13: token = 'CtA'

    if token == 'Ntk':
        print('estA=', estA, 'estado=', estado)


    return token, lexema

def cte():
    global tok, lex 
    if not(tok in tkCts):
        erra('Error de sintaxis', 'se esperaba Cte y llego '+ lex) 


def termino():
    global lex, tok
    if lex != '(' and tok != 'Ide' and tok != 'CtA' and \
        tok != 'CtL' and tok != 'Ent' and 'Dec':
        tok, lex = scanner()
    if lex == '(':
        tok, lex = scanner()
        expr()
        if lex != ')':
            erra('Error de Sintaxis', 'se espera cerrar ) y llego '+ lex)
    elif tok == 'Ide':
        nomIde = lex
        tok, lex = scanner()
        if lex == '[': 
            tok, lex = scanner()
            expr()
            if lex != ']':
                erra('Error Sintaxis', 'se esperaba cerrar ] y llego '+lex)
        elif lex == '(': pass
        oIde = tabSimb.buscaSimbolo(nomIde)
        if oIde != None:
            pilaTipos.append(oIde.tip)
        else:
            erra("Error de Semantica", 'Identificador no declarado '+ nomIde) 
            pilaTipos('I')
    elif tok == 'CtL' or tok == 'CtA' or tok == 'Dec' or tok == 'Ent': 
        cte()
    if lex != ')':  
        tok, lex = scanner()

def signo():
    global lex, tok
    if lex == '-':
        tok, lex = scanner()
    termino()


def expo():
    global tok, lex
    opr = '^'
    while opr == '^':
        signo()
        opr = lex


def multi():
    global tok, lex
    opr = '*'
    while opr == '*' or opr == '/' or opr == '%':
        expo()
        opr = lex

def suma():
    global tok, lex
    opr = '+'
    while opr == '+' or opr == '-':
        multi()
        opr = lex

def oprel():
    global tok, lex
    opr = '<'
    while opr in opRl:
        suma()
        opr = lex

def opno(): 
    global lex, tok
    if lex == 'no':
        tok, lex = scanner()
    oprel()

def opy():
    global tok, lex
    opr = 'y'
    while opr == 'y':
        opno()
        opr = lex

def expr():
    global tok, lex
    opr = 'o'
    while opr == 'o':
        opy()
        opr = lex


def constVars():
        global entrada, idx, tok, lex
        tok, lex = scanner()

def params(): 
    global entrada, lex, tok
    tok, lex = scanner()


def gpoExp():
    global tok, lex
    if lex != ')':
        deli=','
        while deli == ',':
            if lex == ',': 
                tok, lex = scanner()
            expr()
            deli = lex
            #if deli == ',': 
                #genCod(linea, 'OPR 0, 20)


def leer(): pass

def imprime(): 
    global tok, lex 
    tok, lex = scanner()
    if lex != '(':
        erra('Error de Sintaxis', 'se esperaba abrir ( y llego '+ lex)
    tok, lex = scanner()
    if lex != ')': gpoExp()
    if lex != ')': tok, lex = scanner()
    if lex != ')':
        erra('Error de Sintaxis', 'se esperaba cerrar ) y llego '+ lex)
    #genCod(linea, 'OPR 0, 20')

def imprimenl(): 
    global tok, lex 
    tok, lex = scanner()
    if lex != '(':
        erra('Error de Sintaxis', 'se esperaba abrir ( y llego '+ lex)
    tok, lex = scanner()
    if lex != ')': gpoExp()
    if lex != ')': tok, lex = scanner()
    if lex != ')':
        erra('Error de Sintaxis', 'se esperaba cerrar ) y llego '+ lex)
    #genCod(linea, 'OPR 0, 21')


def desde(): pass

def mientras():
    global tok, lex
    if lex != 'mientras':
        erra('Error de Sintaxis', 'se esperaba si y llego '+ lex)

    tok, lex = scanner()
    if lex != 'que':
        erra('Error de Sintaxis', 'se esperaba si y llego '+ lex)
    tok, lex = scanner()
    condicion()
    tok, lex = scanner()
    print('despues de condicin' , tok, lex)
    if lex != '{': erra('Error de Sintaxis', 'se esperaba un { y llego '+ lex)
    print(lex)
    blkFunc()
    if lex != '}': erra('Error de Sintaxis', 'se esperaba un } y llego '+ lex)
    #time.sleep(10)

def condicion():
    """
    puede tener
    x > 1 (comparación)
    num == 0 o num == 1 (or)
    verdadero (bool , ctl)
    """
    global tok, lex
    # print('llegue ', tok, lex)
    if lex in ctl:
        pass
        # print('es ', lex)
    # cacho que sea una variable
    # no sé como hacer aun xd
    elif True:
        tok, lex = scanner()
        if lex not in opRl: erra('Error de Sintaxis', 'se esperaba cerrar operador y llego '+ lex)
        tok, lex = scanner() 
        # vuelvo a verificar que sea lo correcto, no se como
         # tok, lex = scanner() 
        
import time
def si():
    global tok, lex 
    #print(tok, lex)
    if lex != 'si':
        erra('Error de Sintaxis', 'se esperaba si y llego '+ lex)

    tok, lex = scanner()
    condicion() # aquí va la expresión
    tok, lex = scanner()
    # print('acutal', tok, lex)
    if lex != 'hacer':
        erra('Error de Sintaxis', 'se esperaba un hacer y llego y llego '+ lex)
    tok, lex = scanner()
    if lex != '{': erra('Error de Sintaxis', 'se esperaba un { y llego '+ lex)
    print(lex)
    blkFunc()
    if lex != '}': erra('Error de Sintaxis', 'se esperaba un } y llego '+ lex)
    # print(lex)
    # falta el si no
    # time.sleep(10)
   
    """
    tok, lex = scanner()
    # aquí va el por hacer
    tok, lex = scanner()
    if lex == 'regresa':
          pass
    tok, lex = scanner();
    # verificar q el regresar regrese algo
    tok, lex = scanner()
    if lex != ';':
        erra('Error de Sintaxis', 'se esperaba un ; y llego y llego '+ lex)
    print(tok, lex)
    """
def repite(): 
    global tok, lex 
    if lex != 'repite':
        erra('Error de Sintaxis', 'se esperaba repite y llego '+ lex)
    # print('repite')
    tok, lex = scanner()
    if lex != '{': erra('Error de Sintaxis', 'se esperaba un { y llego '+ lex)
    blkFunc()
    if lex != '}': erra('Error de Sintaxis', 'se esperaba un } y llego '+ lex)
    tok, lex = scanner()
    if lex != 'hasta': erra('Error de Sintaxis', 'se esperaba un hasta y llego '+ lex)
    tok, lex = scanner()
    if lex != 'que': erra('Error de Sintaxis', 'se esperaba un que y llego '+ lex)
    
    tok, lex = scanner()
    condicion()
    time.sleep(2)

def lmp(): pass

def regresa(): pass

def asigLfunc(): pass

def comando(): 
    global tok, lex
    if tok == 'Ide': asigLfunc()
    if lex == 'lee': leer()
    elif lex == 'imprime': imprime()
    elif lex == 'imprimenl': imprimenl()
    elif lex == 'desde': desde()
    elif lex == 'mientras': mientras()
    elif lex == 'si': si()
    elif lex == 'repite': repite()
    elif lex == 'lmp': lmp()
    elif lex == 'regresa': regresa()
    elif lex == '/': comentarios()
    else: erra('Error de Sintaxis', 'comando no definido '+ lex)
    tok, lex = scanner()

def blkcmd():
    global lex, tok
    tok, lex = scanner()
    if lex != ';' and lex != '{': 
        comando()
        tok, lex = scanner()
        if lex != ';': erra('Error de Sintaxis', 'se esperaba ; y llego '+lex)
    elif lex == '{':
        estatutos()
        if lex != '}': erra('Error de Sintaxis', 'se esperaba cerrar block \"}\" y llego '+ lex)

def estatutos(): 
    global tok, lex
    cbk = '{'
    while cbk != '}':
        if lex != ';': comando()
        if lex != ';': erra('Error de Sintaxis', 'se esperaba ; y llego '+lex)
        tok, lex = scanner()
        cbk = lex

def blkFunc():
    global lex, tok
    if lex != '{': erra('Error de Sintaxis', 'se esperaba abrir \"{\" y llego '+lex)
    tok, lex = scanner()
    if lex != '}': estatutos()
    if lex != '}':erra('Error de Sintaxis', 'se esperaba cerrar \"}\" y llego '+lex)



def funcs():
        global entrada, idx, tok, lex, tipo, bPrinc
        if not(lex in tipo):
            erra('Error Sintactico', 'Se esperaba tipo' + str(tipo))
        tok, lex = scanner()
        if tok != 'Ide': erra('Error Sintaxis', 'Se esperaba Nombre Funcion y llego ' + lex)
        if bPrinc: erra('Error de Semantica', 'la Funcion Principal ya esta definida') 
        if lex == 'principal': bPrinc = True
        tok, lex = scanner()      
        if lex != '(': erra('Error de Sintaxis', 'se esperaba parentisis abierto \"(\" y llego '+ lex) 
        tok, lex = scanner()      
        if lex != ')': params()
        if lex != ')': erra('Error de Sintaxis', 'se esperaba parentisis cerrado \")\"')
        tok, lex = scanner()
        blkFunc()

def comentarios():
    global entrada, idx, tok, lex
    print('inicio comentario ', lex, tok)
    print('llegue')
    tok, lex = scanner()  
    if lex != "/": erra('Error de Sintaxis', 'se esperaba / y llego ' + lex )
    conti = True
    while conti:
        # tok, lex = scanner()  
        print('lex' ,entrada[idx])
        idx+=1
        if entrada[idx] == '\n':
            print('salto')
            conti = False
            # lex, tok
            tok, lex= scanner()  
    print('fin comentario ', lex, tok)
    time.sleep(3) # aun falla


def prgm():
    while len(entrada) > 0 and  idx < len(entrada):
        constVars()
        funcs()

def parser():
    global entrada, idx, tok, lex
    prgm()

if __name__ == '__main__':
    arche = input('Archivo (.icc) [.]=salir: ')
    if arche == '.': exit()
    archivo = open(arche, 'r')
    #se carag archivo en entrada
    entrada = ''
    for linea in archivo:
        entrada += linea
        
    print(entrada)
    parser()
    if not(cERR): print('Programa COMPILO con EXITO') 