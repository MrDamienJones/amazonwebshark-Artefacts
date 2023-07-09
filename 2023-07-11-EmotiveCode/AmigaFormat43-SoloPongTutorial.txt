` ** Amiga Format Solo Pong **
` **
Curs Off
Hide
Double Buffer
Paper 0
Ink 7
Bar 0,0 To 5,30
Ink 2
Polyline 0,30 To 0,0 To 5,0
Get Sprite 1,0,0 To 6,31
Cls 0
Ink 2
Circle 5,5,2
Paint 5,5
Get Sprite 2,0,0 To 10,10
Limit Mouse X Hard(0,0), Y Hard(0,5) To X Hard(0,0), Y Hard(0,165)
Cls 0
Pen 4
Locate 0,7
Centre `Amiga Format`
Locate 0,9
Centre `Presents`
Locate 0,11
Centre `the vey excellent`
Pen 3
Locate 0,13
Centre `A F   S O L O   P O N G`
Locate 0,24
Pen 2
Centre `<press a key>`
Wave 0 To 15
NOISE
Wait Key
`
RESTART:
Cls 0
Ink 11
Bar 0,0 To 320,5
Bar 0,194 To 320,200
Ink 2
Bar 160,0 To 165,193
Pen 4
Locate 0,0
Centre `AF Solo Pong`
X=150 : Y=100
DX=Rnd(4)+2 : DY=Rnd(2)+1
R1=Rnd(10) : If R1>5 Then DX=-DX
R2=Rnd(10) : If R2>5 Then DY=-DY
`
MAIN:
Add X,DX : Add Y,DY : If Y<=5 or Y>=190 Then DY =-DY
Z1=Bob Col(1) : Z2=Bob Col(2) : If Bob Col(4) Then DX=-DX
If X>=320 Then LOSE : Goto RESTART
If X<=-20 Then LOSE : Goto RESTART
If Z1<>0 Then DX=-DX : DX=Rnd(5)+3
If Z2<>0 Then DX=Rnd(5)+3 : DX=-DX
Y1=Y Screen(Y Mouse)
Bob 1,5,Y1,1
Bob 2,310,Y1,1
Bob 3,X,Y,2 : Wait 1
Goto MAIN
,
Procedure LOSE
	Boom
	Pen 3
	Centre `Game Over, Man`
	Locate 0,24
	Centre `<press a key>`
	Wait Key
End Proc
`
Procedure NOISE
	For L=79 To 0 Step -1
		Play 96-(20+(L/2)),0
		Wait 1
	Next L
End Prod