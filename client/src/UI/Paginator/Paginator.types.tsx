export interface IPaginatorProps {
  page?: {
    number: number
    pagination: {
      pages: number
    }
  } | null
  url: (page: number) => string
}
