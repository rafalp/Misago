## HTML attributes reference

Like [htmx](https://htmx.org/reference/), Misago includes a set of custom HTML attributes that template authors can use.

- [`mg-confirm`](#mg-confirm)
- [`mg-error`](#mg-error)
- [`mg-if`](#mg-if)
- [`mg-loader`](#mg-loader)
- [`mg-text`](#mg-text)


### `mg-confirm`

A `form` element attribute that displays a confirmation prompt on submit:

```html
<form
    post="..."
    mg-confirm="Are you sure?"
>
    <button>Submit</button>
</form>
```

Use this attribute instead of `hx-confirm` for form submissions that don't use HTMX.


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

`mg-if` supports simple conditional expressions in `template` elements:

```html
<template id="loading-error">
  <div class="loading-error">
    <span class="material-icon" mt-if="status === 403">shield</span>
    <span class="material-icon" mt-if="status !== 403">warning</span>
    <div mt-text="error"></div>
  </div>
</template>
```

If the condition in `mg-if` evaluates to `true`, the element it is applied to will be included in the resulting HTML. If it evaluates to `false`, the element will be removed from the resulting HTML.

Supported syntax:

- Variable names: `variable`, `lorem.ipsum.dolor`
- Integers and floats: `0`, `4`, `5.12`
- Logical operators: `&&`, `||`, `!variable`, `!!variable`
- Comparison operators: `==`, `===`, `!=`, `!==`, `>`, `<`, `>=`, `<=`


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

If you want to replace the contents of `hx-target` with the contents of an error template, set `mg-loader` to a selector:

```html
<div id="htmx-outlet"></div>

<button
  type="button"
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


### `mg-modal`

A replacement for `bs-modal` that uses the htmx `beforeSend` event to open a modal and requires the `mg-modal` extension to work.

It enables additional `mg-modal-*` attributes to enhance modal behavior.

Example:

```html
<button
  type="button"
  hx-get="/some-url/"
  hx-target="#htmx-modal"
  mg-modal="#my-modal"
>
  Open modal
</button>

<div
  id="my-modal"
  class="modal fade"
  aria-hidden="false"
  tabindex="-1"
>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">My modal</h4>
      </div>
      <div id="htmx-modal"></div>
    </div>
  </div>
</div>
```


### `mg-modal-title`

Used together with mg-modal to set a custom modal title. Modal title element is specified by the `mg-modal-title` attribute:

```html
<button
  type="button"
  hx-get="/some-url/"
  hx-target="#htmx-modal"
  mg-modal="#my-modal"
  mg-modal-title="My custom modal!"
>
  Open modal
</button>

<div
  id="my-modal"
  class="modal fade"
  aria-hidden="false"
  tabindex="-1"
>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" mg-modal-title></h4>
      </div>
      <div id="htmx-modal"></div>
    </div>
  </div>
</div>
```


### `mg-text`

`mg-text` populates an element’s `textContent` in `template` elements with the value of a variable:

```html
<template id="loading-error">
  <div class="loading-error">
    <div mt-text="error"></div>
  </div>
</template>
```

It also supports property traversal:

```html
<template id="loading-error">
  <div class="loading-error">
    <div mt-text="error.message"></div>
  </div>
</template>
```

If variable is not set or is `null`, empty string is used instead.
