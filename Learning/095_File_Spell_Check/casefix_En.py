# Correct casing for some IT words
# 
# 2022-07-04 PV     Exceptions moved to specialcasing.txt file

# casefix = ['2D', '3D', 'PHP', 'SQL', 'MySQL', 'UML', 'C', 'WCF', 'VBA', 'XML', 'HTML', 'InDesign', 'CSS', 'HTML5', 'CSS3',
#            'NetBeans', 'JavaScript', 'MFC', 'UI', 'UX', 'XSLT', 'API', 'PowerShell', 'BI', 'AutoCAD', 'jQuery', 'GraphQL',
#            'Hands-on', 'WPF', 'WCF', 'COM', 'OpenGL', 'JavaFX', 'DirectX', 'SharePoint', 'WebGL', 'TensorFlow', 'asyncio', 'EE',
#            'SVG', 'PowerApps', 'API', 'APIs', 'PyGTK', 'GTK', 'GameMaker', 'PySpark', 'RPG', 'DepOps', 'MVC', 'CDI', 'TBB',
#            'HLSL', 'ABAP', 'WebSocket', 'WebAssembly', 'JST', 'MooTools', 'MVVM', 'PyGame', 'JRuby', 'VB', 'PayPal', 'ZK',
#            'LINQ', 'GUI', 'eBook', 'PyQt', 'RegExp', 'PyCharm', 'sed', 'FAQ', 'FAQs', 'QuickStart', 'C++', 'C#', 'DevOps',
#            'TypeScript', 'MATLAB', 'p5', 'hapi', 'NET', 'AWS', 'OpenGL', 'OpenCV', 'ASP', 'IoT', 'MongoDB', 'PostgreSQL',
#            'CS', 'DOM', ]

with open(r'words\specialcasing.txt', 'r', encoding='UTF-8') as f:
    set_casefix = set(mot for mot in f.read().splitlines())
dic_casefix = dict([(mot.casefold(), mot) for mot in set_casefix])

def process_exceptions_En(s):
    return s.replace('Hands-On', 'Hands-on').replace('.Js', '.js').replace('Add-In', 'Add-in') \
        .replace('Step-By-Step', 'Step-by-Step').replace('.X ', '.x ').replace('Start-Up', 'Start-up') \
        .replace(' T SQL', ' T-SQL').replace('End-To-End', 'End-to-End').replace('How-to', 'How-To')
