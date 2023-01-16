import PySimpleGUI as sg
import pyperclip
import json
import webbrowser
import re

# The assumption is to create the url to the docs page is the second part of the function name xxx.[#####].lower()
# e.g algo.movePivotPointToTargetedOccurrenceCenter = https://www.pixyz-software.com/documentations/html/2022.1/studio/api/#movepivotpointtotargetedoccurrencecenter
# Works for most, but not all cases
baseURL = "https://www.pixyz-software.com/documentations/html/2022.1/studio/api/#"

# Path to pixyz auto completion for VS Code stored in the current directory
# Generated using https://gitlab.com/pixyz/samples/studio/ide-auto-completion/-/blob/master/generate_auto_completion_libs.py 
apiPath = "./python.json"


apiJson = dict()
apiKeys = []

searchResults = []
selectedKey = ""
selectedPrefix = ""
selectedBody = ""
selectedDesc = ""

def main():
    # --------------------------------- Define Layout ---------------------------------
    search_col = [[sg.Text('Search'), sg.In(size=(25,1), enable_events=True ,key='-SEARCH-')],
                [sg.Listbox(values=apiKeys, enable_events=True, size=(35,30),key='-SELECTION-')]]

    selection_col = [[sg.Image('./logo.png')],
                  [sg.Text("", key='Selected-Key', font='Any 18')],
                  [sg.Text("", size=(50,5), key='Selected-Desc')],
                  [sg.Multiline("", size=(50,5), key='Selected-Body')],
                  [sg.Button('Copy Code'), sg.Button('Open API Documentation')]]

    # ----- Full layout -----
    layout = [[sg.Column(search_col), sg.VSeperator(), sg.Column(selection_col)]]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('Pixyz API Search', layout)

    # ----- Run the Event Loop -----
    # --------------------------------- Event Loop ---------------------------------
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        # If search input has changed
        if event == '-SEARCH-':
            searchValue = values['-SEARCH-'].lower()
            try:
                # Reset if input is empty
                if not searchValue:
                    window['-SELECTION-'].update(apiKeys)

                else:
                    # Filter results based in search input 
                    searchResults = search(apiKeys, f'{searchValue}')
                    window['-SELECTION-'].update(searchResults)
            except:
                pass
        # If a list item was selected
        elif event == '-SELECTION-':
            try:
                selectedKey = values['-SELECTION-'][0]
                selectedBody = apiJson[selectedKey]["body"]
                selectedDesc = apiJson[selectedKey]["description"]

                window['Selected-Key'].update(selectedKey)
                window['Selected-Body'].update(selectedBody)
                window['Selected-Desc'].update(selectedDesc)
            except:
                pass        # something weird happened 

        elif event == 'Copy Code':
            pyperclip.copy(selectedBody)
            print(f"Copy Code: {selectedBody}")

        elif event == 'Open API Documentation':
            urlKey = selectedKey.split('.')[1]
            url = baseURL + urlKey.lower()
            webbrowser.open(url)
            print(f"Open API Documentation: {url}")

    # --------------------------------- Close & Exit ---------------------------------

    window.close()

def search(list, query:str):
    pattern = '.*' + query + '.*'
    return [x for x in list if re.match(pattern, x, re.IGNORECASE)]

if __name__ == "__main__":
    # Themes are cool
    # https://csveda.com/pysimplegui-themes-text-input-multiline-and-button/
    #sg.theme('DarkGrey15')
    sg.theme('DarkGrey13')

    #sg.theme('DarkBlack')

    with open(apiPath) as json_file:
        apiJson = json.load(json_file)
        for key in apiJson:
            apiKeys.append(str(key))
        
        main()
