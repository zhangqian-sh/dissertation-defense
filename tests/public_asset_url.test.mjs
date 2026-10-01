import test from 'node:test'
import assert from 'node:assert/strict'
import { publicAssetUrl } from '../composables/publicAssetUrl.mjs'

test('public paths resolve under root and project deployments', () => {
  for (const path of ['/data/manifest.json', '/data/ch06/time/jet-000.png', '/fallback_figures/ch02/sms_longtime_rollout.png']) {
    assert.equal(publicAssetUrl(path, '/'), path)
    assert.equal(publicAssetUrl(path, '/dissertation-defense/'), '/dissertation-defense' + path)
  }
  assert.equal(publicAssetUrl('data/manifest.json', '/dissertation-defense/'), '/dissertation-defense/data/manifest.json')
})

test('asset paths cannot switch hosts or escape the project directory', () => {
  for (const path of ['https://example.com/data.json', '//example.com/data.json', '../data.json', '/%2e%2e/data.json'])
    assert.throws(() => publicAssetUrl(path, '/dissertation-defense/'))
})
