
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def text(text1,service,DOCUMENT_ID):
    print("inside text insertion")
    text1="\n"+"\n".join(text1)+"\n"
    length=len(text1)
    requests = [
        {
            'insertText': {
                'location': {
                    'index': heading,
                },
                'text': text1
            }
        },
        {
        "updateParagraphStyle": {
            "range": {
                "startIndex": heading,
                "endIndex": heading+length
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    },
        {'updateTextStyle': {
                'range': {
                    'startIndex': heading,
                    'endIndex': heading+length
                },
                'textStyle': {
                    'bold': False,
                    'italic': True,
                    'weightedFontFamily': {
                        'fontFamily': 'Times New Roman'
                    },
                    'fontSize': {
                        'magnitude': 14,
                        'unit': 'PT'
                    },
                },
                
                'fields': 'bold,italic,weightedFontFamily,fontSize'
            }}
    ]
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

def main(URL="",text1=""):
    SCOPES=['https://www.googleapis.com/auth/documents']
    DOCUMENT_ID = '1pcZfzwKwCL2P4bCccT41ow-HE6sNcYNgXWqLpFMMcQI'
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        
    service = build('docs', 'v1', credentials=creds)
    if len(URL)>0:
        image(URL,service,DOCUMENT_ID)
    else:
        text(text1,service,DOCUMENT_ID)

def image(URL,service,DOCUMENT_ID):
    print("inside image insertion")
    requests = [{
            'insertText': {
                'location': {
                    'index': heading,
                },
                'text': "\n"
            }
        },
    
    {
    'insertInlineImage': {
        'location': {
            'index': heading+1
        },
        'uri':
            URL,
        'objectSize': {
            'height': {
                'magnitude': 200,
                'unit': 'PT'
            },
            'width': {
                'magnitude': 200,
                'unit': 'PT'
                }
            }
        }
    },
    {
            'insertText': {
                'location': {
                    'index': heading+2,
                },
                'text': "\n"
            }
        },
    {
        "updateParagraphStyle": {
            "range": {
                "startIndex": heading,
                "endIndex": heading+3
            },
            "paragraphStyle": {
                "alignment": "CENTER"
            },
            "fields": "alignment"
        }
    }

    ]
    body = {'requests': requests}
    response = service.documents().batchUpdate(documentId=DOCUMENT_ID, body=body).execute()
    #insert_inline_image_response = response.get('replies')[0].get('insertInlineImage')
    #print('Inserted image with object ID: {0}'.format(insert_inline_image_response.get('objectId')))

    
heading=35
if __name__ == '__main__':
    main("https://images-na.ssl-images-amazon.com/images/I/718TqGvI%2BnL._AC_UX679_.jpg")
    main(text1=["yash","khandelwal","yo","tot","ruru"])
    #text()
