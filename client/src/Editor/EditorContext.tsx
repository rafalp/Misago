import React from "react"
import replaceSelection from "./replaceSelection"

export interface IEditorContextValues {
  disabled: boolean
  textarea: HTMLTextAreaElement | null
  getSelection: () => string
  getValue: () => string
  replaceSelection: (options: IReplaceSelectionOptions) => void
}

export const EditorContext = React.createContext<IEditorContextValues>({
  disabled: true,
  textarea: null,
  getSelection: () => "",
  getValue: () => "",
  replaceSelection: (options: IReplaceSelectionOptions) => {},
})

interface IReplaceSelectionOptions {
  replace?: string
  prefix?: string
  suffix?: string
}

interface IEditorContextProviderProps {
  disabled: boolean
  textarea: HTMLTextAreaElement | null
  children: React.ReactNode
  setValue: (value: string) => void
}

export const EditorContextProvider: React.FC<IEditorContextProviderProps> = ({
  children,
  disabled,
  textarea,
  setValue,
}) => {
  const getSelection = React.useCallback(() => {
    if (!textarea) return ""

    return ""
  }, [textarea])

  const getValue = React.useCallback(() => {
    if (!textarea) return ""

    return textarea.value
  }, [textarea])

  const replaceSelectionMemo = React.useCallback(
    (options: IReplaceSelectionOptions) => {
      if (!textarea) return

      const { selection, value } = replaceSelection({ textarea, ...options })
      setValue(value)
      textarea.focus()
      textarea.setSelectionRange(selection.start, selection.end)
    },
    [textarea, setValue]
  )

  const value = React.useMemo(() => {
    return {
      textarea,
      getSelection,
      getValue,
      disabled: textarea ? disabled : false,
      replaceSelection: replaceSelectionMemo,
    }
  }, [textarea, disabled, getSelection, getValue, replaceSelectionMemo])

  return (
    <EditorContext.Provider value={value}>{children}</EditorContext.Provider>
  )
}
