'use client'

import { QueryClientProvider } from '@/app/_providers/QueryClientProvider'

export default function RootLayoutComp({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return <QueryClientProvider>{children}</QueryClientProvider>
}
