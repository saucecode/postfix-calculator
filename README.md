# postfix-calculator
An awesome [postfix (RPN)](https://en.wikipedia.org/wiki/Reverse_Polish_notation) calculator in python 2 &amp; 3.

    $ python postfix.py

Supports commands `+ - * / ** % sqrt sin cos tan asin acos atan ln log rad deg Re Im =`  
Trigonometry is done in radians. Use `rad` and `deg` to convert to radians and degrees respectively.

**Dimensional analysis and dimensioned number support added as of version 8.**

Numbers can be input in Python's `a+bj` format. Comes with `pi`, `e`, and `i` as variables. The answer of the last operation is put into variable `\`.

### Commands
**Variable Assignment** -- The answer of the last operation is put into `\`

    > 2 pi * tau =           ; tau = 2*pi
     6.28318530718
    
    > tau cos                ; cos(tau)
     1.0
    
    > 8+3j 2 /               ; (8+3i)/2
     (4+1.5j)
    
    > \ 2.5 -                ; (4+1.5j) - 2.5
     (1.5+1.5j)

**Arithmetic & Expoentiation**

    > 2 5 4 - * 4 /          ; 2*(5-4)/6
     0.3333333333333333
    
    > 2 8 **                 ; 2^8
     256.0
    
    > 1 2 sqrt /             ; 1/sqrt(2)
     0.707106781187

**Dimensioned Numbers**

The calculator supports meters, seconds, kilograms, Kelvin, and Coulomb as `m, s, kg, K, C`

    > 10kg 4s / massflow =     ; massflow = 10/4 kg/s
     2.5kg/s
    
    > massflow 1.52kg/m^3 /  ; 2.5kg/s / 1.52 kg/m^3 = 1.645m^3/s
     1.644736842105263m^3/s
    
    > 1.005kg.m^2/s^2/kg/K Cp = ; Specific Heat of Water: 1.005 J/(kg K)
    > Cp massflow * 80s * 35K * ; 1.005 J/(kg K) * 2.5 kg/s * 80 s * 35 K = 7035 J
     7035kg.m^2/s^2.0
    
    > 4m/s 3s **                ; (4 m/s) ^ (3s) -- Issues a warning
     64m/s
    
    > 10kg 20s +                ; 10 kg + 20 s -- Issues a warning
     30kg

The calculator will only warn when dimensions are potentially misused. It will still return an answer, with either no dimensions, or the dimension of the left-most symbol.

You can also put dimensions on complex numbers, if you're feeling particularly devilish. There will be no warnings.

**Logarithms**

    > e 32 ** ln             ; ln(e^32)
     32.0
    
    > 1500 10 log            ; log_10(1500)
     3.17609125906
    
    > 10 \ **                ; 10^3.17609125906
     1500.0

**Trigonometry** -- rad converts to radians, deg converts to degrees

    > 30 rad cos asin deg    ; 180/pi * asin( cos( 30 * pi/180 ) )
     60.0

**Complex Numbers** -- Python's `a+bj` format can be used.

    > -1 sqrt 0+1j **           ; sqrt(-1)^sqrt(-1)
     0.207879576351
    
    > e pi i * **            ; Euler's Identity  e^(i*pi) = -1  (plus rounding error)
     (-1+1.22464679915e-16j)
    
    > e i 120 rad * ** z =   ; z = e^(i*120*pi/180)    (A cube root of 1)
     (-0.5+0.866025403784j)
    
    > z 3 **                 ; z^3 = 1  (plus rounding error)
     (1-6.10622663544e-16j)
    
    > z arg deg              ; arg(z) * 180/pi
     120.0

### Changelog
**version 7**
 - Added complex numbers suport

**version 8 (still testing)**
 - Added dimensional analysis
