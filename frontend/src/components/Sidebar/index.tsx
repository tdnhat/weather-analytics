'use client'

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine } from '@fortawesome/free-solid-svg-icons';

const sidebarItems = [
    { href: '/pattern1', label: 'Raw Data', icon: faChartLine },
    { href: '/analysis', label: 'Analysis Dashboard', icon: faChartLine },
];

function Sidebar() {
    const [isExpanded, setIsExpanded] = useState(true);
    const pathname = usePathname();

    useEffect(() => {
        const handleToggle = (e: CustomEvent) => {
            setIsExpanded(!isExpanded);
        };

        window.addEventListener('toggle-sidebar', handleToggle as EventListener);
        return () => window.removeEventListener('toggle-sidebar', handleToggle as EventListener);
    }, [isExpanded]);

    return (
        <aside className={`
            h-[calc(100vh-var(--ds-header-height))] 
            transition-all duration-200 ease-in-out overflow-hidden
            bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-30 border border-gray-100
            ${isExpanded ? 'w-64' : 'w-16'}
        `}>
            <div className="p-2 space-y-2">
                {sidebarItems.map((item) => (
                    <Link 
                        key={item.href}
                        href={item.href}
                        className={`
                            relative px-3 py-3 flex items-center space-x-4 justify-start rounded-lg group
                            backdrop-filter backdrop-blur-sm bg-opacity-30 
                            ${pathname === item.href 
                                ? 'bg-gradient-to-r from-cyan-400/70 to-cyan-500/70 text-gray-100' 
                                : 'text-cyan-500 hover:bg-white/10'}
                            ${isExpanded ? 'h-12' : 'h-12'}
                        `}
                    >
                        <FontAwesomeIcon icon={item.icon} className="text-lg" />
                        <span className={`
                            font-medium transition-all duration-200
                            ${isExpanded ? 'opacity-100' : 'opacity-0'}
                        `}>
                            {item.label}
                        </span>
                    </Link>
                ))}
            </div>
        </aside>
    );
}

export default Sidebar; 