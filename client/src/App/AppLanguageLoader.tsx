import { Catalogs } from "@lingui/core"
import { I18nProvider } from "@lingui/react"
import React from "react"
import RootLoader from "../RootLoader"

interface IAppLanguageLoaderProps {
  children: React.ReactNode
  language: string
}

const AppLanguageLoader: React.FC<IAppLanguageLoaderProps> = ({ children, language }) => {
  const [catalogs, setCatalogs] = React.useState<Catalogs>({})

  React.useEffect(() => {
    import(
      /* webpackMode: "lazy", webpackChunkName: "i18n-[index]" */
      `../locale/${language}/messages`
    ).then(catalog => {
      setCatalogs(c => {
        return { ...c, [language]: catalog.default }
      })
    })
  }, [language])

  if (!catalogs[language]) return <RootLoader />
  return (
    <I18nProvider language={language} catalogs={catalogs}>
      {children}
    </I18nProvider>
  )
}

export default AppLanguageLoader
