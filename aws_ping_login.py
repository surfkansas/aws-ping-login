import argparse
import os
import wx 
import wx.html2 
import boto3
from bs4 import BeautifulSoup

class MyBrowser(wx.Frame): 
    def __init__(self, *args, **kwds): 
        wx.Frame.__init__(self, *args, **kwds) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.browser = wx.html2.WebView.New(self) 
        sizer.Add(self.browser, 1, wx.EXPAND, 10) 
        self.SetSizer(sizer) 
        self.SetSize((700, 700)) 
        self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.OnNavigate, self.browser)

    def OnNavigate(self,evt):
        if self.browser.GetCurrentURL() == 'https://signin.aws.amazon.com/saml':
            page_source = self.browser.GetPageSource()
            self.Close()
            soup = BeautifulSoup(page_source, 'html.parser')
            base64saml = soup.find('input', {'name': 'SAMLResponse'})['value']
            self.saml = base64saml

def execute_login_dialog(args):
    app = wx.App() 
    dialog = MyBrowser(None, -1) 
    dialog.browser.LoadURL(args.sso_url) 
    dialog.Show() 
    app.MainLoop() 
    return dialog.saml    

def process_login(args):

    saml = execute_login_dialog(args)

    role_arn = 'arn:aws:iam::{0}:role/{1}'.format(args.account, args.role)
    principal_arn = 'arn:aws:iam::{0}:saml-provider/KBSPingFed'.format(args.account, args.saml_provider)
    session_duration = int(args.session_duration) * 60

    sts = boto3.client('sts')

    sts_session = sts.assume_role_with_saml(   
        RoleArn=role_arn,
        PrincipalArn=principal_arn,
        SAMLAssertion=saml,
        DurationSeconds=session_duration
    )

    os.system('aws configure --profile {0} set aws_access_key_id {1}'.format(args.profile, sts_session['Credentials']['AccessKeyId']))
    os.system('aws configure --profile {0} set aws_secret_access_key {1}'.format(args.profile, sts_session['Credentials']['SecretAccessKey']))
    os.system('aws configure --profile {0} set aws_session_token {1}'.format(args.profile, sts_session['Credentials']['SessionToken']))
    if args.region is not None:
        os.system('aws configure --profile {0} set region {1}'.format(args.profile, args.region))

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--sso-url')
    parser.add_argument('--saml-provider')
    parser.add_argument('--account')
    parser.add_argument('--role')
    parser.add_argument('--profile')
    parser.add_argument('--region')
    parser.add_argument('--session-duration')

    args = parser.parse_args()

    process_login(args)

if __name__ == "__main__":
    main()
