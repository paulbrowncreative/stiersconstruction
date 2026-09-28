// Run with:  node tests/submission-created.test.js
'use strict';
const assert = require('assert');
const path = require('path');
const { handler } = require(path.join(__dirname, '..', 'netlify', 'functions', 'submission-created.js'));

let calls = [];
function mockFetch(routes) {
  global.fetch = async (url, opts = {}) => {
    calls.push({ url, opts });
    for (const [prefix, fn] of routes) if (String(url).startsWith(prefix)) return fn(url, opts);
    throw new Error('unexpected fetch ' + url);
  };
}
const json = (status, obj) => ({ ok: status < 300, status, json: async () => obj, text: async () => JSON.stringify(obj) });
const evt = (payload) => ({ httpMethod: 'POST', body: JSON.stringify({ payload }) });
const quote = (extra = {}) => ({ id: 'sub1', form_name: 'quote', created_at: '2026-09-21T15:00:00Z', data: { name: 'Pat Smith', phone: '5865550100', email: 'pat@example.com', address: '12 Canal St', service: 'Seawall', message: 'Wall is leaning <script>alert(1)</script>', 'bot-field': '', ...extra } });
const reset = (env = {}) => { calls = []; for (const k of ['RESEND_API_KEY', 'MAIL_FROM', 'MAIL_TO', 'NETLIFY_API_TOKEN']) delete process.env[k]; Object.assign(process.env, env); };
const ENV = { RESEND_API_KEY: 're_test', MAIL_FROM: "Stier's Website <forms@example.com>" };
let n = 0;
async function t(name, fn) { await fn(); n++; console.log('  ok', name); }

(async () => {
  await t('quote form emails kevin@stiers-construction.com with reply-to, subject and escaped HTML', async () => {
    reset(ENV); mockFetch([['https://api.resend.com', () => json(200, { id: 'e1' })]]);
    const r = await handler(evt(quote()));
    assert.strictEqual(r.statusCode, 200); assert.strictEqual(calls.length, 1);
    const b = JSON.parse(calls[0].opts.body);
    assert.deepStrictEqual(b.to, ['kevin@stiers-construction.com']);
    assert.strictEqual(b.reply_to, 'pat@example.com');
    assert.strictEqual(b.subject, 'New quote request: Pat Smith (Seawall)');
    assert.ok(b.html.includes('&lt;script&gt;') && !b.html.includes('<script>'), 'HTML must be escaped');
    assert.ok(b.text.includes('Job address: 12 Canal St'));
    assert.ok(!b.text.includes('bot-field') && !b.text.includes('form-name'));
    assert.strictEqual(calls[0].opts.headers.Authorization, 'Bearer re_test');
  });
  await t('MAIL_TO overrides the default recipient', async () => {
    reset({ ...ENV, MAIL_TO: 'office@example.com' }); mockFetch([['https://api.resend.com', () => json(200, {})]]);
    await handler(evt(quote())); assert.deepStrictEqual(JSON.parse(calls[0].opts.body).to, ['office@example.com']);
  });
  await t('uploaded photos are fetched and attached', async () => {
    reset(ENV);
    mockFetch([['https://files.netlify.test', () => ({ ok: true, status: 200, arrayBuffer: async () => Buffer.from('JPEGDATA') })], ['https://api.resend.com', () => json(200, {})]]);
    const p = quote({ files: [{ filename: 'wall.jpg', size: 8, type: 'image/jpeg', url: 'https://files.netlify.test/a' }] });
    await handler(evt(p)); const b = JSON.parse(calls[calls.length - 1].opts.body);
    assert.strictEqual(b.attachments.length, 1); assert.strictEqual(b.attachments[0].filename, 'wall.jpg');
    assert.strictEqual(Buffer.from(b.attachments[0].content, 'base64').toString(), 'JPEGDATA');
  });
  await t('failed file download falls back to a link and the email still sends', async () => {
    reset(ENV);
    mockFetch([['https://files.netlify.test', () => ({ ok: false, status: 403 })], ['https://api.resend.com', () => json(200, {})]]);
    const r = await handler(evt(quote({ files: { filename: 'x.jpg', url: 'https://files.netlify.test/x' } })));
    const b = JSON.parse(calls[calls.length - 1].opts.body);
    assert.strictEqual(r.statusCode, 200); assert.ok(!b.attachments); assert.ok(b.text.includes('File not attached') && b.text.includes('x.jpg'));
  });
  await t('careers form sends a job-application email with resume attached', async () => {
    reset(ENV);
    mockFetch([['https://files.netlify.test', () => ({ ok: true, status: 200, arrayBuffer: async () => Buffer.from('PDF') })], ['https://api.resend.com', () => json(200, {})]]);
    const r = await handler(evt({ id: 's2', form_name: 'careers', data: { name: 'Sam Lee', phone: '5865550111', email: 'sam@example.com', experience: '5 years welding', resume: { filename: 'resume.pdf', url: 'https://files.netlify.test/r' } } }));
    const b = JSON.parse(calls[calls.length - 1].opts.body);
    assert.strictEqual(r.statusCode, 200); assert.strictEqual(b.subject, 'New job application: Sam Lee'); assert.strictEqual(b.attachments[0].filename, 'resume.pdf');
  });
  await t('missing API key: no email attempt, submission still reported saved (200)', async () => {
    reset({}); mockFetch([]);
    const r = await handler(evt(quote())); assert.strictEqual(r.statusCode, 200); assert.strictEqual(calls.length, 0);
  });
  await t('provider error returns 502 (visible in Netlify function logs)', async () => {
    reset(ENV); mockFetch([['https://api.resend.com', () => json(422, { message: 'domain not verified' })]]);
    const r = await handler(evt(quote())); assert.strictEqual(r.statusCode, 502);
  });
  await t('network failure returns 502', async () => {
    reset(ENV); global.fetch = async () => { throw new Error('ECONNRESET'); };
    const r = await handler(evt(quote())); assert.strictEqual(r.statusCode, 502);
  });
  await t('unknown form names and filled honeypot are ignored', async () => {
    reset(ENV); mockFetch([]);
    assert.strictEqual((await handler(evt({ id: 'x', form_name: 'other', data: {} }))).statusCode, 200);
    assert.strictEqual((await handler(evt(quote({ 'bot-field': 'gotcha' })))).statusCode, 200);
    assert.strictEqual(calls.length, 0);
  });
  await t('invalid JSON, empty body and GET are rejected', async () => {
    reset(ENV); mockFetch([]);
    assert.strictEqual((await handler({ httpMethod: 'POST', body: 'nope' })).statusCode, 400);
    assert.strictEqual((await handler({ httpMethod: 'POST', body: '{}' })).statusCode, 400);
    assert.strictEqual((await handler({ httpMethod: 'GET' })).statusCode, 405);
  });
  await t('with NETLIFY_API_TOKEN, forged submissions are blocked and real ones pass', async () => {
    reset({ ...ENV, NETLIFY_API_TOKEN: 'tok' });
    mockFetch([['https://api.netlify.com', () => json(404, {})], ['https://api.resend.com', () => json(200, {})]]);
    assert.strictEqual((await handler(evt(quote()))).statusCode, 403);
    assert.ok(!calls.some((c) => c.url.includes('resend')));
    reset({ ...ENV, NETLIFY_API_TOKEN: 'tok' });
    mockFetch([['https://api.netlify.com', () => json(200, { id: 'sub1' })], ['https://api.resend.com', () => json(200, {})]]);
    assert.strictEqual((await handler(evt(quote()))).statusCode, 200); assert.ok(calls.some((c) => c.url.includes('resend')));
  });
  await t('invalid visitor email is not used as reply-to', async () => {
    reset(ENV); mockFetch([['https://api.resend.com', () => json(200, {})]]);
    await handler(evt(quote({ email: 'not-an-email' }))); assert.strictEqual(JSON.parse(calls[0].opts.body).reply_to, undefined);
  });
  console.log(`\n${n} tests passed`);
})().catch((e) => { console.error('FAIL:', e.message); process.exit(1); });
