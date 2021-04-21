# pyramid-googleauth

An example library

Usage
-----

Provides a pyramid security policy and the necessary views to complete google's oauth flow.


## Settings


Secret and google's configuration:

`pyramid_googleauth.secret` 
`pyramid_googleauth.google_client_id`
`pyramid_googleauth.google_client_secret`

Where to redirect after a successful login:

`pyramid_googleauth.login_success_redirect_url`


The extension provides several routes, their locations are configurable with these settings:

`pyramid_googleauth.login_route` Defaults to /ui/api/login
`pyramid_googleauth.login_callback_route` Defaults to /ui/api/login_callback
`pyramid_googleauth.logout_route` Defaults to /ui/api/logout

`pyramid_googleauth.login_failure_route` Defaults to /ui/api/login_failure


## Installation

- Include the package in your project's dependencies

- Set the necessary settings

- Include the extension in your pyramid app

```config.include("pyramid_googleauth")```


- Create your own security policy based on `GoogleSecurityPolicy` overriding `identity` and `permits`. Use your own permissions and identity structure.


```
class CheckmateGoogleSecurityPolicy(GoogleSecurityPolicy):
    def identity(self, request):
        userid = self.authenticated_userid(request)

        if userid and userid.endswith("@hypothes.is"):
            return Identity(
                userid, permissions=[Permissions.ADMIN, Permissions.ADD_TO_ALLOW_LIST]
            )

        return Identity("", [])

    def permits(self, request, context, permission):
        return _permits(self, request, context, permission)
```


- Set your new policy in pyramid

`config.set_security_policy(SecurityPolicy())`



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
cd h-pyramid-google-oauth
```

#### Run the tests

```terminal
make test
```

**That's it!** You’ve finished setting up your h-pyramid-google-oauth
development environment. Run `make help` to see all the commands that're
available for linting, code formatting, packaging, etc.

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
