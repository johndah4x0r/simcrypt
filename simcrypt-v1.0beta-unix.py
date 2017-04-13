#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
SimpleCrypt, a simple Caesar cipher program

This program's focus is to be simple and lightweight

This program is using a chain instead of using a main function
which executes all functions one by one.
The program architecture:
menu() -> startCrypt() -> cryptFunc() -> done!
'''

import os
import sys
from time import sleep
import time

# variables & data
upperSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowerSet = upperSet.lower()
excluded = "0123456789!\"@#$%&/()=+?-^*~,. "
charSet = (upperSet, lowerSet, excluded)


def clear():
    '''Clear the screen. Might only work
with terminals that support ANSI'''

    # print out \033c
    sys.stdout.write("\033c")
    sys.stdout.flush()
    
def menu():
    '''The menu (__main__ function substitute)'''
    global verbose

    clear()
    print(12 * "-", "SimpleCrypt", 12 * '-')
    print("Version: simcrypt-v1.0beta")
    print('-' * len((12 * "-"+' SimpleCrypt '+ 12 * '-')))
    print("1. Start")
    print("2. Help")
    print("3. Exit")
    print(37 * '-')
    print("Welcome to SimpleCrypt (simcrypt-v1.0beta)")
    verbose = input ("Allow logging (warning: personal info also logged)? (y/N): ").strip()
    if verbose in ('y', 'Y', '1', 'yes'):
        verbose = True
    elif verbose in ('n', 'N', '0', 'no'):
        verbose = False
    else:
        verbose = False
    
    option = False
    while not option:
        option = input("Option  [1-3]: ")
        if option == "1":
            result = startCrypt()
        elif option == "2":
            clear()
            helpScreen()
            clear()
            menu()
        elif option == "3":
            print("Clearing the screen for privacy sake...")
            sleep(0.5)
            clear()
            exit()
        else:
            print("Invalid option!")
            option = False
            none = input("Press Enter to continue...")
            del none
            clear()
            menu()
    print(12 * "-", 'Result', 12 * '-')
    print("Output: {0}".format(result))
    sys.exit()
    
def helpScreen():
    '''Help screen'''
    helpStr = '''\
Help:
You really don't need help for this program!
It\'s so simple!
1.  When the menu pops up, enter 1.
2.  Enter the message when asked to do so.
3.  Choose if you wanna scramble (1) or descramble (2)
    the message you entered.
4.  Let the power of programming do it\'s job...
5.  Volia! Processing finished! The program will clear the
    screen for you, if you wish (clear the screen for the
    sake of privacy)'''

    print(helpStr)
    none = input("Press Enter to continue...")
    del none

def startCrypt():
    '''Starts the ciphering process'''
    message = input("Enter the message: ").strip()
    if not message:
        print("Note: Cannot start without message! Will go to demo mode...")
        message = "The quick brown fox jumps over the 13 lazy dogs!!"
        sleep(0.5)
    clear()

    print("-" * 12, "Encryption options", "-" * 12)
    print("1. Scramble message")
    print("2. Descramble message")
    print("-" * len(''.join("-" * 12+" Encryption options "+"-" * 12)))

    ans = False
    while not ans:
        ans = input("Encrypt or decrypt? [1-2]: ")
        if ans == "1":
            shifts = getShifts('e')
        elif ans == "2":
            shifts = getShifts('d')
        else:
            print("Invalid option! Try again!\n")
            ans = False
        
    output = cryptFunc(message, shifts)
    return output

def cryptFunc(target, shifts):
    '''The encryption function'''
    writeLog("target = ", target)
    writeLog("shifts =", shifts)
    
    t_len = len(target)
    writeLog("targetLen =", t_len)
    iteration = 0
    result = ''
    for i in range(t_len):
        iteration += 1
        printProgress(iteration, t_len)
        writeLog("chrNum: #", i)
        currentChar = target[i]
        writeLog("current char chosen (currentChar) =", currentChar)
        if currentChar in charSet[2]:
            writeLog("current char (currentChar) is in charSet[2]. Excluded for processing.")
            result += currentChar
            writeLog("result += currentChar")
            continue
        if currentChar.isupper():
            writeLog("currentChar.isupper() =", True)
            writeLog("using charSet[0] (upperSet)")
            charMap = charSet[0]
        elif currentChar.islower():
            writeLog("currentChar.isupper() =", False)
            writeLog("using charSet[1] (lowerSet)")
            charMap = charSet[1]
        
        chrPos = charMap.find(currentChar)
        writeLog("chrPos =", chrPos)
        writeLog("adding", chrPos, "to", shifts, "(chrPos + newPos) % 26")
        newPos = (chrPos + shifts) % 26
        newChr = charMap[newPos]
        writeLog("newChr =", newChr)
        writeLog("result += newChr")
        result += newChr
    return result
    print("\n")
    
def printProgress(current, total):
    if current == total:
        percentage = total
    elif current == 0:
        percentage = 0
    else:
        percentage = 100 * abs(current/total)
        percentage = int(percentage)

    print("Processed: {0}% [{1}/{2}]".format(str(percentage),str(current),str(total)), end='\r')

def writeLog(*output):
    '''Write out *output to stderr'''
    procName = "simcrypt"
    currentTime = ":".join(str(t) for t in time.gmtime()[3:6])
    logoutput = "("
    logoutput += procName + ":"+currentTime
    logoutput += "): "
    logoutput += " ".join(str(i) for i in output)
    
    if verbose:
        logfile = open("/tmp/.simcrypt.log", "a")
        logfile.write(logoutput+"\n")
    else:
        pass
    
    sleep(0.005)
def getShifts(mode):
    shifts = input("Enter shifts [1-26]: ")
    
    try:
        shifts = int(shifts)
    except:
        print("Invalid input!\n")
        getShifts(mode)
    
    if shifts == 0:
        print("Cannot accept 0 as shfits value!\n")
        getShifts(mode)
    elif shifts > 26:
        print("Shifts is too much than 26! Can't take more!\n")
        shifts %= 26
    
    if mode == "e":
        shifts = shifts
    elif mode == "d":
        shifts = - shifts
    else:
        raise NameError("Options are: \'e\' and \'d\', not \'"+mode+"\'")
    
    return shifts

def initLog():
    logfile = open("/tmp/.simcrypt.log", "a")
    logfile.write("[initSymCrypt] ")
    currentDate = "/".join(str(i) for i in time.gmtime()[0:3])
    currentTime = ":".join(str(i) for i in time.gmtime()[3:6])
    output = (12*"-"+currentDate+" "+currentTime+12*"-"+"\n")
    logfile.write(output)
    logfile.close()
    
if __name__ == '__main__':
    initLog()
    try:
        menu()
    except (KeyboardInterrupt,EOFError):
        verbose = True
        writeLog("Ctrl-C / Ctrl-D detected (KeyboardInterrupt/EOFError)")
        print("\n")
        print("Exiting...\n")
        exit(2)
    except Exception as err:
        verbose = True
        writeLog("Python Environment Error (Exception)")
        writeLog("ErrMsg:", err)
        print("Something wrong has happend!")
        print("ERRMSG:", str(err))
        exit(1)
