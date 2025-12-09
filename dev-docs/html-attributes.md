## HTML attributes reference

Like [htmx](https://htmx.org/reference/), Misago includes a set of custom HTML attributes that template authors can use.

- [`mg-loader`](#mg-loader)


### `mg-loader`

Misago displays a thin loading bar at the top of the viewport while an htmx request is running.

To disable this loader for a specific element, add `mg-loader="false"` to it:

```html
<button
  type="button"
  hx-get="/some-url/"
  hx-target="#htmx-outlet"
  mg-loader="false"
>
  Run request
</button>
```