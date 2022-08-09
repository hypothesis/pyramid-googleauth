
## Usage

To use pyramid-googleauth with your Pyramid app:

### 1. Create a Google client ID and secret

1. Register a Google OAuth client:

   1. Create a new **Google Cloud Platform project**.

      Go to https://console.cloud.google.com/projectcreate and create a new project,
      or use an existing Google Cloud Platform project.

   2. Configure the project's **OAuth consent screen** settings:

      1. Go to https://console.cloud.google.com/apis/credentials/consent
         and make sure the correct project is selected from the projects
         dropdown menu in the top left.

      2. Under **User Type** select **Internal** and then click <kbd>CREATE</kbd>.

         Note that **Internal** means that only users within the Google
         organization that contains the project will be able to log in.
         If you want _anyone_ to be able to log in to your app with their
         Google account you have to select **External**.

      3. Fill out the app name, user support email and other fields and click <kbd>SAVE AND CONTINUE</kbd>.

      4. On the **Scopes** screen click <kbd>ADD OR REMOVE SCOPES</kbd>,
         select the `..auth/userinfo.email`, `..auth/userinfo.profile` and `openid` scopes,
         and click <kbd>UPDATE</kbd> and <kbd>SAVE AND CONTINUE</kbd>.

   3. Configure the project's **Credentials** settings:

      1. Go to https://console.cloud.google.com/apis/credentials
         and make sure the correct project is selected from the projects
         dropdown menu in the top left.

      2. Click <kbd><kbd>CREATE CREDENTIALS</kbd> &rarr; <kbd>OAuth client ID</kbd></kbd>.

      3. Under **Application type** select **Web application**.

      4. Enter a **Name**.

      5. Under **Authorized redirect URIs** click <kbd>ADD URI</kbd> and enter
         `https://<YOUR_DOMAIN>/googleauth/login/callback`.

      6. Click <kbd>CREATE</kbd>.

      7. Note the **Client ID** and **Client Secret** that are created for you.
         You'll need to use these for the `pyramid_googleauth.google_client_id`
         and `pyramid_googleauth.google_client_secret` settings in your app.

### 2. Add pyramid-googleauth to your Pyramid app

1. Add [pyramid-googleauth](https://pypi.org/project/pyramid-googleauth/) to
   your app's Python requirements.

2. Add pyramid-googleauth to your app's code:

   Your app needs to set a session factory, a security policy, and a handful of
   pyramid-googleauth settings, before doing `config.include("pyramid-googleauth")`.
   See [the example app](examples/app.py) for a working example to copy from.
