<a href="https://github.com/hypothesis/pyramid-googleauth/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/hypothesis/pyramid-googleauth/CI/main"></a>
<a href="https://pypi.org/project/pyramid-googleauth"><img src="https://img.shields.io/pypi/v/pyramid-googleauth"></a>
<a><img src="https://img.shields.io/badge/python-3.9 | 3.8-success"></a>
<a href="https://github.com/hypothesis/pyramid-googleauth/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# pyramid-googleauth

'Sign in with Google' for Pyramid.

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

## Setting up Your pyramid-googleauth Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/pyramid-googleauth.git
cd pyramid_googleauth
make help
```

## Releasing a New Version of the Project

1. First, to get PyPI publishing working you need to go to:
   <https://github.com/organizations/hypothesis/settings/secrets/actions/PYPI_TOKEN>
   and add pyramid-googleauth to the `PYPI_TOKEN` secret's selected
   repositories.

2. Now that the pyramid-googleauth project has access to the `PYPI_TOKEN` secret
   you can release a new version by just [creating a new GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
   Publishing a new GitHub release will automatically trigger
   [a GitHub Actions workflow](.github/workflows/pypi.yml)
   that will build the new version of your Python package and upload it to
   <https://pypi.org/project/pyramid-googleauth>.

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request
