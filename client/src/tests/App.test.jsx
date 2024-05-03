import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest';
import App from '../App';

describe('Home Screen', () => {
  it('should render the home screen', () => {
    render(<App/>)

    const heading = screen.getByRole('heading')
    expect(heading).toBeInTheDocument()
  })

  it('should have a working counter', async () => {
    render(<App/>)

    const button = screen.getByRole('button')
    const count = screen.getByText(/count is 0/i)

    expect(count).toBeInTheDocument()

    button.click()

    expect(await screen.findByText(/count is 1/i)).toBeInTheDocument()
  })
})