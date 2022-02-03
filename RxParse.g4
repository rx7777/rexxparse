grammar RxParse ;

fragment LETTER : [a-zA-Z_] ;
fragment DIGIT  : [0-9] ;
fragment PLUS   : '+' ;
fragment MINUS  : '-' ;

tmpl : expr EOF
     ;

expr : var=ID expr                # variable
     | var=ID                     # oneVariable
     | var=DUMMY expr             # dummy
     | var=DUMMY                  # oneDummy
     | var=STRING                 # oneString
     | var=STRING expr            # string
     | var=NUMBER                 # oneNumber
     | var=NUMBER expr            # number
     | EQUALS var=NUMBER          # oneNumber
     | EQUALS var=NUMBER expr     # number
     | LPAREN var=ID RPAREN       # onePattern
     | LPAREN var=ID RPAREN expr  # pattern
     ;

ID     : LETTER (LETTER|DIGIT)* ;
DUMMY  : '.' ;
NUMBER : DIGIT+ ;

STRING : DQSTRING
       | SQSTRING
       ;

EQUALS  : '=' ;
SQUOTE  : '\'' ;
DQUOTE  : '"' ;
LPAREN  : '(' ;
RPAREN  : ')' ;

SQSTRING : SQUOTE .*? SQUOTE ;
DQSTRING : DQUOTE .*? DQUOTE ;

WS : [ \r\t\u000C\n]+ -> skip ;
