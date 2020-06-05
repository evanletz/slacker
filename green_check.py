import pyautogui as auto
import PySimpleGUI as sg
import time
import subprocess

def move_mouse():
    '''
    Move the mouse back and forth. Click after every other move.
    '''
    while True:
        auto.moveRel(100, 0, duration=0.2)
        time.sleep(5)
        auto.moveRel(-100, 0, duration=0.2)
        auto.click()

def interface():
    '''
    Load the GUI for the user and allow input for the desired duration
    of the program.
    '''
    sg.theme('Reddit')

    layout = [ [sg.Text('Status:'), sg.Text('Stopped', key='-STATUS-', text_color='red'),
               sg.Button('Start', key='-START-'), sg.Button('Stop', key='-STOP-')] ]

    window = sg.Window('Green Check', layout, element_justification='center', size=(250,40))

    while True:
        event, values = window.read()
        print(event, values)
        if event == '-START-' and window['-STATUS-'].get() == 'Stopped':
            window['-STATUS-'].update('Running', text_color='green')
            sp = subprocess.Popen(["python", '-c', 'from green_check import move_mouse; move_mouse()'])
        if event == '-STOP-' and window['-STATUS-'].get() == 'Running':
            window['-STATUS-'].update('Stopped', text_color='red')
            sp.kill()
        if event is None:
            break
    window.close()

if __name__ == "__main__":
    interface()