import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'Missing email' });
  }

  try {
    const response = await resend.emails.send({
      from: 'noreply@myndz.net',
      to: 'hello@myndz.net',
      subject: 'New newsletter signup',
      html: `<p><strong>Email:</strong> ${email}</p>`
    });

    return res.status(200).json({ success: true, id: response.id });
  } catch (error) {
    console.error('Newsletter email error:', error);
    return res.status(500).json({ error: 'Failed to send email' });
  }
}
