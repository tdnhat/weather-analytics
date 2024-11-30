import React from 'react'
import DashboardLayoutComp from '@/layouts/DashboardLayoutComp'

function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <DashboardLayoutComp>{children}</DashboardLayoutComp>
}

export default DashboardLayout
