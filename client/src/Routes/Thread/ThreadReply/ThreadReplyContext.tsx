import React from "react"
import { FormContextValues, useForm } from "react-hook-form"

interface IThreadReplyFormValues {
  markup: string
}

interface IThreadReplyContext {
  active: boolean
  form: FormContextValues<IThreadReplyFormValues>
  activate: () => void
}

const ThreadReplyContext = React.createContext<IThreadReplyContext | null>(
  null
)

const ThreadReplyProvider: React.FC = ({ children }) => {
  const [active, setActive] = React.useState(false)
  const activate = () => setActive(true)

  const form = useForm<IThreadReplyFormValues>({
    defaultValues: { markup: "" },
  })

  return (
    <ThreadReplyContext.Provider value={{ active, form, activate }}>
      {children}
    </ThreadReplyContext.Provider>
  )
}

const useThreadReplyContext = () => React.useContext(ThreadReplyContext)

export { ThreadReplyContext, ThreadReplyProvider, useThreadReplyContext }
