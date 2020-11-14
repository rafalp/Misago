import { yupResolver } from "@hookform/resolvers/yup"
import { t } from "@lingui/macro"
import React from "react"
import { UseFormMethods, useForm } from "react-hook-form"
import * as Yup from "yup"
import { useSettingsContext } from "../../../Context"

interface IThreadReplyFormValues {
  markup: string
}

interface IThreadReplyPost {
  id: string
}

export interface IThreadReplyContext {
  isActive: boolean
  fullscreen: boolean
  minimized: boolean
  mode: string
  post: IThreadReplyPost | null
  form: UseFormMethods<IThreadReplyFormValues>
  startReply: () => void
  editReply: (post: IThreadReplyPost) => void
  cancelReply: (force?: boolean) => void
  setFullscreen: (state: boolean) => void
  setMinimized: (state: boolean) => void
  getValue: () => string
  setValue: (value: string, dirty?: boolean) => void
  resetValue: (value?: string) => void
}

const ThreadReplyContext = React.createContext<IThreadReplyContext | null>(
  null
)

interface IThreadReplyProviderProps {
  active?: boolean
  mode?: string
  post?: IThreadReplyPost
  children: React.ReactNode
}

const ThreadReplyProvider: React.FC<IThreadReplyProviderProps> = (props) => {
  const { postMinLength } = useSettingsContext()
  const [isActive, setActive] = React.useState(props.active || false)
  const [mode, setMode] = React.useState(props.mode || "")
  const [post, setPost] = React.useState<IThreadReplyPost | null>(
    props.post || null
  )
  const [fullscreen, setFullscreen] = React.useState(false)
  const [minimized, setMinimized] = React.useState(false)

  const validators = Yup.object().shape({
    markup: Yup.string()
      .required("value_error.missing")
      .min(postMinLength, "value_error.any_str.min_length"),
  })

  const form = useForm<IThreadReplyFormValues>({
    defaultValues: { markup: "" },
    resolver: yupResolver(validators),
  })

  const formGetValue = form.getValues
  const getValue = React.useCallback(() => formGetValue("markup") || "", [
    formGetValue,
  ])

  const formSetValue = form.setValue
  const setValue = React.useCallback(
    (value: string) => formSetValue("markup", value),
    [formSetValue]
  )

  const formReset = form.reset
  const resetValue = React.useCallback(
    (value?: string) => {
      formReset({ markup: value || "" }, { submitCount: true })
    },
    [formReset]
  )

  const dirtyFields = form.formState.dirtyFields
  const hasChanges = React.useCallback(() => {
    if (getValue().length === 0) return false
    return !!dirtyFields.markup
  }, [getValue, dirtyFields])

  const startReply = React.useCallback(() => {
    if (isActive && mode === "edit" && hasChanges()) {
      // ask user to confirm mode change
      const confirmed = window.confirm(
        t({
          id: "posting.confirm_cancel_edit_to_reply",
          message:
            "You are currently editing a post. Do you want to abandon your changes and write a new reply instead?",
        })
      )

      if (!confirmed) return
    }

    resetValue()
    setActive(true)
    setMode("reply")
    setPost(null)
    setFullscreen(false)
    setMinimized(false)
  }, [
    isActive,
    mode,
    hasChanges,
    setActive,
    setMode,
    setPost,
    setFullscreen,
    setMinimized,
    resetValue,
  ])

  const editReply = React.useCallback(
    (newPost: IThreadReplyPost) => {
      if (isActive && hasChanges()) {
        if (mode === "reply") {
          const confirmed = window.confirm(
            t({
              id: "posting.confirm_cancel_reply_to_edit",
              message:
                "You are currently writing a new reply. Do you want to abandon it and edit this post instead?",
            })
          )

          if (!confirmed) return
        }

        if (mode === "edit" && post?.id !== newPost.id) {
          const confirmed = window.confirm(
            t({
              id: "posting.confirm_cancel_edit_to_edit",
              message:
                "You are currently editing other post. Do you want to abandon your changes and edit this post instead?",
            })
          )

          if (!confirmed) return
        }
      }

      resetValue()
      setActive(true)
      setMode("edit")
      setPost(newPost)
      setFullscreen(false)
      setMinimized(false)
    },
    [
      isActive,
      mode,
      post,
      hasChanges,
      setActive,
      setMode,
      setPost,
      setFullscreen,
      setMinimized,
      resetValue,
    ]
  )

  const cancelReply = React.useCallback(
    (force?: boolean) => {
      if (!force && isActive && hasChanges()) {
        // ask user to confirm cancel
        const confirmed = window.confirm(
          t({
            id: "posting.confirm_cancel",
            message: "Are you sure you want to abandon your post?",
          })
        )

        if (!confirmed) return
      }

      setActive(false)
      setMode("reply")
      setPost(null)
      resetValue()
    },
    [isActive, hasChanges, setActive, setMode, setPost, resetValue]
  )

  return (
    <ThreadReplyContext.Provider
      value={{
        isActive,
        form,
        fullscreen,
        minimized,
        mode,
        post,
        setFullscreen,
        setMinimized,
        startReply,
        editReply,
        cancelReply,
        getValue,
        setValue,
        resetValue,
      }}
    >
      {props.children}
    </ThreadReplyContext.Provider>
  )
}

const useThreadReplyContext = () => React.useContext(ThreadReplyContext)

export { ThreadReplyContext, ThreadReplyProvider, useThreadReplyContext }
