import React from "react"
import { RouteError } from "../RouteError"

interface IRouteErrorBoundaryProps {
  children: React.ReactNode
}

class RouteErrorBoundary extends React.Component<IRouteErrorBoundaryProps> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) return <RouteError />
    return this.props.children
  }
}

export default RouteErrorBoundary
