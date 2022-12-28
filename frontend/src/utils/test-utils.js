import React from "react"
import ReactDOM from "react-dom"
import ReactTestUtils from "react-addons-test-utils"

// clean test mounts from components
export function render(containerOrComponent, Component) {
  if (Component) {
    return ReactDOM.render(
      Component,
      document.getElementById(containerOrComponent + "-mount")
    )
  } else {
    return ReactDOM.render(
      containerOrComponent,
      document.getElementById("test-mount")
    )
  }
}

export function unmountComponents() {
  ReactDOM.unmountComponentAtNode(document.getElementById("dropdown-mount"))
  ReactDOM.unmountComponentAtNode(document.getElementById("modal-mount"))
  ReactDOM.unmountComponentAtNode(document.getElementById("page-mount"))
  ReactDOM.unmountComponentAtNode(document.getElementById("test-mount"))
}

// global utility for mocking context
export function contextClear(misago) {
  misago._context = {}
}

export function mockUser(overrides) {
  let user = {
    id: 42,
    absolute_url: "/user/loremipsum-42/",
    api_url: {
      avatar: "/test-api/users/42/avatar/",
      change_email: "/test-api/users/42/change-email/",
      change_password: "/test-api/users/42/change-password/",
      options: "/test-api/users/42/forum-options/",
      username: "/test-api/users/42/username/",
    },
    avatar_hash: "5c6a04b4",
    email: "test@example.com",
    is_hiding_presence: false,
    joined_on: "2015-05-09T16:13:33.973603Z",
    limits_private_thread_invites_to: 0,
    new_notifications: 0,
    posts: 30,
    rank: {
      id: 1,

      css_class: "team",
      description:
        '<p>Lorem ipsum dolor met sit amet elit, si vis pacem para bellum.</p>\n<p>To help see <a href="http://wololo.com/something.php?page=2131">http://wololo.com/something.php?page=2131</a></p>',
      is_tab: true,
      name: "Forum team",
      slug: "forum-team",
      title: "Team",
    },
    slug: "loremipsum",
    subscribe_to_replied_threads: 2,
    subscribe_to_started_threads: 1,
    threads: 0,
    title: "",
    unread_private_threads: 0,
    username: "LoremIpsum",

    status: null,

    acl: {},
  }

  if (overrides) {
    return Object.assign(user, overrides)
  } else {
    return user
  }
}

export function contextGuest(misago) {
  misago._context = Object.assign({}, misago._context, {
    isAuthenticated: false,

    user: {
      id: null,

      acl: {},
    },
  })
}

export function contextAuthenticated(misago, overrides) {
  misago._context = Object.assign({}, misago._context, {
    isAuthenticated: true,

    user: mockUser(overrides),
  })
}

// global utility function for store mocking
export function initEmptyStore(store) {
  store.constructor()
  store.addReducer(
    "tick",
    function (state = {}, action = null) {
      return {}
    },
    {}
  )
  store.init()
}

export function snackbarStoreMock() {
  return {
    message: null,
    _callback: null,

    callback: function (callback) {
      this._callback = callback
    },

    dispatch: function (action) {
      if (action.type === "SHOW_SNACKBAR") {
        this.message = {
          message: action.message,
          type: action.messageType,
        }

        if (this._callback) {
          window.setTimeout(() => {
            this._callback(this.message)
          }, 100)
        }
      }
    },
  }
}

// global init function for modal and dropdown services
export function initModal(modal) {
  $("#modal-mount").off()
  modal.init(document.getElementById("modal-mount"))
}

export function initDropdown(dropdown) {
  dropdown.init(document.getElementById("dropdown-mount"))
}

// global util for reseting snackbar
export function snackbarClear(snackbar) {
  // NOTE: Never ever cause situation when snackbar is triggered more than once
  // in the single test, because this results in race condition within tests
  // suite where one tests check's snackbar state before it has reopened with
  // new message set by current test
  if (snackbar._timeout) {
    window.clearTimeout(snackbar._timeout)
    snackbar._timeout = null
  }
}

// global util functions for events
export function simulateClick(selector) {
  if ($(selector).length) {
    ReactTestUtils.Simulate.click($(selector).get(0))
  } else {
    throw 'selector "' + selector + '" did not match anything'
  }
}

export function simulateSubmit(selector) {
  if ($(selector).length) {
    ReactTestUtils.Simulate.submit($(selector).get(0))
  } else {
    throw 'selector "' + selector + '" did not match anything'
  }
}

export function simulateChange(selector, value) {
  if ($(selector).length) {
    $(selector).val(value)
    ReactTestUtils.Simulate.change($(selector).get(0))
  } else {
    throw 'selector "' + selector + '" did not match anything'
  }
}

export function afterAjax(callback) {
  window.setTimeout(function () {
    callback()
  }, 200)
}

export function onElement(selector, callback) {
  let _getElement = function () {
    window.setTimeout(function () {
      let element = $(selector)
      if (element.length >= 1) {
        callback(element)
      } else {
        _getElement()
      }
    }, 50)
  }

  _getElement()
}
