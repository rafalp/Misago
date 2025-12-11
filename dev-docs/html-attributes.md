## HTML attributes reference

Like [htmx](https://htmx.org/reference/), Misago includes a set of custom HTML attributes that template authors can use.

- [`mg-loader`](#mg-loader)
- [`mg-toasts`](#mg-toasts)


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

With the `mg-loader` htmx extension, you can also use the contents of a `template` element as the loader:

```html
<div id="htmx-outlet"></div>

<button
  type="button"
  hx-ext="mg-loader"
  hx-get="/some-url/"
  hx-target="#htmx-outlet"
  mg-loader="#htmx-loader"
>
  Run request
</button>

<template id="htmx-loader">
    <div>Please wait...</div>
</template>
```

In the above example, the contents of the `htmx-loader` template will be cloned and inserted into the `htmx-outlet` element when the request starts.

This feature ignores the `hx-swap` option and always behaves as if `hx-swap="innerHTML"` was set.

If the `mg-loader` extension is not enabled, no loader will be used.


### `mg-error`

If an htmx request returns an error response, Misago will display it in a toast.

To disable this behavior for a specific element, add `mg-error="false"` to it:

```html
<button
  type="button"
  hx-get="/some-url/"
  hx-target="#htmx-outlet"
  mg-error="false"
>
  Run request
</button>
```