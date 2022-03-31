#PDF Attachment Extractor

import PyPDF2

def getAttachments(reader):
      """
      Retrieves the file attachments of the PDF as a dictionary of file names
      and the file data as a bytestring.
      :return: dictionary of filenames and bytestrings
      """
      catalog = reader.trailer["/Root"]
      fileNames = catalog['/Names']['/EmbeddedFiles']['/Names']
      attachments = {}
      for f in fileNames:
          if isinstance(f, str):
              name = f
              dataIndex = fileNames.index(f) + 1
              fDict = fileNames[dataIndex].getObject()
              fData = fDict['/EF']['/F'].getData()
              attachments[name] = fData

      return attachments


handler = open('E:\yourfile.pdf', 'rb')
reader = PyPDF2.PdfFileReader(handler)
dictionary = getAttachments(reader)
print(dictionary)
for fName, fData in dictionary.items():
    with open(fName, 'wb') as outfile:
        outfile.write(fData)
