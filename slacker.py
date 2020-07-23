import pyautogui as auto
import PySimpleGUI as sg
import time
import threading
import ctypes

def move_mouse():
    '''
    Move the mouse back and forth. Click after every other move.
    '''
    while True:
        auto.moveRel(-100, 0, duration=0.2)
        auto.click()
        time.sleep(3)
        auto.moveRel(100, 0, duration=0.2)
        time.sleep(3)

class thread_with_exception(threading.Thread): 
    def __init__(self, name, target, daemon): 
        threading.Thread.__init__(self, target=target, daemon=daemon) 
        self.name = name
           
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 

def interface():
    '''
    Load the GUI for the user and allow input for the desired duration
    of the program.
    '''
    sg.theme('Reddit')

    layout = [ [sg.Text('Status:'), sg.Text('Stopped', key='-STATUS-', text_color='red'),
               sg.Button('Start', key='-START-'), sg.Button('Stop', key='-STOP-')] ]

    window = sg.Window('Slacker', layout, element_justification='center', size=(250,40))

    while True:
        event, _ = window.read(timeout=10)

        if event is None:
            break

        if event == '-START-' and window['-STATUS-'].get() == 'Stopped':
            window['-STATUS-'].update('Slacking', text_color='green')
            thread_id = thread_with_exception('Thread 1', target=move_mouse, daemon=False)
            thread_id.start()
            print(f'{thread_id} started')
        
        if event == '-STOP-' and window['-STATUS-'].get() == 'Slacking':
            window['-STATUS-'].update('Stopped', text_color='red')
            thread_id.raise_exception()
            thread_id.join()
            print(f'{thread_id} killed')
            
    
    window.close()

if __name__ == "__main__":
    interface()