import random
from hardware import solenoid,display

def teken_hint(locatie,kleur):
    display.paint_dot([(locatie+1) * 64, 240//2], 20, kleur)

sub_code = [i for i in range(10)]
for i in range(100):
    a = random.randint(0,9)
    b = random.randint(0,9)
    t = sub_code[a]
    sub_code[a] = sub_code[b]
    sub_code[b] = t

code = f"{sub_code[0]}{sub_code[1]}{sub_code[2]}{sub_code[3]}"

code_input = ""
guess_count = 0
while guess_count < 10 and code != code_input:
    if(guess_count > 0):
        print("code is fout!")
    guess_count += 1
    print(f"dit is poging {guess_count}")
    code_input = input()
    while len(code_input) != 4:
        print("foute invoer, voer een code van 4 cijfers in!")
        code_input = input()
    display.clear_display()
    
    # DE OPDRACHT BEGINT HIERRRRRRRRRRRR.....................
    for getal in range(len(code)):
        
        if code_input[getal] == code[getal]:
            # ALS JE NUMMER OVEREENKOMT MET HET NUMMER VAN DE CODE:
    
            pass
        elif code_input[getal] in code:
            # ALS JE NUMMER VOORKOMT MET EEN NUMMER VAN DE CODE, MAAR NIET OP DEZELFDE PLAATS:
            
            pass
        else:
            #ALS JE NUMMER NIET VOORKOMT IN DE CODE:
            
            pass


if code == code_input:
    print("je hebt het geraden")
    solenoid.open()
else:
    print(f"je hebt het niet geraden, het antwoord was: {code}")


