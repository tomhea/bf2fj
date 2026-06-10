DIM M(5)
M(0) = 1: M(1) = 3: M(2) = 1: M(3) = 0: M(4) = 0: M(5) = 0: M(6) = 0
X = 2
DO WHILE M(0) <> 0
  M(X) = ASC(INPUT$(1))
  M(X) = M(X) - 8
  DO WHILE M(X) <> 0 'not backspace
    M(X) = M(X) - 5
    DO WHILE M(X) <> 0 'not enter
      'normal character
      DO WHILE M(1) <> 0 'at end?
        
        EXIT DO
      LOOP
      M(X) = 0
    LOOP
    M(X) = 0
  LOOP
LOOP

