# Misago Parser AST Reference

This document contains a reference to all standard abstract syntax tree elements used to represent a parsed markup.

Plugins may modify standard AST as well as add their own AST elements.


## Heading (ATX)

```markdown
# Hello world
```

```json
{
    "type": "heading",
    "level": 1,
    "children": [
        {"type": "text", "text": "Hello world"}
    ]
}
```


## Heading (Setex)

```markdown
Hello world
===========
```

```json
{
    "type": "heading-setex",
    "level": 1,
    "children": [
        {"type": "text", "text": "Hello world"}
    ]
}
```


## List (unordered)

```markdown
- Lorem
- Ipsum
  - Dolor
```

```json
{
    "type": "list",
    "ordered": false,
    "sign": "-",
    "items": [
        {
            "type": "list-item",
            "children": [
                {"type": "text", "text": "Lorem"}
            ],
            "lists": []
        },
        {
            "type": "list-item",
            "children": [
                {"type": "text", "text": "Ipsum"}
            ],
            "lists": [
                {
                    "type": "list",
                    "ordered": false,
                    "sign": "-",
                    "items": [
                        {
                            "type": "list-item",
                            "children": [
                                {"type": "text", "text": "Dolor"}
                            ],
                            "lists": []
                        }
                    ]
                }
            ]
        }
    ]
}
```


## List (ordered)

```markdown
1. Lorem
2. Ipsum
  1. Dolor
```

```json
{
    "type": "list",
    "ordered": true,
    "sign": null,
    "items": [
        {
            "type": "list-item",
            "children": [
                {"type": "text", "text": "Lorem"}
            ],
            "lists": []
        },
        {
            "type": "list-item",
            "children": [
                {"type": "text", "text": "Ipsum"}
            ],
            "lists": [
                {
                    "type": "list",
                    "ordered": true,
                    "sign": null,
                    "items": [
                        {
                            "type": "list-item",
                            "children": [
                                {"type": "text", "text": "Dolor"}
                            ],
                            "lists": []
                        }
                    ]
                }
            ]
        }
    ]
}
```


## Code

    ```
    alert("print")
    ```

```json
{
    "type": "code",
    "syntax": null,
    "code": "alert(\"print\")"
}
```


## Code with syntax

    ```javascript
    alert("print")
    ```

```json
{
    "type": "code",
    "syntax": "javascript",
    "code": "alert(\"print\")"
}
```


## Code (BBCode)

```
[code]alert("print")[/code]
```

```json
{
    "type": "code-bbcode",
    "syntax": null,
    "code": "alert(\"print\")"
}
```


## Code with syntax (BBCode)

```markdown
[code=javascript]alert("print")[/code]
```

```json
{
    "type": "code-bbcode",
    "syntax": "javascript",
    "code": "alert(\"print\")"
}
```


## Code (indented)

```markdown
    alert("print")
```

```json
{
    "type": "code-indented",
    "code": "alert(\"print\")"
}
```


## Code (inlined)

```markdown
`alert("print")`
```

```json
{
    "type": "code-inline",
    "code": "alert(\"print\")"
}
```


## Quote

```markdown
> Hello world!
```

```json
{
    "type": "quote",
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Quote (BBCode)

```markdown
[quote]Hello world![/quote]
```

```json
{
    "type": "quote-bbcode",
    "author": null,
    "post": null,
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Quote with author (BBCode)

```markdown
[quote=Author]Hello world![/quote]
```

```json
{
    "type": "quote-bbcode",
    "author": "Author",
    "post": null,
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Quote with author and post (BBCode)

```markdown
[quote=Author;post=123]Hello world![/quote]
```

```json
{
    "type": "quote-bbcode",
    "author": "Author",
    "post": 123,
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Spoiler (BBCode)

```markdown
[spoiler]Hello world![/spoiler]
```

```json
{
    "type": "spoiler-bbcode",
    "summary": null,
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Spoiler with summary (BBCode)

```markdown
[spoiler=Very secret stuff]Hello world![/spoiler]
```

```json
{
    "type": "spoiler-bbcode",
    "summary": "Very secret stuff",
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Paragraph

```markdown
Hello world!
```

```json
{
    "type": "paragraph",
    "children": [
        {"type": "text", "text": "Hello world!"}
    ]
}
```


## Emphasis

```markdown
*Text*
```

```json
{
    "type": "emphasis",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Emphasis (underscore)

```markdown
_Text_
```

```json
{
    "type": "emphasis-underscore",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Strong

```markdown
**Text**
```

```json
{
    "type": "strong",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Strong (underscore)

```markdown
__Text__
```

```json
{
    "type": "strong-underscore",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Strikethrough

```markdown
~~Text~~
```

```json
{
    "type": "strikethrough",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Strikethrough (BBCode)

```markdown
[s]Text[/s]
```

```json
{
    "type": "strikethrough-bbcode",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Bold (BBCode)

```markdown
[b]Text[/b]
```

```json
{
    "type": "bold-bbcode",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Italics (BBCode)

```markdown
[i]Text[/i]
```

```json
{
    "type": "italics-bbcode",
    "children": [
        {"type": "text", "text": "Text"}
    ]
}
```


## Underline (BBCode)

```markdown
[u]Text[/u]
```

```json
{
    "type": "underline-bbcode",
    "children": [
        {"type": "text", "text": "Text"}
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