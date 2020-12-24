import React from "react"

interface BodyScrollLockContextData {
  stack: number
  increaseStack: () => void
  decreaseStack: () => void
}

const BodyScrollLockContext = React.createContext<BodyScrollLockContextData>({
  stack: 0,
  increaseStack: () => {},
  decreaseStack: () => {},
})

interface BodyScrollLockProviderProps {
  children?: React.ReactNode
}

const BodyScrollLockProvider: React.FC<BodyScrollLockProviderProps> = ({
  children,
}) => {
  const [stack, setStack] = React.useState(0)
  const increaseStack = React.useCallback(
    () => setStack((stack) => stack + 1),
    [setStack]
  )
  const decreaseStack = React.useCallback(
    () => setStack((stack) => (stack > 0 ? stack - 1 : stack)),
    [setStack]
  )

  return (
    <BodyScrollLockContext.Provider
      value={{
        stack,
        increaseStack,
        decreaseStack,
      }}
    >
      {children}
    </BodyScrollLockContext.Provider>
  )
}

const useBodyScrollLockContext = () => React.useContext(BodyScrollLockContext)

export {
  BodyScrollLockContext,
  BodyScrollLockProvider,
  useBodyScrollLockContext,
}
