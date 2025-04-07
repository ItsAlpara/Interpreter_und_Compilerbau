%%
[0-9]+ printf ("Zahl : % s \n", yytext);
[a-zA-Z]+ printf ("Wort : % s \n", yytext);
.  printf ("Unbekanntes Zeichen\n");
%%
int main () {
// Lexer - Code
yylex ();
return 0;
}
