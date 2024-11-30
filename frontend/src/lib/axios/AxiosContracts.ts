import { AxiosHeaders, AxiosResponse } from 'axios'
import { ZodType } from 'zod'
import { AxiosValidationError } from './AxiosValidationError'

export class AxiosContracts {
  static responseContract<Data>(schema: ZodType<Data>) {
    const schemaName = (schema as any).description

    return (response: AxiosResponse<unknown>): AxiosResponse<Data> => {
      const validationResult = schema.safeParse(response.data)

      if (validationResult.error) {
        console.log(`[AxiosContracts-Response] Validation failed for schema: ${schemaName}`)
        console.log('[AxiosContracts-Response] Invalid data:', response.data)
        console.log('[AxiosContracts-Response] Validation errors:', validationResult.error.errors)

        throw new AxiosValidationError(
          response.config,
          response.request,
          response,
          validationResult.error.errors
        )
      }

      return { ...response, data: validationResult.data }
    }
  }

  static requestContract<Data>(schema: ZodType<Data>, data: unknown ) {
    const validationResult = schema.safeParse(data)
    const schemaName = (schema as any).description

    if (validationResult.error) {
      console.log(`[AxiosContracts-Request] Validation failed for schema: ${schemaName}`)
      console.log('[AxiosContracts-Request] Invalid data:', data)
      console.log('[AxiosContracts-Request] Validation errors:', validationResult.error.errors)

      throw new AxiosValidationError(
        { headers: new AxiosHeaders() },
        undefined,
        undefined,
        validationResult.error.errors
      )
    }

    return validationResult.data
  }
}