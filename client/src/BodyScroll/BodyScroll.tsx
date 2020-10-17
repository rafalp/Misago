import React from "react"
import { useBodyScrollLockContext } from "../Context"

const BodyScroll: React.FC = () => {
  const { stack } = useBodyScrollLockContext()
  const lock = stack > 0
  const body = React.useMemo(() => window.document.querySelector("body"), [])

  React.useEffect(() => {
    if (body) {
      body.style.overflowY = lock ? "hidden" : "auto"
    }
  }, [body, lock])

  return null
}

export default BodyScroll
