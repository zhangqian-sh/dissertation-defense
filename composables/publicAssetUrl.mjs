// Public asset paths stay independent of the deployment directory in source data.
export function publicAssetUrl(path, base = import.meta.env?.BASE_URL ?? '/') {
  if (!base.startsWith('/') || base.startsWith('//') || !base.endsWith('/'))
    throw new Error('Invalid public base path')
  if (/^(?:[a-z][\w+.-]*:|\/\/)/i.test(path))
    throw new Error('Nonlocal public asset URL')
  const root = new URL(base, 'https://local.invalid')
  const url = new URL(path.replace(/^\/+/, ''), root)
  if (url.origin !== root.origin || !url.pathname.startsWith(root.pathname))
    throw new Error('Public asset path escapes deployment directory')
  return url.pathname + url.search + url.hash
}
