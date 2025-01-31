
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftCONDITIONALORleftCONDITIONALANDleftEQUALITYNOTEQUALleftLESSLESSOREQUALGREATERGREATEROREQUALleftPLUSMINUSleftTIMESDIVIDEMODULOrightNOTrightUMINUSBOOL BOOLEAN_LITERAL BREAK CASE COLON COMMA CONDITIONALAND CONDITIONALOR CONTINUE DECREMENT DEFAULT DIVIDE ELSE EQUAL EQUALITY FLOAT FOR FUNC GREATER GREATEROREQUAL ID IF INCREMENT INT LBRACE LBRACKET LESS LESSOREQUAL LPAREN MINUS MODULO NOT NOTEQUAL NUMBER_LITERAL PLUS RBRACE RBRACKET RETURN RPAREN SEMICOLON STRING STRING_LITERAL SWITCH TIMES VAR VOID WALRUSprogram : global_declarationsglobal_declarations : global_declarations global_declarationglobal_declarations : global_declarationglobal_declaration : function_declarationglobal_declaration : var_declaration\n                          | short_var_declaration\n    function_declaration : FUNC ID LPAREN parameters_opt RPAREN type block\n    parameters_opt : parametersparameters : emptyparameters : parameters COMMA parameterparameters : parameterparameter : ID typeblock : LBRACE block_contents RBRACEblock : LBRACE RBRACEblock_contents : statementsstatements : statements statementstatements : statementstatement : var_declaration\n                 | short_var_declaration\n                 | expression_statement\n                 | if_statement\n                 | for_statement\n                 | switch_statement\n                 | return_statement\n                 | assignmentstatement : CONTINUE SEMICOLONstatement : BREAK SEMICOLONexpression_statement : expression SEMICOLONif_statement : IF expression block else_clauseelse_clause : ELSE if_statementelse_clause : ELSE blockelse_clause : empty\n    for_statement : FOR for_init SEMICOLON expression SEMICOLON for_post block\n    for_statement : FOR expression blockfor_statement : FOR blockfor_init : ID WALRUS expressionfor_init : VAR ID type EQUAL expressionfor_post : assignmentfor_post : expression\n    switch_statement : SWITCH expression LBRACE switch_cases default_clause RBRACE\n    switch_cases : switch_cases switch_caseswitch_cases : switch_caseswitch_case : CASE expression COLON statementsdefault_clause : DEFAULT COLON statementsdefault_clause : emptyreturn_statement : RETURN expression_opt SEMICOLONexpression_opt : expression\n                      | emptyvar_declaration : VAR ID array_type EQUAL array_initializer SEMICOLONvar_declaration : VAR ID array_type SEMICOLONvar_declaration : ID WALRUS array_type array_initializer SEMICOLONvar_declaration : VAR ID type EQUAL expression SEMICOLONvar_declaration : VAR ID type SEMICOLONshort_var_declaration : ID WALRUS expression SEMICOLONarray_type : type LBRACKET NUMBER_LITERAL RBRACKETarray_type : array_type LBRACKET NUMBER_LITERAL RBRACKETarray_type : type LBRACKET RBRACKETarray_type : array_type LBRACKET RBRACKETarray_initializer : LBRACE RBRACEarray_initializer : LBRACE expression_list RBRACEarray_initializer : LBRACE nested_initializer_list RBRACEnested_initializer_list : array_initializernested_initializer_list : nested_initializer_list COMMA array_initializerarray_access : ID LBRACKET expression RBRACKETarray_access : array_access LBRACKET expression RBRACKETassignment : ID EQUAL expression SEMICOLONassignment : array_access EQUAL expression SEMICOLONassignment : ID EQUAL array_initializer SEMICOLONexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDE expression\n                  | expression MODULO expression\n                  | expression EQUALITY expression\n                  | expression NOTEQUAL expression\n                  | expression GREATER expression\n                  | expression LESS expression\n                  | expression GREATEROREQUAL expression\n                  | expression LESSOREQUAL expression\n                  | expression CONDITIONALAND expression\n                  | expression CONDITIONALOR expressionexpression : NOT expression\n                  | MINUS expression %prec UMINUSexpression : LPAREN expression RPARENexpression : literalexpression : IDexpression : array_accessexpression : ID INCREMENTexpression : ID DECREMENTexpression : function_callfunction_call : ID LPAREN arguments_opt RPARENarguments_opt : argumentsarguments : emptyarguments : arguments COMMA expressionarguments : expressionexpression_list : expression_list COMMA expressionexpression_list : expressionliteral : NUMBER_LITERALliteral : STRING_LITERALliteral : BOOLEAN_LITERALtype : INT \n            | FLOAT \n            | BOOL \n            | STRING \n            | VOIDempty :'
    
_lr_action_items = {'FUNC':([0,2,3,4,5,6,10,47,67,69,78,117,118,119,125,145,],[7,7,-3,-4,-5,-6,-2,-54,-50,-53,-51,-49,-52,-7,-14,-13,]),'VAR':([0,2,3,4,5,6,10,47,67,69,78,117,118,119,120,125,126,127,128,129,130,131,132,133,134,135,141,145,146,147,148,150,154,164,166,170,172,173,174,176,183,184,185,198,199,200,201,202,203,],[9,9,-3,-4,-5,-6,-2,-54,-50,-53,-51,-49,-52,-7,9,-14,9,-17,-18,-19,-20,-21,-22,-23,-24,-25,156,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-67,-30,-31,-40,9,9,-33,9,9,]),'ID':([0,2,3,4,5,6,7,9,10,12,14,20,21,22,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,67,68,69,72,78,109,112,117,118,119,120,125,126,127,128,129,130,131,132,133,134,135,140,141,142,143,145,146,147,148,149,150,154,156,161,164,165,166,167,170,172,173,174,176,182,183,184,185,186,187,198,199,200,201,202,203,],[8,8,-3,-4,-5,-6,11,13,-2,15,35,15,15,15,15,15,15,-54,15,15,15,15,15,15,15,15,15,15,15,15,15,15,-50,15,-53,35,-51,15,15,-49,-52,-7,138,-14,138,-17,-18,-19,-20,-21,-22,-23,-24,-25,15,155,15,15,-13,-16,-26,-27,15,-28,-35,168,15,-106,15,-34,15,-46,-66,-68,-29,-32,15,-67,-30,-31,196,15,-40,138,138,-33,138,138,]),'$end':([1,2,3,4,5,6,10,47,67,69,78,117,118,119,125,145,],[0,-1,-3,-4,-5,-6,-2,-54,-50,-53,-51,-49,-52,-7,-14,-13,]),'WALRUS':([8,138,155,],[12,12,167,]),'LPAREN':([11,12,15,20,21,22,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,67,68,69,78,109,112,117,118,120,125,126,127,128,129,130,131,132,133,134,135,138,140,141,142,143,145,146,147,148,149,150,154,155,161,164,165,166,167,170,172,173,174,176,182,183,184,185,186,187,196,198,199,200,201,202,203,],[14,22,43,22,22,22,22,22,22,-54,22,22,22,22,22,22,22,22,22,22,22,22,22,22,-50,22,-53,-51,22,22,-49,-52,22,-14,22,-17,-18,-19,-20,-21,-22,-23,-24,-25,43,22,22,22,22,-13,-16,-26,-27,22,-28,-35,43,22,-106,22,-34,22,-46,-66,-68,-29,-32,22,-67,-30,-31,22,22,43,-40,22,22,-33,22,22,]),'NOT':([12,20,21,22,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,67,68,69,78,109,112,117,118,120,125,126,127,128,129,130,131,132,133,134,135,140,141,142,143,145,146,147,148,149,150,154,161,164,165,166,167,170,172,173,174,176,182,183,184,185,186,187,198,199,200,201,202,203,],[21,21,21,21,21,21,21,-54,21,21,21,21,21,21,21,21,21,21,21,21,21,21,-50,21,-53,-51,21,21,-49,-52,21,-14,21,-17,-18,-19,-20,-21,-22,-23,-24,-25,21,21,21,21,-13,-16,-26,-27,21,-28,-35,21,-106,21,-34,21,-46,-66,-68,-29,-32,21,-67,-30,-31,21,21,-40,21,21,-33,21,21,]),'MINUS':([12,15,17,19,20,21,22,23,24,25,31,32,40,41,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64,65,67,68,69,73,77,78,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,109,112,116,117,118,120,121,122,125,126,127,128,129,130,131,132,133,134,135,138,139,140,141,142,143,144,145,146,147,148,149,150,151,153,154,155,157,159,161,162,164,165,166,167,170,171,172,173,174,176,177,178,182,183,184,185,186,187,192,193,196,197,198,199,200,201,202,203,],[20,-86,49,-98,20,20,20,-85,-87,-90,-99,-100,-88,-89,20,20,20,-54,20,20,20,20,20,20,20,20,20,20,20,20,20,-83,-82,49,20,-50,20,-53,49,49,-51,49,-69,-70,-71,-72,-73,49,49,49,49,49,49,49,49,-84,49,49,-64,-91,20,20,-65,-49,-52,20,49,49,-14,20,-17,-18,-19,-20,-21,-22,-23,-24,-25,-86,49,20,20,20,20,-87,-13,-16,-26,-27,20,-28,49,49,-35,-86,49,49,20,49,-106,20,-34,20,-46,49,-66,-68,-29,-32,49,49,20,-67,-30,-31,20,20,49,49,-86,49,-40,20,20,-33,20,20,]),'INT':([12,13,35,71,168,],[26,26,26,26,26,]),'FLOAT':([12,13,35,71,168,],[27,27,27,27,27,]),'BOOL':([12,13,35,71,168,],[28,28,28,28,28,]),'STRING':([12,13,35,71,168,],[29,29,29,29,29,]),'VOID':([12,13,35,71,168,],[30,30,30,30,30,]),'NUMBER_LITERAL':([12,20,21,22,42,43,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,65,67,68,69,78,109,112,117,118,120,125,126,127,128,129,130,131,132,133,134,135,140,141,142,143,145,146,147,148,149,150,154,161,164,165,166,167,170,172,173,174,176,182,183,184,185,186,187,198,199,200,201,202,203,],[19,19,19,19,19,19,79,19,-54,19,19,19,19,19,19,19,19,19,19,19,19,19,99,19,-50,19,-53,-51,19,19,-49,-52,19,-14,19,-17,-18,-19,-20,-21,-22,-23,-24,-25,19,19,19,19,-13,-16,-26,-27,19,-28,-35,19,-106,19,-34,19,-46,-66,-68,-29,-32,19,-67,-30,-31,19,19,-40,19,19,-33,19,19,]),'STRING_LITERAL':([12,20,21,22,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,67,68,69,78,109,112,117,118,120,125,126,127,128,129,130,131,132,133,134,135,140,141,142,143,145,146,147,148,149,150,154,161,164,165,166,167,170,172,173,174,176,182,183,184,185,186,187,198,199,200,201,202,203,],[31,31,31,31,31,31,31,-54,31,31,31,31,31,31,31,31,31,31,31,31,31,31,-50,31,-53,-51,31,31,-49,-52,31,-14,31,-17,-18,-19,-20,-21,-22,-23,-24,-25,31,31,31,31,-13,-16,-26,-27,31,-28,-35,31,-106,31,-34,31,-46,-66,-68,-29,-32,31,-67,-30,-31,31,31,-40,31,31,-33,31,31,]),'BOOLEAN_LITERAL':([12,20,21,22,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,67,68,69,78,109,112,117,118,120,125,126,127,128,129,130,131,132,133,134,135,140,141,142,143,145,146,147,148,149,150,154,161,164,165,166,167,170,172,173,174,176,182,183,184,185,186,187,198,199,200,201,202,203,],[32,32,32,32,32,32,32,-54,32,32,32,32,32,32,32,32,32,32,32,32,32,32,-50,32,-53,-51,32,32,-49,-52,32,-14,32,-17,-18,-19,-20,-21,-22,-23,-24,-25,32,32,32,32,-13,-16,-26,-27,32,-28,-35,32,-106,32,-34,32,-46,-66,-68,-29,-32,32,-67,-30,-31,32,32,-40,32,32,-33,32,32,]),'COMMA':([14,15,19,23,24,25,26,27,28,29,30,31,32,37,38,39,40,41,43,62,63,70,75,76,77,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,101,106,107,108,111,113,116,121,122,123,],[-106,-86,-98,-85,-87,-90,-101,-102,-103,-104,-105,-99,-100,72,-9,-11,-88,-89,-106,-83,-82,-12,109,-93,-95,-59,112,114,-97,-62,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-84,-10,-64,-91,-60,-61,-65,-94,-96,-63,]),'RPAREN':([14,15,19,23,24,25,26,27,28,29,30,31,32,36,37,38,39,40,41,43,62,63,64,70,74,75,76,77,86,87,88,89,90,91,92,93,94,95,96,97,98,101,106,107,108,116,121,],[-106,-86,-98,-85,-87,-90,-101,-102,-103,-104,-105,-99,-100,71,-8,-9,-11,-88,-89,-106,-83,-82,101,-12,108,-92,-93,-95,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-84,-10,-64,-91,-65,-94,]),'SEMICOLON':([15,17,19,23,24,25,26,27,28,29,30,31,32,33,34,40,41,44,62,63,80,81,86,87,88,89,90,91,92,93,94,95,96,97,98,100,101,103,104,107,108,110,111,113,115,116,136,137,138,139,143,144,152,158,159,160,162,163,171,177,178,197,],[-86,47,-98,-85,-87,-90,-101,-102,-103,-104,-105,-99,-100,67,69,-88,-89,78,-83,-82,-58,-59,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-57,-84,117,118,-64,-91,-56,-60,-61,-55,-65,147,148,-86,150,-106,-87,165,170,-47,-48,172,173,183,186,-36,-37,]),'PLUS':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,48,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,48,48,48,48,-69,-70,-71,-72,-73,48,48,48,48,48,48,48,48,-84,48,48,-64,-91,-65,48,48,-86,48,-87,48,48,-86,48,48,48,48,48,48,48,48,-86,48,]),'TIMES':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,50,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,50,50,50,50,50,50,-71,-72,-73,50,50,50,50,50,50,50,50,-84,50,50,-64,-91,-65,50,50,-86,50,-87,50,50,-86,50,50,50,50,50,50,50,50,-86,50,]),'DIVIDE':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,51,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,51,51,51,51,51,51,-71,-72,-73,51,51,51,51,51,51,51,51,-84,51,51,-64,-91,-65,51,51,-86,51,-87,51,51,-86,51,51,51,51,51,51,51,51,-86,51,]),'MODULO':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,52,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,52,52,52,52,52,52,-71,-72,-73,52,52,52,52,52,52,52,52,-84,52,52,-64,-91,-65,52,52,-86,52,-87,52,52,-86,52,52,52,52,52,52,52,52,-86,52,]),'EQUALITY':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,53,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,53,53,53,53,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,53,53,-84,53,53,-64,-91,-65,53,53,-86,53,-87,53,53,-86,53,53,53,53,53,53,53,53,-86,53,]),'NOTEQUAL':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,54,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,54,54,54,54,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,54,54,-84,54,54,-64,-91,-65,54,54,-86,54,-87,54,54,-86,54,54,54,54,54,54,54,54,-86,54,]),'GREATER':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,55,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,55,55,55,55,-69,-70,-71,-72,-73,55,55,-76,-77,-78,-79,55,55,-84,55,55,-64,-91,-65,55,55,-86,55,-87,55,55,-86,55,55,55,55,55,55,55,55,-86,55,]),'LESS':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,56,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,56,56,56,56,-69,-70,-71,-72,-73,56,56,-76,-77,-78,-79,56,56,-84,56,56,-64,-91,-65,56,56,-86,56,-87,56,56,-86,56,56,56,56,56,56,56,56,-86,56,]),'GREATEROREQUAL':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,57,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,57,57,57,57,-69,-70,-71,-72,-73,57,57,-76,-77,-78,-79,57,57,-84,57,57,-64,-91,-65,57,57,-86,57,-87,57,57,-86,57,57,57,57,57,57,57,57,-86,57,]),'LESSOREQUAL':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,58,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,58,58,58,58,-69,-70,-71,-72,-73,58,58,-76,-77,-78,-79,58,58,-84,58,58,-64,-91,-65,58,58,-86,58,-87,58,58,-86,58,58,58,58,58,58,58,58,-86,58,]),'CONDITIONALAND':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,59,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,59,59,59,59,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,59,-84,59,59,-64,-91,-65,59,59,-86,59,-87,59,59,-86,59,59,59,59,59,59,59,59,-86,59,]),'CONDITIONALOR':([15,17,19,23,24,25,31,32,40,41,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,101,102,104,107,108,116,121,122,138,139,144,151,153,155,157,159,162,171,177,178,192,193,196,197,],[-86,60,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,60,60,60,60,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-84,60,60,-64,-91,-65,60,60,-86,60,-87,60,60,-86,60,60,60,60,60,60,60,60,-86,60,]),'RBRACKET':([15,19,23,24,25,31,32,40,41,45,61,62,63,73,79,86,87,88,89,90,91,92,93,94,95,96,97,98,99,101,102,107,108,116,],[-86,-98,-85,-87,-90,-99,-100,-88,-89,80,100,-83,-82,107,110,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,115,-84,116,-64,-91,-65,]),'RBRACE':([15,19,23,24,25,31,32,40,41,46,47,62,63,67,69,78,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,101,107,108,111,113,116,117,118,120,122,123,124,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,180,181,183,184,185,188,189,191,198,201,202,203,],[-86,-98,-85,-87,-90,-99,-100,-88,-89,81,-54,-83,-82,-50,-53,-51,-59,111,113,-97,-62,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-84,-64,-91,-60,-61,-65,-49,-52,125,-96,-63,145,-14,-15,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-106,-42,-67,-30,-31,198,-41,-45,-40,-33,-44,-43,]),'LBRACE':([15,16,19,23,24,25,26,27,28,29,30,31,32,40,41,46,62,63,66,80,86,87,88,89,90,91,92,93,94,95,96,97,98,100,101,105,107,108,110,114,115,116,141,144,149,151,153,155,157,172,173,175,183,193,194,195,196,],[-86,46,-98,-85,-87,-90,-101,-102,-103,-104,-105,-99,-100,-88,-89,46,-83,-82,46,-58,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-57,-84,120,-64,-91,-56,46,-55,-65,120,-87,46,120,120,-86,169,-66,-68,120,-67,-39,120,-38,-86,]),'COLON':([15,19,23,24,25,31,32,40,41,62,63,86,87,88,89,90,91,92,93,94,95,96,97,98,101,107,108,116,190,192,],[-86,-98,-85,-87,-90,-99,-100,-88,-89,-83,-82,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,-81,-84,-64,-91,-65,199,200,]),'INCREMENT':([15,138,155,196,],[40,40,40,40,]),'DECREMENT':([15,138,155,196,],[41,41,41,41,]),'LBRACKET':([15,16,18,24,26,27,28,29,30,33,34,80,100,107,110,115,116,138,144,155,196,],[42,45,61,65,-101,-102,-103,-104,-105,45,61,-58,-57,-64,-56,-55,-65,42,65,42,42,]),'EQUAL':([26,27,28,29,30,33,34,80,100,107,110,115,116,138,144,179,196,],[-101,-102,-103,-104,-105,66,68,-58,-57,-64,-56,-55,-65,149,161,187,149,]),'CONTINUE':([47,67,69,78,117,118,120,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,183,184,185,198,199,200,201,202,203,],[-54,-50,-53,-51,-49,-52,136,-14,136,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-67,-30,-31,-40,136,136,-33,136,136,]),'BREAK':([47,67,69,78,117,118,120,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,183,184,185,198,199,200,201,202,203,],[-54,-50,-53,-51,-49,-52,137,-14,137,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-67,-30,-31,-40,137,137,-33,137,137,]),'IF':([47,67,69,78,117,118,120,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,175,176,183,184,185,198,199,200,201,202,203,],[-54,-50,-53,-51,-49,-52,140,-14,140,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,140,-32,-67,-30,-31,-40,140,140,-33,140,140,]),'FOR':([47,67,69,78,117,118,120,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,183,184,185,198,199,200,201,202,203,],[-54,-50,-53,-51,-49,-52,141,-14,141,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-67,-30,-31,-40,141,141,-33,141,141,]),'SWITCH':([47,67,69,78,117,118,120,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,183,184,185,198,199,200,201,202,203,],[-54,-50,-53,-51,-49,-52,142,-14,142,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-67,-30,-31,-40,142,142,-33,142,142,]),'RETURN':([47,67,69,78,117,118,120,125,126,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,183,184,185,198,199,200,201,202,203,],[-54,-50,-53,-51,-49,-52,143,-14,143,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,-67,-30,-31,-40,143,143,-33,143,143,]),'DEFAULT':([47,67,69,78,117,118,125,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,170,172,173,174,176,180,181,183,184,185,189,198,201,203,],[-54,-50,-53,-51,-49,-52,-14,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,-46,-66,-68,-29,-32,190,-42,-67,-30,-31,-41,-40,-33,-43,]),'CASE':([47,67,69,78,117,118,125,127,128,129,130,131,132,133,134,135,145,146,147,148,150,154,164,166,169,170,172,173,174,176,180,181,183,184,185,189,198,201,203,],[-54,-50,-53,-51,-49,-52,-14,-17,-18,-19,-20,-21,-22,-23,-24,-25,-13,-16,-26,-27,-28,-35,-106,-34,182,-46,-66,-68,-29,-32,182,-42,-67,-30,-31,-41,-40,-33,-43,]),'ELSE':([125,145,164,],[-14,-13,175,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'global_declarations':([0,],[2,]),'global_declaration':([0,2,],[3,10,]),'function_declaration':([0,2,],[4,4,]),'var_declaration':([0,2,120,126,199,200,202,203,],[5,5,128,128,128,128,128,128,]),'short_var_declaration':([0,2,120,126,199,200,202,203,],[6,6,129,129,129,129,129,129,]),'array_type':([12,13,],[16,33,]),'expression':([12,20,21,22,42,43,46,48,49,50,51,52,53,54,55,56,57,58,59,60,65,68,109,112,120,126,140,141,142,143,149,161,165,167,182,186,187,199,200,202,203,],[17,62,63,64,73,77,84,86,87,88,89,90,91,92,93,94,95,96,97,98,102,104,121,122,139,139,151,153,157,159,162,171,177,178,192,193,197,139,139,139,139,]),'type':([12,13,35,71,168,],[18,34,70,105,179,]),'literal':([12,20,21,22,42,43,46,48,49,50,51,52,53,54,55,56,57,58,59,60,65,68,109,112,120,126,140,141,142,143,149,161,165,167,182,186,187,199,200,202,203,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'array_access':([12,20,21,22,42,43,46,48,49,50,51,52,53,54,55,56,57,58,59,60,65,68,109,112,120,126,140,141,142,143,149,161,165,167,182,186,187,199,200,202,203,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,144,144,24,24,24,24,24,24,24,24,24,144,24,144,144,144,144,]),'function_call':([12,20,21,22,42,43,46,48,49,50,51,52,53,54,55,56,57,58,59,60,65,68,109,112,120,126,140,141,142,143,149,161,165,167,182,186,187,199,200,202,203,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'parameters_opt':([14,],[36,]),'parameters':([14,],[37,]),'empty':([14,43,143,164,180,],[38,76,160,176,191,]),'parameter':([14,72,],[39,106,]),'array_initializer':([16,46,66,114,149,],[44,85,103,123,163,]),'arguments_opt':([43,],[74,]),'arguments':([43,],[75,]),'expression_list':([46,],[82,]),'nested_initializer_list':([46,],[83,]),'block':([105,141,151,153,175,194,],[119,154,164,166,185,201,]),'block_contents':([120,],[124,]),'statements':([120,199,200,],[126,202,203,]),'statement':([120,126,199,200,202,203,],[127,146,127,127,146,146,]),'expression_statement':([120,126,199,200,202,203,],[130,130,130,130,130,130,]),'if_statement':([120,126,175,199,200,202,203,],[131,131,184,131,131,131,131,]),'for_statement':([120,126,199,200,202,203,],[132,132,132,132,132,132,]),'switch_statement':([120,126,199,200,202,203,],[133,133,133,133,133,133,]),'return_statement':([120,126,199,200,202,203,],[134,134,134,134,134,134,]),'assignment':([120,126,186,199,200,202,203,],[135,135,195,135,135,135,135,]),'for_init':([141,],[152,]),'expression_opt':([143,],[158,]),'else_clause':([164,],[174,]),'switch_cases':([169,],[180,]),'switch_case':([169,180,],[181,189,]),'default_clause':([180,],[188,]),'for_post':([186,],[194,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> global_declarations','program',1,'p_program','parser.py',46),
  ('global_declarations -> global_declarations global_declaration','global_declarations',2,'p_global_declarations_multiple','parser.py',52),
  ('global_declarations -> global_declaration','global_declarations',1,'p_global_declarations_single','parser.py',57),
  ('global_declaration -> function_declaration','global_declaration',1,'p_global_declaration_func','parser.py',62),
  ('global_declaration -> var_declaration','global_declaration',1,'p_global_declaration_var','parser.py',67),
  ('global_declaration -> short_var_declaration','global_declaration',1,'p_global_declaration_var','parser.py',68),
  ('function_declaration -> FUNC ID LPAREN parameters_opt RPAREN type block','function_declaration',7,'p_function_declaration','parser.py',75),
  ('parameters_opt -> parameters','parameters_opt',1,'p_parameters_opt','parser.py',89),
  ('parameters -> empty','parameters',1,'p_parameters_empty','parser.py',94),
  ('parameters -> parameters COMMA parameter','parameters',3,'p_parameters_multiple','parser.py',99),
  ('parameters -> parameter','parameters',1,'p_parameters_single','parser.py',104),
  ('parameter -> ID type','parameter',2,'p_parameter','parser.py',109),
  ('block -> LBRACE block_contents RBRACE','block',3,'p_block','parser.py',114),
  ('block -> LBRACE RBRACE','block',2,'p_block_empty','parser.py',119),
  ('block_contents -> statements','block_contents',1,'p_block_contents','parser.py',123),
  ('statements -> statements statement','statements',2,'p_statements_multiple','parser.py',130),
  ('statements -> statement','statements',1,'p_statements_single','parser.py',135),
  ('statement -> var_declaration','statement',1,'p_statement','parser.py',140),
  ('statement -> short_var_declaration','statement',1,'p_statement','parser.py',141),
  ('statement -> expression_statement','statement',1,'p_statement','parser.py',142),
  ('statement -> if_statement','statement',1,'p_statement','parser.py',143),
  ('statement -> for_statement','statement',1,'p_statement','parser.py',144),
  ('statement -> switch_statement','statement',1,'p_statement','parser.py',145),
  ('statement -> return_statement','statement',1,'p_statement','parser.py',146),
  ('statement -> assignment','statement',1,'p_statement','parser.py',147),
  ('statement -> CONTINUE SEMICOLON','statement',2,'p_statement_continue','parser.py',152),
  ('statement -> BREAK SEMICOLON','statement',2,'p_statement_break','parser.py',157),
  ('expression_statement -> expression SEMICOLON','expression_statement',2,'p_expression_statement','parser.py',162),
  ('if_statement -> IF expression block else_clause','if_statement',4,'p_if_statement','parser.py',168),
  ('else_clause -> ELSE if_statement','else_clause',2,'p_else_clause_if','parser.py',172),
  ('else_clause -> ELSE block','else_clause',2,'p_else_clause_block','parser.py',176),
  ('else_clause -> empty','else_clause',1,'p_else_clause_empty','parser.py',180),
  ('for_statement -> FOR for_init SEMICOLON expression SEMICOLON for_post block','for_statement',7,'p_for_statement','parser.py',187),
  ('for_statement -> FOR expression block','for_statement',3,'p_for_statement_expression','parser.py',194),
  ('for_statement -> FOR block','for_statement',2,'p_for_while_statement','parser.py',199),
  ('for_init -> ID WALRUS expression','for_init',3,'p_for_init_short_var','parser.py',204),
  ('for_init -> VAR ID type EQUAL expression','for_init',5,'p_for_init_var_declaration','parser.py',209),
  ('for_post -> assignment','for_post',1,'p_for_post_assignment','parser.py',214),
  ('for_post -> expression','for_post',1,'p_for_post_expression','parser.py',219),
  ('switch_statement -> SWITCH expression LBRACE switch_cases default_clause RBRACE','switch_statement',6,'p_switch_statement','parser.py',226),
  ('switch_cases -> switch_cases switch_case','switch_cases',2,'p_switch_cases_multiple','parser.py',231),
  ('switch_cases -> switch_case','switch_cases',1,'p_switch_cases_single','parser.py',235),
  ('switch_case -> CASE expression COLON statements','switch_case',4,'p_switch_case','parser.py',239),
  ('default_clause -> DEFAULT COLON statements','default_clause',3,'p_default_clause_with_statements','parser.py',243),
  ('default_clause -> empty','default_clause',1,'p_default_clause_empty','parser.py',247),
  ('return_statement -> RETURN expression_opt SEMICOLON','return_statement',3,'p_return_statement','parser.py',253),
  ('expression_opt -> expression','expression_opt',1,'p_expression_opt','parser.py',257),
  ('expression_opt -> empty','expression_opt',1,'p_expression_opt','parser.py',258),
  ('var_declaration -> VAR ID array_type EQUAL array_initializer SEMICOLON','var_declaration',6,'p_var_declaration_array_init','parser.py',264),
  ('var_declaration -> VAR ID array_type SEMICOLON','var_declaration',4,'p_var_declaration_array_noinit','parser.py',268),
  ('var_declaration -> ID WALRUS array_type array_initializer SEMICOLON','var_declaration',5,'p_var_declaration_array_short','parser.py',272),
  ('var_declaration -> VAR ID type EQUAL expression SEMICOLON','var_declaration',6,'p_var_declaration_init','parser.py',276),
  ('var_declaration -> VAR ID type SEMICOLON','var_declaration',4,'p_var_declaration_noinit','parser.py',280),
  ('short_var_declaration -> ID WALRUS expression SEMICOLON','short_var_declaration',4,'p_short_var_declaration','parser.py',284),
  ('array_type -> type LBRACKET NUMBER_LITERAL RBRACKET','array_type',4,'p_array_type_first_dimension','parser.py',290),
  ('array_type -> array_type LBRACKET NUMBER_LITERAL RBRACKET','array_type',4,'p_array_type_more_dimensions','parser.py',295),
  ('array_type -> type LBRACKET RBRACKET','array_type',3,'p_array_type_first_empty','parser.py',301),
  ('array_type -> array_type LBRACKET RBRACKET','array_type',3,'p_array_type_more_empty','parser.py',307),
  ('array_initializer -> LBRACE RBRACE','array_initializer',2,'p_array_initializer_empty','parser.py',314),
  ('array_initializer -> LBRACE expression_list RBRACE','array_initializer',3,'p_array_initializer_flat','parser.py',319),
  ('array_initializer -> LBRACE nested_initializer_list RBRACE','array_initializer',3,'p_array_initializer_nested','parser.py',324),
  ('nested_initializer_list -> array_initializer','nested_initializer_list',1,'p_nested_initializer_list_single','parser.py',338),
  ('nested_initializer_list -> nested_initializer_list COMMA array_initializer','nested_initializer_list',3,'p_nested_initializer_list_multiple','parser.py',342),
  ('array_access -> ID LBRACKET expression RBRACKET','array_access',4,'p_array_access_first','parser.py',348),
  ('array_access -> array_access LBRACKET expression RBRACKET','array_access',4,'p_array_access_next','parser.py',353),
  ('assignment -> ID EQUAL expression SEMICOLON','assignment',4,'p_simple_assignment','parser.py',361),
  ('assignment -> array_access EQUAL expression SEMICOLON','assignment',4,'p_array_element_assignment','parser.py',366),
  ('assignment -> ID EQUAL array_initializer SEMICOLON','assignment',4,'p_array_assignment','parser.py',371),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','parser.py',378),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','parser.py',379),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','parser.py',380),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','parser.py',381),
  ('expression -> expression MODULO expression','expression',3,'p_expression_binop','parser.py',382),
  ('expression -> expression EQUALITY expression','expression',3,'p_expression_binop','parser.py',383),
  ('expression -> expression NOTEQUAL expression','expression',3,'p_expression_binop','parser.py',384),
  ('expression -> expression GREATER expression','expression',3,'p_expression_binop','parser.py',385),
  ('expression -> expression LESS expression','expression',3,'p_expression_binop','parser.py',386),
  ('expression -> expression GREATEROREQUAL expression','expression',3,'p_expression_binop','parser.py',387),
  ('expression -> expression LESSOREQUAL expression','expression',3,'p_expression_binop','parser.py',388),
  ('expression -> expression CONDITIONALAND expression','expression',3,'p_expression_binop','parser.py',389),
  ('expression -> expression CONDITIONALOR expression','expression',3,'p_expression_binop','parser.py',390),
  ('expression -> NOT expression','expression',2,'p_expression_unaryop','parser.py',395),
  ('expression -> MINUS expression','expression',2,'p_expression_unaryop','parser.py',396),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parser.py',401),
  ('expression -> literal','expression',1,'p_expression_literal','parser.py',406),
  ('expression -> ID','expression',1,'p_expression_id','parser.py',411),
  ('expression -> array_access','expression',1,'p_expression_array_access','parser.py',416),
  ('expression -> ID INCREMENT','expression',2,'p_expression_increment','parser.py',421),
  ('expression -> ID DECREMENT','expression',2,'p_expression_decrement','parser.py',426),
  ('expression -> function_call','expression',1,'p_expression_function_call','parser.py',431),
  ('function_call -> ID LPAREN arguments_opt RPAREN','function_call',4,'p_function_call','parser.py',436),
  ('arguments_opt -> arguments','arguments_opt',1,'p_arguments_opt','parser.py',440),
  ('arguments -> empty','arguments',1,'p_arguments_empty','parser.py',444),
  ('arguments -> arguments COMMA expression','arguments',3,'p_arguments_multiple','parser.py',448),
  ('arguments -> expression','arguments',1,'p_arguments_single','parser.py',452),
  ('expression_list -> expression_list COMMA expression','expression_list',3,'p_expression_list_multiple','parser.py',456),
  ('expression_list -> expression','expression_list',1,'p_expression_list_single','parser.py',460),
  ('literal -> NUMBER_LITERAL','literal',1,'p_literal_number','parser.py',466),
  ('literal -> STRING_LITERAL','literal',1,'p_literal_string','parser.py',474),
  ('literal -> BOOLEAN_LITERAL','literal',1,'p_literal_boolean','parser.py',478),
  ('type -> INT','type',1,'p_basic_type','parser.py',483),
  ('type -> FLOAT','type',1,'p_basic_type','parser.py',484),
  ('type -> BOOL','type',1,'p_basic_type','parser.py',485),
  ('type -> STRING','type',1,'p_basic_type','parser.py',486),
  ('type -> VOID','type',1,'p_basic_type','parser.py',487),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',493),
]
