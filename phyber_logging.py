from os import system
from colorama import Fore, Back, Style

def table(stuffToPrint, spacing):
        clamp = 0
        line = ''
        msg = ''
        for i in range(len(stuffToPrint[0])):
            line += stuffToPrint[0][i]
            clamp = spacing * (i + 1) - len(line)
            if clamp > 0:
                for _ in range(clamp):
                    line += ' '
        msg += Fore.BLACK + Back.YELLOW + line + Style.RESET_ALL + '\n'
        for i in range(1, len(stuffToPrint)):
            line = ''
            line += stuffToPrint[i][0]
            clamp = spacing * 1 - len(line)
            if clamp > 0:
                for _ in range(clamp):
                    line += ' '
            msg +=  Fore.GREEN + line
            line = ''
            for n in range(1, len(stuffToPrint[i])):
                line += stuffToPrint[i][n]
                clamp = spacing * (n) - len(line)
                if clamp > 0:
                    for _ in range(clamp):
                        line += ' '
            msg += Fore.WHITE + line + '\n'
        system('clear')
        print(msg)
            
                