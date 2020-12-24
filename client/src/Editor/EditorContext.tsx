import React from "react"
import replaceSelection from "./replaceSelection"

export interface EditorContextData {
  disabled: boolean
  textarea: HTMLTextAreaElement | null
  getSelection: () => string
  getValue: () => string
  replaceSelection: (options: ReplaceSelectionOptions) => void
}

export const EditorContext = React.createContext<EditorContextData>({
  disabled: true,
  textarea: null,
  getSelection: () => "",
  getValue: () => "",
  replaceSelection: (options: ReplaceSelectionOptions) => {},
})

interface ReplaceSelectionOptions {
  replace?: string
  default?: string
  prefix?: string
  suffix?: string
  trim?: boolean
  lstrip?: RegExp
  rstrip?: RegExp
}

interface EditorContextProviderProps {
  disabled: boolean
  textarea: HTMLTextAreaElement | null
  children: React.ReactNode
  setValue: (value: string) => void
}

export const EditorContextProvider: React.FC<EditorContextProviderProps> = ({
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
    (options: ReplaceSelectionOptions) => {
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
