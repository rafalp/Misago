import React from "react"
import { useBodyScrollLockContext } from "../Context"

interface IBodyScrollLockProps {
  locked?: boolean
}

const BodyScrollLock: React.FC<IBodyScrollLockProps> = ({ locked }) => {
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
