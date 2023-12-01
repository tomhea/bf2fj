(*
    The Towers of Hanoi -- Preparation for the Brainfuck version
    Copyright (C) 2002  Roland Illig <1illig@informatik.uni-hamburg.de>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*)

program hanoi;

var
  stack: array [0..15] of record
    recurse: Boolean;
    step: Integer;
    next: Integer;
    a, b, c: Char;
    n: Integer;
  end;
  sp: Integer;

procedure push(next: Integer; a, b, c: Char; n: Integer);
begin
  Inc(sp);
  stack[sp].recurse := True;
  stack[sp].step := 0;
  stack[sp].next := next;
  stack[sp].a := a;
  stack[sp].b := b;
  stack[sp].c := c;
  stack[sp].n := n;
end;

begin
  sp := 0;
  fillchar(stack, sizeof(stack), 0);
  push(4, 'a', 'b', 'c', 3);
  stack[sp].step := 4;
  while (stack[sp].recurse) do
    begin
      while (stack[sp].step <> 0) do
        begin
          case (stack[sp].step) of
            4:
              begin
                stack[sp].next := 3;
                if (stack[sp].n > 1) then
                  push(4, stack[sp].a, stack[sp].c, stack[sp].b, stack[sp].n - 1);
              end;
            3:
              begin
                stack[sp].next := 2;
                push(1, stack[sp].a, stack[sp].b, stack[sp].c, 1);
              end;
            2:
              begin
                stack[sp].next := 0;
                if (stack[sp].n > 1) then
                  push(4, stack[sp].b, stack[sp].a, stack[sp].c, stack[sp].n - 1);
              end;
            1:
              begin
                stack[sp].next := 0;
                WriteLn('von ', stack[sp].a, ' nach ', stack[sp].c, '.');
              end;
          end;
          stack[sp].step := stack[sp].next;
        end;
      Dec(sp);
      stack[sp].step := stack[sp].next;
    end;
  WriteLn('fertig.');
end.
