import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getCssVariableValue (variableName: string) {
  const root = document.documentElement
  const variableValue = getComputedStyle(root).getPropertyValue(variableName)
  return variableValue.trim()
}