import React from "react"
import { RouteError } from "../RouteError"

interface RouteErrorBoundaryProps {
  children: React.ReactNode
}

class RouteErrorBoundary extends React.Component<RouteErrorBoundaryProps> {
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
