import React from "react"
import { FormContextValues, useForm } from "react-hook-form"
import * as Yup from "yup"
import { useSettingsContext } from "../../../Context"

interface IThreadReplyFormValues {
  markup: string
}

interface IThreadReplyContext {
  isActive: boolean
  fullscreen: boolean
  minimized: boolean
  mode: string
  form: FormContextValues<IThreadReplyFormValues>
  startReply: () => void
  deactivate: () => void
  setFullscreen: (state: boolean) => void
  setMinimized: (state: boolean) => void
}

const ThreadReplyContext = React.createContext<IThreadReplyContext | null>(
  null
)

interface IThreadReplyProviderProps {
  active?: boolean
  mode?: string
  children: React.ReactNode
}

const ThreadReplyProvider: React.FC<IThreadReplyProviderProps> = (props) => {
  const { postMinLength } = useSettingsContext()
  const [isActive, setActive] = React.useState(props.active || false)
  const [mode, setMode] = React.useState(props.mode || "")
  const [fullscreen, setFullscreen] = React.useState(false)
  const [minimized, setMinimized] = React.useState(false)

  const ThreadReplySchema = Yup.object().shape({
    markup: Yup.string()
      .required("value_error.missing")
      .min(postMinLength, "value_error.any_str.min_length"),
  })

  const form = useForm<IThreadReplyFormValues>({
    defaultValues: { markup: "" },
    validationSchema: ThreadReplySchema,
  })

  const startReply = () => {
    setActive(true)
    setMode("reply")
    setFullscreen(false)
    setMinimized(false)
  }

  const deactivate = () => setActive(false)

  return (
    <ThreadReplyContext.Provider
      value={{
        isActive,
        form,
        fullscreen,
        minimized,
        mode,
        setFullscreen,
        setMinimized,
        startReply,
        deactivate,
      }}
    >
      {props.children}
    </ThreadReplyContext.Provider>
  )
}

const useThreadReplyContext = () => React.useContext(ThreadReplyContext)

export { ThreadReplyContext, ThreadReplyProvider, useThreadReplyContext }
