/// <reference types="vitest/globals" />
/// <reference types="@testing-library/jest-dom" />

import type { TestingLibraryMatchers } from '@testing-library/jest-dom/matchers'
import type { vi } from 'vitest'

declare global {
  // Vitest globals
  const describe: typeof import('vitest').describe
  const test: typeof import('vitest').test
  const it: typeof import('vitest').it
  const expect: typeof import('vitest').expect
  const beforeEach: typeof import('vitest').beforeEach
  const afterEach: typeof import('vitest').afterEach
  const beforeAll: typeof import('vitest').beforeAll
  const afterAll: typeof import('vitest').afterAll
  const vi: typeof import('vitest').vi

  namespace jest {
    interface Matchers<R = void> extends TestingLibraryMatchers<typeof expect.stringContaining, R> {}
  }
}
