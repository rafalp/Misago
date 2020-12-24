import React from "react"
import { useBodyScrollLockContext } from "../Context"

interface BodyScrollLockProps {
  locked?: boolean
}

const BodyScrollLock: React.FC<BodyScrollLockProps> = ({ locked }) => {
  const { increaseStack, decreaseStack } = useBodyScrollLockContext()
  React.useEffect(() => {
    if (locked) {
      increaseStack()
      return () => decreaseStack()
    }
  }, [locked, increaseStack, decreaseStack])

  return null
}

export default BodyScrollLock
