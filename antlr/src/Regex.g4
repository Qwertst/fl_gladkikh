grammar Regex;

regex: expr EOF;

expr:    left=expr '|' right=expr  # OrExpr
     |   left=expr right=expr #ConExpr
     |   atom '?'  # QmarkExpr
     |   atom '*'  # StarExpr
     |   atom '+'  # PlusExpr
     |   atom #AtomExpr
     ;
atom: CHAR | '(' expr ')';

CHAR : [a-zA-Z0-9];
WS  :   [ \t]+ -> skip ;