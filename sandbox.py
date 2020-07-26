import PySimpleGUI as sg
from config import Config
import os

sg.theme('Reddit')

license_layout = [ [sg.Text('Enter your license key. It can be found in the email you receive after purchase:',
                justification='center', font=10)],
           [sg.Input(size=(5,1), key='LICENSE1', enable_events=True), sg.Text('-'),
            sg.Input(size=(5,1), key='LICENSE2', enable_events=True), sg.Text('-'),
            sg.Input(size=(5,1), key='LICENSE3', enable_events=True), sg.Text('-'),
            sg.Input(size=(5,1), key='LICENSE4', enable_events=True)],
           [sg.Button('OK', key='OK'), sg.Button('Cancel', key='CANCEL')] ]

license_window = sg.Window('License Key', license_layout, element_justification='center', finalize=True)

if os.path.isfile('license.txt'):
        print('License file found. Decrypting ...')
        c = Config()
        token = c.r()
        license = c.z(token)
        print(license)

else:
    while True:

        event, _ = license_window.read()

        if event is None or event == 'CANCEL':
            break

        if event[:-1] == 'LICENSE':
            if len(license_window[event].get()) > 5:
                license_window[event].update(license_window[event].get()[:-1])

        if event == 'OK':
            l1 = license_window['LICENSE1'].get()
            l2 = license_window['LICENSE2'].get()
            l3 = license_window['LICENSE3'].get()
            l4 = license_window['LICENSE4'].get()

            parts = [l1, l2, l3, l4]
            if '' in parts:
                sg.popup_non_blocking('Please fill out each box of the license key.', title='Warning')
            else:
                license = '-'.join(parts)
                print(f'Raw: {license}')

                if license == '12345-67890-54321-09876':
                    print('License is valid.')
                    c = Config()
                    key = bytes(license, encoding='ascii')
                    token = c.a(key)
                    print(f'Token: {token}')
                    c.c(token)
                else:
                    print('License is invalid.')