import React from "react"
import {
  CategoriesNav,
  Layout,
  LayoutMain,
  LayoutSide,
  RouteContainer,
} from "../../UI"
import { MobileCategoryNavButton } from "./MobileCategoryNav"
import { IActiveCategory } from "./Threads.types"

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
        <MobileCategoryNavButton active={activeCategory} />
        {children}
      </LayoutMain>
    </Layout>
  </RouteContainer>
)

export default ThreadsLayout
