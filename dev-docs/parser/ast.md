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


## Superscript (BBCode)

```markdown
[sup]Text[/sup]
```

```json
{
    "type": "superscript-bbcode",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Subscript (BBCode)

```markdown
[sub]Text[/sub]
```

```json
{
    "type": "subscript-bbcode",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Thematic break

```markdown
- - -
```

```json
{"type": "thematic-break"}
```


## Thematic break (BBCode)

```markdown
[hr]
```

```json
{"type": "thematic-break-bbcode"}
```


## Image

```markdown
!(https://misago-project.org/logo.png)
```

```json
{
    "type": "image",
    "src": "https://misago-project.org/logo.png",
    "alt": null
}
```


## Image with alt text

```markdown
![Misago Forums](https://misago-project.org/logo.png)
```

```json
{
    "type": "url",
    "src": "https://misago-project.org/logo.png",
    "alt": "Misago Forums"
}
```


## Image (BBCode)

```markdown
[img]https://misago-project.org/logo.png[/img]
```

```json
{
    "type": "img-bbcode",
    "src": "https://misago-project.org/logo.png",
    "alt": null
}
```


## Image (BBCode with alt text)

```markdown
[url=https://misago-project.org/logo.png]Misago forums[/url]
```

```json
{
    "type": "img-bbcode",
    "src": "https://misago-project.org/logo.png",
    "alt": "Misago Forums"
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


## Escaped special character

```markdown
\*
```

```json
{
    "type": "escape",
    "character": "*"
}
```


## Line break

```markdown
\n
```

```json
{"type": "line-break"}
```


## Text

```markdown
Hello world!
```

```json
{"type": "text", "text": "Hello world"}
```