Social authentication
=====================

Misago can be configured to allow your users to join or sign in to your site using already-existing account in other service.

This feature is implemented using the [Python Social Auth](http://python-social-auth.readthedocs.io/en/latest/) library, so you should check it out to see which authentication providers are supported, how to customize social authentication in Misago or develop your own integration for your site.

In this guide we will only focus on providing example for making your Misago site allow users to join with GitHub as well as showing few additional configuration options that make process faster or more secure.


## Sign in with GitHub


### Configure your site on GitHub

Great majority of authentication providers require you to register your site as an "app" using their developer settings page.

Start by going to [Developer settings](https://github.com/settings/developers) page, and make sure you are in the "OAuth Apps" section. If you don't any apps yet, it will look like this:

![OAuth Apps](./images/SocialAuth/github_step_1.png)

Click the "Register a new application" button. This will move you to page where you will have to fill in details for your app:

![GitHub App Create](./images/SocialAuth/github_step_2.png)

Fill in following data:

**Application name** - this the name that will be displayed to users when GitHub will ask them if they want to share their account's data with your site.
**Homepage URL** - Url to your site's homepage.
**Authorization callback URL** - This is where GitHub will send user's data to after they confirm that they want to sign on your site. Unless you've customized your ``Python Social Auth`` links, entering same url as in "Homepage URL" will work.

Now click "Register application".


#### Note:

Different providers have different requirements for 3rd party apps. For example, Facebook Login requires app authors to meet following requirements to create app in Facebook for developers:

- Site is reachable from internet and uses ``https``
- You need to provide link to Privacy Policy used by your site
- Your callback URL needs to be explicit and contain `/complete/facebook/` in it to pass validation

To get start with GitHub, you don't have to meet any of those requirements. In fact, you can use `http://127.0.0.1:8000/` as callback URL and it will allow you to log in to Misago running on your computer, which makes it great for testing things out on your own.


### Client ID and secret

You should be redirected to page displaying your application name and settings:

![GitHub App Settings](./images/SocialAuth/github_step_3.png)

You can return to this page any time by going to your [Developer settings](https://github.com/settings/developers) and clicking it on list of apps.

There are quite a few options here, but we are only interested in two:

- Client ID
- Client Secret

Those are the values that you will need to enter in your Misago ``settings.py`` in next step. It is **critical** that you don't make those values public and that you will not run Misago with ``DEBUG = True`` after you setup GitHub authentication because just going to non-existing page like `https://yoursite.com/dsjahkdhsajkh` will make Misago display its running settings and leak your Client ID and Secret, forcing you to generate new ones using "Reset client secret". If you don't do this, anybody will easily be able to pretend they are user coming from GitHub to join your site.


### Enabling GitHub authentication on Misago

Now open your Misago ``settings.py`` in code editor and find the ``AUTHENTICATION_BACKENDS`` setting. By default it looks like this:

```python
AUTHENTICATION_BACKENDS = [
    'misago.users.authbackends.MisagoBackend',
]
```

You will need to module that will handle GitHub authentication to this list. Go to [list of backends implemented by Python Social Auth](http://python-social-auth.readthedocs.io/en/latest/backends/index.html) and find "GitHub" on it:

![GitHub App Settings](./images/SocialAuth/github_step_4.png)

This is suprising. Looks like there is not one but 7 GitHub backends available. Click the first one, named siply "GitHub", and this will take you to [documentation](http://python-social-auth.readthedocs.io/en/latest/backends/github.html) explaining how to add GitHub auth in your site:

![GitHub Backend Settings](./images/SocialAuth/github_step_5.png)

As it says, you should add ``'social_core.backends.github.GithubOAuth2',`` to your ``AUTHENTICATION_BACKENDS``:

```python
AUTHENTICATION_BACKENDS = [
    'misago.users.authbackends.MisagoBackend',
    'social_core.backends.github.GithubOAuth2',
]
```

And you should add ``SOCIAL_AUTH_GITHUB_KEY`` and ``SOCIAL_AUTH_GITHUB_SECRET`` at end of your ``settings.py`` using Client ID and Secret that GitHub has given you ealier:

```python
# GitHub OAuth

SOCIAL_AUTH_GITHUB_KEY = '53b098f7d772fc196389'
SOCIAL_AUTH_GITHUB_SECRET = 'cddceb4164d897485e76d69751e9e20eb50114c3'
```

Lastly, we would like to tell GitHub to pass user email and profile details when user signs in, so add one more line to your settings:

```python
# GitHub OAuth

SOCIAL_AUTH_GITHUB_KEY = '53b098f7d772fc196389'
SOCIAL_AUTH_GITHUB_SECRET = 'cddceb4164d897485e76d69751e9e20eb50114c3'
SOCIAL_AUTH_GITHUB_SCOPE = ['read:user', 'user:email']
```

GitHub verifies that user email address is correct before passing it to other application. We can use this fact to tell Misago that if email returned by GitHub already exists in Misago database, user should be signed in to this account instead of being asked to enter new e-mail. Find your ``SOCIAL_AUTH_PIPELINE``, inside of it you will find line like this:

```python
SOCIAL_AUTH_PIPELINE = (
    # ...some other lines

    # Uncomment next line to let your users to associate their old forum account with social one.
    # 'misago.users.social.pipeline.associate_by_email',

    # ...some other lines
)
```

Like comment says, remove the ``#`` sign from before the ``'misago.users.social.pipeline.associate_by_email',`` so it looks like this:

```python
SOCIAL_AUTH_PIPELINE = (
    # ...some other lines

    # Uncomment next line to let your users to associate their old forum account with social one.
    'misago.users.social.pipeline.associate_by_email',

    # ...some other lines
)
```

Now you are finished. Save your changes and restart your Misago to reload settings. "Sign in with GitHub" button will now appear on your login and registration forms.