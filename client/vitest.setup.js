import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { HttpResponse, http } from 'msw'

let count = 0;

export const restHandlers = [
  http.get('/api/count', () => {
    return HttpResponse.json({count})
  }),
  http.post('/api/count/increment', () => {
    console.log(count)
    return HttpResponse.json({count: ++count})
  }),
]

const server = setupServer(...restHandlers)

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))

afterEach(() => {
  server.resetHandlers()
  cleanup()
})

afterAll(() => server.close())