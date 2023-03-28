import React from "react"
import ReactDOM from "react-dom"
import { Provider } from "react-redux"
import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom"
import store from "misago/services/store"

const rootElement = document.getElementById("page-mount")

export default function mountRoutedComponent(options) {
  let routes = []
  if (options.basepath) {
    routes.push(
      {
        path: options.basepath,
        element: <Navigate to={options.paths[0].path} />
      }
    )
  }
  
  options.paths.map(( route ) => routes.push(route))
  
  const { Component } = options
  const router = createBrowserRouter(routes)

  ReactDOM.render(
    <Provider store={store.getStore()}>
      {Component ? (
        <Component>
          <RouterProvider router={router}  />
        </Component>
      ) : (
        <RouterProvider router={router}  />
      )}
    </Provider>,
    rootElement
  )
}
