# pyramid-googleauth

"Sign in with Google" for Pyramid. Provides a Pyramid security policy and views
for Google's OAuth flow.

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

Hacking
-------

### Installing pyramid-googleauth in a development environment

#### You will need

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.
  On Ubuntu follow the Basic GitHub Checkout method.

#### Clone the git repo

```terminal
git clone https://github.com/hypothesis/pyramid-googleauth.git
```

This will download the code into a `pyramid-googleauth` directory
in your current working directory. You need to be in the
`pyramid-googleauth` directory for the rest of the installation
process:

```terminal
cd pyramid-googleauth
```

#### Run the test app

`pyramid-googleauth` comes with a demo Pyramid app that you can use to test the
extension. To run the test app:

1. Set the `PYRAMID_GOOGLEAUTH_CLIENT_ID`, `PYRAMID_GOOGLEAUTH_CLIENT_SECRET`
   and `PYRAMID_GOOGLEAUTH_SECRET` environment variables.

   Hypothesis developers can set these by just running `make devdata`:

   ```terminal
   make devdata
   ```

   <details>
   <summary>If you get a permissions error</summary>

   If you get a permissions error when running `make devdata` then you'll have
   to create your own values and set the environment variables yourself. Follow
   the instructions above to
   [create a Google client ID and secret](#1-create-a-google-client-id-and-secret)
   and use `http://localhost:6547/googleauth/login/callback` for the
   **authorized redirect URI**. Then set the environment variables to the
   client ID and secret that you created:

   ```terminal
   export PYRAMID_GOOGLEAUTH_CLIENT_ID='765...2g6.apps.googleusercontent.com'
   export PYRAMID_GOOGLEAUTH_CLIENT_SECRET='Dfj...Y6i'
   ```

   You also need to set the `PYRAMID_GOOGLEAUTH_SECRET` environment variable
   for creating OAuth 2.0 `state` params. This can be set to any
   securely-generated random string:

   ```terminal
   export PYRAMID_GOOGLEAUTH_SECRET='abc...123'
   ```

   </details>

#### Run the tests

```terminal
make test
```

**That's it!** You’ve finished setting up your pyramid-googleauth development
environment. Run `make help` to see all the commands that're available for
linting, code formatting, packaging, etc.

### Updating the Cookiecutter scaffolding

This project was created from the
https://github.com/hypothesis/h-cookiecutter-pypackage/ template.
If h-cookiecutter-pypackage itself has changed since this project was created, and
you want to update this project with the latest changes, you can "replay" the
cookiecutter over this project. Run:

```terminal
make template
```

**This will change the files in your working tree**, applying the latest
updates from the h-cookiecutter-pypackage template. Inspect and test the
changes, do any fixups that are needed, and then commit them to git and send a
pull request.

If you want `make template` to skip certain files, never changing them, add
these files to `"options.disable_replay"` in
[`.cookiecutter.json`](.cookiecutter.json) and commit that to git.

If you want `make template` to update a file that's listed in `disable_replay`
simply delete that file and then run `make template`, it'll recreate the file
for you.
