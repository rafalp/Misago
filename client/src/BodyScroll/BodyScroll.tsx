import React from "react"
import { useBodyScrollLockContext } from "../Context"

const BodyScroll: React.FC = () => {
  const { stack } = useBodyScrollLockContext()
  const lock = stack > 0
  const body = React.useMemo(() => window.document.querySelector("body"), [])

  React.useLayoutEffect(() => {
    if (body && lock) {
      const scroll = document.documentElement.scrollTop
      body.style.overflow = "hidden"
      body.style.position = "fixed"
      body.style.height = "100%"
      document.documentElement.scrollTop = scroll

      return () => {
        body.style.height = "auto"
        body.style.position = "static"
        body.style.overflow = "auto"
        document.documentElement.scrollTop = scroll
      }
    }
  }, [body, lock])

  return null
}

export default BodyScroll
