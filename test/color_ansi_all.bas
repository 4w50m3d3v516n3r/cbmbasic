10 SYS 1: REM Turn on extensions
20 FOR F=30 TO 37
30 FOR B=40 TO 47
40 FOR A=0 TO 8
50 ANSISGM A,F,B:PRINT "TEST STRING";:ANSISGM 0,37,40:PRINT "Attr:";A;"FG:";F;"BG:";B
60 NEXT A:NEXT B:NEXT F
70 ANSISGM 0,37,40:PRINT