/**
 * Silent form backend for stiersconstruction.com
 *
 * The quote and careers forms POST straight to this function (no Netlify Forms
 * "detection" step involved), which emails the submission to the office inbox
 * and redirects the visitor to /thank-you/. There is no separate storage/backup
 * of submissions beyond the outgoing email itself, so a failed send is reported
 * back to the visitor instead of silently dropped.
 *
 * Environment variables (Netlify > Site configuration > Environment variables):
 *   RESEND_API_KEY   required   API key from resend.com (RESEND_API also accepted)
 *   MAIL_FROM        optional   e.g.  Stier's Website <forms@stiers-construction.com>
 *                                Defaults to the onboarding@resend.dev test sender, which Resend
 *                                only delivers to the Resend account owner's own address. Once a
 *                                sending domain is verified in Resend (Domains tab), set this to
 *                                an address on that domain so mail reaches MAIL_TO reliably.
 *   MAIL_TO          optional   defaults to kevin@stiers-construction.com
 */
'use strict';

const RESEND_URL = () => process.env.RESEND_API_URL || 'https://api.resend.com/emails'; // override is for local testing only
const DEFAULT_TO = 'kevin@stiers-construction.com';
const DEFAULT_FROM = "Stier's Website <onboarding@resend.dev>";
const MAX_FIELD = 5000;
const PHONE = '586-703-7214';

const FORMS = {
  quote: { label: 'Quote request', subject: (d) => `New quote request: ${d.name || 'website visitor'}${d.service ? ' (' + d.service + ')' : ''}` },
  careers: { label: 'Job application', subject: (d) => `New job application: ${d.name || 'applicant'}` },
};
const SKIP = new Set(['bot-field', 'form-name']);
const LABELS = {
  name: 'Name', phone: 'Phone', email: 'Email', address: 'Job address', service: 'Service',
  message: 'Project details', files: 'Photos or video', experience: 'Experience', resume: 'Resume',
};
const ORDER = ['name', 'phone', 'email', 'address', 'service', 'message', 'experience', 'files', 'resume'];

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clip = (s) => String(s).slice(0, MAX_FIELD);

function errorPage(message) {
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>We Could Not Send That | Stier's Marine & Construction</title></head>
<body style="font-family:Arial,Helvetica,sans-serif;background:#10222B;color:#fff;margin:0;padding:48px 24px;text-align:center">
<h1 style="margin:0 0 12px">We Could Not Send That</h1>
<p style="color:#CBDAE0;max-width:480px;margin:0 auto 20px">${esc(message)} Please call us directly so your project does not wait.</p>
<p style="font-size:1.3rem;margin:0"><a href="tel:+1${PHONE.replace(/[^0-9]/g, '')}" style="color:#fff;font-weight:700">${PHONE}</a></p>
</body></html>`;
  return { statusCode: 502, headers: { 'Content-Type': 'text/html; charset=UTF-8' }, body: html };
}

function parseMultipart(buffer, boundary) {
  const fields = {};
  const files = [];
  const boundaryBuf = Buffer.from(`--${boundary}`);
  let start = buffer.indexOf(boundaryBuf);
  while (start !== -1) {
    const next = buffer.indexOf(boundaryBuf, start + boundaryBuf.length);
    if (next === -1) break;
    let part = buffer.slice(start + boundaryBuf.length, next);
    if (part.slice(0, 2).toString() === '--') break; // closing boundary
    if (part.slice(0, 2).toString('binary') === '\r\n') part = part.slice(2);
    const headerEnd = part.indexOf('\r\n\r\n');
    if (headerEnd !== -1) {
      const headerText = part.slice(0, headerEnd).toString('utf8');
      let body = part.slice(headerEnd + 4);
      if (body.slice(-2).toString('binary') === '\r\n') body = body.slice(0, -2);
      const nameMatch = /name="([^"]*)"/.exec(headerText);
      const fileMatch = /filename="([^"]*)"/.exec(headerText);
      const typeMatch = /Content-Type:\s*([^\r\n]+)/i.exec(headerText);
      const name = nameMatch ? nameMatch[1] : '';
      if (name) {
        if (fileMatch && fileMatch[1]) {
          files.push({ field: name, filename: fileMatch[1], contentType: typeMatch ? typeMatch[1].trim() : 'application/octet-stream', buffer: body });
        } else {
          const value = body.toString('utf8');
          fields[name] = fields[name] ? fields[name] + ', ' + value : value;
        }
      }
    }
    start = next;
  }
  return { fields, files };
}

function buildEmail(formName, fields, files) {
  const lines = fields.map((f) => `${f.label}: ${f.value}`);
  if (files.length) lines.push(`Attachments: ${files.length} file(s) attached to this email`);
  const stamp = new Date().toLocaleString('en-US', { timeZone: 'America/Detroit' });
  const text = `${FORMS[formName].label} from stiersconstruction.com (${stamp} Eastern)\n\n${lines.join('\n')}\n\nReply to this email to respond to the sender.`;
  const rows = fields.map((f) => `<tr><th align="left" valign="top" style="padding:6px 14px 6px 0;color:#4C5F68;white-space:nowrap">${esc(f.label)}</th><td style="padding:6px 0;white-space:pre-wrap">${esc(f.value)}</td></tr>`).join('');
  const extra = files.length ? `<p><strong>${files.length}</strong> file(s) attached.</p>` : '';
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#10222B"><h2 style="margin:0 0 4px">${esc(FORMS[formName].label)}</h2><p style="margin:0 0 14px;color:#4C5F68">stiersconstruction.com &middot; ${esc(stamp)} Eastern</p><table cellpadding="0" cellspacing="0" style="border-collapse:collapse">${rows}</table>${extra}<p style="margin-top:18px;color:#4C5F68">Reply to this email to respond to the sender.</p></div>`;
  return { text, html };
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method not allowed' };

  const contentType = event.headers['content-type'] || event.headers['Content-Type'] || '';
  const boundaryMatch = /boundary=([^;]+)/.exec(contentType);
  if (!boundaryMatch) return errorPage('Your submission arrived in a format we could not read.');

  const raw = event.isBase64Encoded ? Buffer.from(event.body, 'base64') : Buffer.from(event.body || '', 'utf8');
  const { fields: data, files: rawFiles } = parseMultipart(raw, boundaryMatch[1].replace(/^"|"$/g, ''));

  const formName = data['form-name'];
  if (!FORMS[formName]) return errorPage('We could not tell which form this was.');
  if (data['bot-field']) return { statusCode: 303, headers: { Location: '/thank-you/' } }; // spam trap: pretend success, send nothing

  const key = process.env.RESEND_API_KEY || process.env.RESEND_API;
  if (!key) {
    console.warn('Email not sent: set RESEND_API_KEY (or RESEND_API).');
    return errorPage('Our email service is not fully set up yet.');
  }

  const fields = [];
  for (const [k, v] of Object.entries(data)) {
    if (SKIP.has(k) || !v) continue;
    fields.push({ key: k, label: LABELS[k] || k, value: clip(v) });
  }
  fields.sort((a, b) => {
    const ia = ORDER.indexOf(a.key), ib = ORDER.indexOf(b.key);
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
  });

  const files = rawFiles.filter((f) => f.buffer && f.buffer.length);
  const { text, html } = buildEmail(formName, fields, files);
  const replyTo = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(data.email || '').trim()) ? String(data.email).trim() : undefined;

  const body = {
    from: process.env.MAIL_FROM || DEFAULT_FROM,
    to: [process.env.MAIL_TO || DEFAULT_TO],
    subject: FORMS[formName].subject(data).slice(0, 200),
    text,
    html,
  };
  if (replyTo) body.reply_to = replyTo;
  if (files.length) body.attachments = files.map((f) => ({ filename: f.filename, content: f.buffer.toString('base64') }));

  let res;
  try {
    res = await fetch(RESEND_URL(), { method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  } catch (err) {
    console.error('Email provider unreachable:', err.message);
    return errorPage('Our email service could not be reached.');
  }
  if (!res.ok) {
    console.error('Email provider rejected the message:', res.status, (await res.text()).slice(0, 300));
    return errorPage('Our email service rejected the message.');
  }

  return { statusCode: 303, headers: { Location: '/thank-you/' } };
};
