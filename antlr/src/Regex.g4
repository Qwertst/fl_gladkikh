grammar Regex;

regex: expr EOF;

expr: left=term '|' right=expr #OrExpr
     | term #TermExpr
     ;

term: left=quant right=expr #ConExpr
     | quant #QuantExpr;

quant: atom '?' # QmarkQuant
     | atom '*' # StarQuant
     | atom '+' # PlusQuant
     | atom # AtomQuant
     ;

atom: CHAR #charAtom
     | '(' expr ')' #parExpr
     ;

CHAR : [a-zA-Z0-9];
WS  :   [ \t\n]+ -> skip ;