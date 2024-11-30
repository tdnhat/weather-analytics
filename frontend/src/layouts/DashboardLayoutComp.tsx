import React from 'react'
import Header from './shared/Header'
import Sidebar from './shared/Sidebar'

function DashboardLayoutComp({ children }: { children: React.ReactNode }) {
  return (
    <div className='size-full'>
      <Header />
      <main className='flex w-full h-[calc(100vh-var(--ds-header-height))]'>
        <Sidebar />
        <section className='flex-1 overflow-y-scroll max-h-full'>{children}</section>
      </main>
    </div>
  )
}

export default DashboardLayoutComp
