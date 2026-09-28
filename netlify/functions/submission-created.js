/**
 * Silent form backend for stiersconstruction.com
 *
 * Netlify runs this function automatically every time a verified (non-spam) Netlify Form
 * submission is created ("submission-created" is a reserved event name). It emails the
 * submission to the office inbox and does not change what the visitor sees.
 * Netlify still stores every submission in the dashboard as a backup.
 *
 * Environment variables (Netlify > Site configuration > Environment variables):
 *   RESEND_API_KEY      required   API key from resend.com
 *   MAIL_FROM           required   e.g.  Stier's Website <forms@stiers-construction.com>
 *                                  (or "Stier's Website <onboarding@resend.dev>" while testing;
 *                                   Resend only delivers that sender to the account owner's own address)
 *   MAIL_TO             optional   defaults to kevin@stiers-construction.com
 *   NETLIFY_API_TOKEN   optional   recommended: lets the function confirm each submission is real
 */
'use strict';

const RESEND_URL = () => process.env.RESEND_API_URL || 'https://api.resend.com/emails'; // override is for local testing only
const DEFAULT_TO = 'kevin@stiers-construction.com';
const MAX_ATTACH_BYTES = 20 * 1024 * 1024;
const MAX_FIELD = 5000;

const FORMS = {
  quote: { label: 'Quote request', subject: (d) => `New quote request: ${d.name || 'website visitor'}${d.service ? ' (' + d.service + ')' : ''}` },
  careers: { label: 'Job application', subject: (d) => `New job application: ${d.name || 'applicant'}` },
};
const SKIP = new Set(['bot-field', 'form-name', 'ip', 'user_agent', 'referrer']);
const LABELS = {
  name: 'Name', phone: 'Phone', email: 'Email', address: 'Job address', service: 'Service',
  message: 'Project details', files: 'Photos or video', experience: 'Experience', resume: 'Resume',
};
const ORDER = ['name', 'phone', 'email', 'address', 'service', 'message', 'experience', 'files', 'resume'];

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clip = (s) => String(s).slice(0, MAX_FIELD);
const isFile = (v) => v && typeof v === 'object' && !Array.isArray(v) && typeof v.url === 'string';

function collect(data) {
  const fields = [];
  const files = [];
  for (const [key, raw] of Object.entries(data || {})) {
    if (SKIP.has(key)) continue;
    const list = Array.isArray(raw) ? raw : [raw];
    const fileItems = list.filter(isFile);
    if (fileItems.length) { fileItems.forEach((f) => files.push({ field: key, ...f })); continue; }
    const value = list.filter((v) => v !== null && v !== undefined && v !== '').map((v) => (typeof v === 'object' ? JSON.stringify(v) : String(v))).join(', ');
    if (value) fields.push({ key, label: LABELS[key] || key, value: clip(value) });
  }
  fields.sort((a, b) => {
    const ia = ORDER.indexOf(a.key), ib = ORDER.indexOf(b.key);
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
  });
  return { fields, files };
}

async function loadAttachments(files) {
  const attachments = [];
  const links = [];
  let total = 0;
  for (const f of files) {
    const name = f.filename || f.name || 'attachment';
    try {
      const res = await fetch(f.url);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const buf = Buffer.from(await res.arrayBuffer());
      if (total + buf.length > MAX_ATTACH_BYTES) throw new Error('over attachment size limit');
      total += buf.length;
      attachments.push({ filename: name, content: buf.toString('base64') });
    } catch (err) {
      links.push({ name, url: f.url, reason: err.message });
    }
  }
  return { attachments, links };
}

function buildEmail(formName, meta, fields, links, attachmentCount) {
  const stamp = meta.created_at ? new Date(meta.created_at).toLocaleString('en-US', { timeZone: 'America/Detroit' }) : '';
  const lines = fields.map((f) => `${f.label}: ${f.value}`);
  if (attachmentCount) lines.push(`Attachments: ${attachmentCount} file(s) attached to this email`);
  links.forEach((l) => lines.push(`File not attached (${l.reason}): ${l.name} ${l.url}`));
  const text = `${FORMS[formName].label} from stiersconstruction.com${stamp ? ' (' + stamp + ' Eastern)' : ''}\n\n${lines.join('\n')}\n\nReply to this email to respond to the sender. A copy is also saved in the Netlify Forms dashboard.`;
  const rows = fields.map((f) => `<tr><th align="left" valign="top" style="padding:6px 14px 6px 0;color:#4C5F68;white-space:nowrap">${esc(f.label)}</th><td style="padding:6px 0;white-space:pre-wrap">${esc(f.value)}</td></tr>`).join('');
  const extra = [attachmentCount ? `<p><strong>${attachmentCount}</strong> file(s) attached.</p>` : '', ...links.map((l) => `<p>File not attached (${esc(l.reason)}): <a href="${esc(l.url)}">${esc(l.name)}</a></p>`)].join('');
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#10222B"><h2 style="margin:0 0 4px">${esc(FORMS[formName].label)}</h2><p style="margin:0 0 14px;color:#4C5F68">stiersconstruction.com${stamp ? ' &middot; ' + esc(stamp) + ' Eastern' : ''}</p><table cellpadding="0" cellspacing="0" style="border-collapse:collapse">${rows}</table>${extra}<p style="margin-top:18px;color:#4C5F68">Reply to this email to respond to the sender. A copy is also saved in the Netlify Forms dashboard.</p></div>`;
  return { text, html };
}

exports.handler = async (event) => {
  if (event.httpMethod && event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method not allowed' };

  let payload;
  try { payload = JSON.parse(event.body || '{}').payload; } catch (e) { return { statusCode: 400, body: 'Bad request' }; }
  if (!payload || typeof payload !== 'object') return { statusCode: 400, body: 'Bad request' };

  const formName = payload.form_name;
  const data = payload.data || {};
  if (!FORMS[formName]) return { statusCode: 200, body: 'Ignored: unknown form' };
  if (data['bot-field']) return { statusCode: 200, body: 'Ignored: spam trap' };

  // Optional: confirm the submission really exists in Netlify (blocks forged direct calls to this URL).
  if (process.env.NETLIFY_API_TOKEN) {
    try {
      const check = await fetch(`https://api.netlify.com/api/v1/submissions/${encodeURIComponent(payload.id || '')}`, { headers: { Authorization: `Bearer ${process.env.NETLIFY_API_TOKEN}` } });
      if (!check.ok) return { statusCode: 403, body: 'Submission could not be verified' };
    } catch (e) { return { statusCode: 502, body: 'Verification unavailable' }; }
  }

  const key = process.env.RESEND_API_KEY;
  const from = process.env.MAIL_FROM;
  if (!key || !from) {
    console.warn('Email not sent: set RESEND_API_KEY and MAIL_FROM. The submission is still saved in Netlify Forms.');
    return { statusCode: 200, body: 'Saved in Netlify Forms; email not configured' };
  }

  const { fields, files } = collect(data);
  const { attachments, links } = await loadAttachments(files);
  const { text, html } = buildEmail(formName, payload, fields, links, attachments.length);
  const replyTo = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(data.email || '').trim()) ? String(data.email).trim() : undefined;

  const body = { from, to: [process.env.MAIL_TO || DEFAULT_TO], subject: FORMS[formName].subject(data).slice(0, 200), text, html };
  if (replyTo) body.reply_to = replyTo;
  if (attachments.length) body.attachments = attachments;

  let res;
  try {
    res = await fetch(RESEND_URL(), { method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  } catch (err) {
    console.error('Email provider unreachable:', err.message);
    return { statusCode: 502, body: 'Email provider unreachable' };
  }
  if (!res.ok) {
    console.error('Email provider rejected the message:', res.status, (await res.text()).slice(0, 300));
    return { statusCode: 502, body: 'Email provider error' };
  }
  return { statusCode: 200, body: 'Email sent' };
};
