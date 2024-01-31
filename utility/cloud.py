from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("./docs/mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile("./docs/mycreds.txt")

drive = GoogleDrive(gauth)

folderID = '1VW3jHXlaUd_tpCWvA3xG_vv3HX5xTHPK'
bound_folderID = '1_Vl6mZe4LKMe-9bV3M0d6JxOugAiW_IN'

def uploadFile(uploaded_file,bounding_vid=0):
    if bounding_vid == 1:
        file_list = drive.ListFile({'q': "'1_Vl6mZe4LKMe-9bV3M0d6JxOugAiW_IN' in parents and trashed=false"}).GetList()
    else:
        file_list = drive.ListFile({'q': "'1VW3jHXlaUd_tpCWvA3xG_vv3HX5xTHPK' in parents and trashed=false"}).GetList()
    file_names = []
    if len(file_list) != 0:
        for file in file_list:
            file_names.append(int(file['title'].split(".")[0]))
    else:
        file_names = [0]
    max_num = max(file_names)
    if bounding_vid == 1:
        file = drive.CreateFile({'title':f'{max_num+1}.mp4','parents': [{'id': f'{bound_folderID}'}]})
    else:
        file = drive.CreateFile({'title':f'{max_num+1}.mp4','parents': [{'id': f'{folderID}'}]})
    file.SetContentFile(uploaded_file)
    file.Upload()
    permission = file.InsertPermission({
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'})
    return file['embedLink']