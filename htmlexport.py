import sys
import json

THEME = "dark"
LANG = "python"


class HTMLExportFormatter:

    def __init__(self, theme, lang):
        self.theme = dict()
        with open('theme/%s.json' % (theme), 'r') as file:
            self.theme = json.loads(file.read())
        
        self.lang = dict()
        with open('lang/%s.json' % (lang), 'r') as file:
            self.lang = json.loads(file.read())

    def getStyleSource(self):
        source = '<style>\n'
        if('background' in self.theme):
            source += 'body{background-color:' + self.theme['background'] + '}\n'
        if('default' in self.theme):
            source += 'body{color:' + self.theme['default'] + '}\n'
        if('font' in self.theme):
            source += 'body{font-family:' + self.theme['font'] + '}\n'
        for colorKey in self.theme['colors']:
            source += '.color-' + colorKey + '{color:' + self.theme['colors'][colorKey] + '}\n'
        source += '</style>'
        return source

    def processLine(self, line):
        for highlightKey in self.lang['highlight']:
            if highlightKey in line:
                line = line.replace(highlightKey, '<p class="color-%s">%s</p>' % (self.lang['highlight'][highlightKey], highlightKey) )
        #line = line.replace(' ', '&nbsp;')
        return line + '<br>'

    def getSource(self, input, title):
        source = ''
        for line in self.exportStream(input):
            source += line
        with open('preset.html', 'r') as file:
            return file.read() % (title, self.getStyleSource(), source)

    def exportStream(self, input):
        for line in input:
            yield self.processLine(line)

    def exportFile(self, origin, target):
        with open(origin, 'r') as inputFile:
            outputFile = open(target, 'w')
            outputFile.write(self.getSource(inputFile, origin))
            outputFile.flush()
            outputFile.close()

if __name__ == '__main__':
    formatter = HTMLExportFormatter(THEME, LANG)
    formatter.exportFile('example.py', 'example.html')
