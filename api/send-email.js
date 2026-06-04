import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, email, company, projectType, brief } = req.body;

  if (!name || !email || !brief) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  try {
    const response = await resend.emails.send({
      from: 'noreply@myndz.net',
      to: 'hello@myndz.net',
      subject: `New Project Brief from ${name}`,
      html: `
        <h2>New Project Brief Submission</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Company/Brand:</strong> ${company || 'Not provided'}</p>
        <p><strong>Project Type:</strong> ${projectType || 'Not specified'}</p>
        <h3>Brief:</h3>
        <p>${brief.replace(/\n/g, '<br>')}</p>
      `
    });

    return res.status(200).json({ success: true, id: response.id });
  } catch (error) {
    console.error('Email error:', error);
    return res.status(500).json({ error: 'Failed to send email' });
  }
}
