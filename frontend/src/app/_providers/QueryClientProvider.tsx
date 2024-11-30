import { ReactNode } from 'react'
import { AxiosError } from 'axios'
import { queryClient } from '@/lib/react-query/queryClient'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Query, QueryClientProvider as TanStackQueryClientProvider } from '@tanstack/react-query'

type QueryClientProviderProps = {
  children: ReactNode
}

export function QueryClientProvider(props: QueryClientProviderProps) {
  const { children } = props

  return (
    <TanStackQueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools
        initialIsOpen={false}
        buttonPosition='bottom-left'
        errorTypes={[
          {
            name: 'Error',
            initializer: errorInitializer(new Error('Error message'))
          },
          {
            name: 'Axios Error',
            initializer: errorInitializer(new AxiosError('Axios error'))
          }
        ]}
      />
    </TanStackQueryClientProvider>
  )
}

function errorInitializer(error: Error) {
  return (query: Query) => {
    query.reset()
    return error
  }
}
