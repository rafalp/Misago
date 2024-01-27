# Misago Parser AST Reference


## Paragraph

```markdown
Hello world!
```

```json
{
    "type": "paragraph",
    "children": [
        {"type": "text", "text": "Hello world"}
    ]
}
```


## URL

```markdown
[Misago Forums](https://misago-project.org)
```

```json
{
    "type": "url",
    "href": "https://misago-project.org",
    "children": [
        {"type": "text", "text": "Misago forums"}
    ]
}
```


## URL (BBCode)

```markdown
[url]https://misago-project.org[/url]
```

```json
{
    "type": "url-bbcode",
    "href": "https://misago-project.org",
    "children": []
}
```


## URL (BBCode with text)

```markdown
[url=https://misago-project.org]Misago forums[/url]
```

```json
{
    "type": "url-bbcode",
    "href": "https://misago-project.org",
    "children": [
        {"type": "text", "text": "Misago forums"}
    ]
}
```


## Autolink

```markdown
<https://misago-project.org>
```

```json
{
    "type": "auto-link",
    "image": false,
    "href": "https://misago-project.org"
}
```


## Autolink (image)

```markdown
<!https://misago-project.org/logo.png>
```

```json
{
    "type": "auto-link",
    "image": true,
    "href": "https://misago-project.org/logo.png"
}
```


## Autourl

```markdown
https://misago-project.org/logo.png
```

```json
{
    "type": "auto-url",
    "href": "https://misago-project.org/logo.png"
}
```


## Mention

```markdown
@JohnDoe
```

```json
{
    "type": "mention",
    "username": "JohnDoe"
}
```

`username` value represents username as it was entered in the mention. It needs to be normalized before processing further (eg. with `misago.core.utils.slugify`).


## Text

```markdown
Hello world!
```

```json
{"type": "text", "text": "Hello world"}
```