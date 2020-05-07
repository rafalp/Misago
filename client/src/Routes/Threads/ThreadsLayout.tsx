import React from "react"
import {
  CategoriesNav,
  Layout,
  LayoutMain,
  LayoutSide,
  RouteContainer,
} from "../../UI"
import { IActiveCategory } from "./Threads.types"
import { ThreadsCategoriesModalButton } from "./ThreadsCategoriesModal"

interface IThreadsLayoutProps {
  activeCategory?: IActiveCategory | null
  className?: string
  children: React.ReactNode
}

const ThreadsLayout: React.FC<IThreadsLayoutProps> = ({
  activeCategory,
  className,
  children,
}) => (
  <RouteContainer className={className}>
    <Layout>
      <LayoutSide>
        <CategoriesNav active={activeCategory} />
      </LayoutSide>
      <LayoutMain>
        <ThreadsCategoriesModalButton active={activeCategory} />
        {children}
      </LayoutMain>
    </Layout>
  </RouteContainer>
)

export default ThreadsLayout
