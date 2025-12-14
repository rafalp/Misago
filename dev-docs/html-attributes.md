## HTML attributes reference

Like [htmx](https://htmx.org/reference/), Misago includes a set of custom HTML attributes that template authors can use.

- [`mg-error`](#mg-error)
- [`mg-if`](#mg-if)
- [`mg-loader`](#mg-loader)
- [`mg-text`](#mg-text)


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
  Make request
</button>
```

If you want to replace the contents of `hx-target` with the contents of an error template, set `mg-error` to a selector:

```html
<div id="htmx-outlet"></div>

<button
  type="button"
  hx-ext="mg-loader"
  hx-get="/some-url/"
  hx-target="#htmx-outlet"
  mg-error="false"
>
  Make request
</button>

<template id="htmx-error">
  <div mt-text="error"></div>
</template>
```

In the above example, the contents of the `htmx-error` template will be cloned and inserted into the `htmx-outlet` element when the request fails.

This feature ignores the `hx-swap` option and always behaves as if `hx-swap="innerHTML"` were set.

The template receives two variables in its context:

- `error`: a string with the error message.
- `status`: an integer containing the error status: 0 (couldn’t establish a connection), 400, 403, 408 (timeout), or 500.


### `mg-if`



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
  Make request
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
  Make request
</button>

<template id="htmx-loader">
  <div>Please wait...</div>
</template>
```

In the above example, the contents of the `htmx-loader` template will be cloned and inserted into the `htmx-outlet` element when the request starts.

This feature ignores the `hx-swap` option and always behaves as if `hx-swap="innerHTML"` was set.

If the `mg-loader` extension is not enabled, no loader will be used.
